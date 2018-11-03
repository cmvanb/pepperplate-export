# -----------------------------------------------------------------------------
# Parse recipe HTML
# -----------------------------------------------------------------------------
def parse_recipe_html(inputFile):
    from bs4 import BeautifulSoup
    import io
    import json
    import re
    import string
    import unicodedata

    # Config ------------------------------------------------------------------

    outputDirectory = 'parsed-recipes'
    ingredientUnitsMap = {
        u'ml': u'ml',
        u'milliliter': u'ml',
        u'milliliters': u'ml',

        u'l': u'l',
        u'liter': u'l',
        u'liters': u'l',

        u'mg': u'mg',
        u'milligram': u'mg',
        u'milligrams': u'mg',

        u'g': u'g',
        u'gram': u'g',
        u'grams': u'g',

        u'kg': u'kg',
        u'kilogram': u'kg',
        u'kilograms': u'kg',

        u'tsp': u'tsp',
        u'teaspoon': u'tsp',
        u'teaspoons': u'tsp',

        u'tbsp': u'tbsp',
        u'tablespoon': u'tbsp',
        u'tablespoons': u'tbsp',

        u'cup': u'cup',
        u'cups': u'cup',

        u'oz': u'oz',
        u'ounce': u'oz',
        u'ounces': u'oz',

        u'lb': u'lb',
        u'lbs': u'lb',
        u'pound': u'lb',
        u'pounds': u'lb',

        u'small': u'small',
        u'medium': u'medium',
        u'large': u'large',
    }

    # Setup -------------------------------------------------------------------

    def slugify(value):
        """
        Convert to ASCII. Convert spaces to hyphens.
        Remove characters that aren't alphanumerics, underscores, or hyphens.
        Convert to lowercase. Also strip leading and trailing whitespace.
        """
        value = unicode(str(value))
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
        value = re.sub(r'[^\w\s-]', '', value).strip().lower()
        return re.sub(r'[-\s]+', '-', value)

    def merge_maps(x, y):
        z = x.copy()
        z.update(y)
        return z

    output = {}

    # Script ------------------------------------------------------------------

    print "Parsing..."

    # Get recipe page
    with io.open(inputFile, 'r', encoding='utf-8') as f:
        parseTarget = f.read()

    # Parse recipe
    soup = BeautifulSoup(parseTarget, 'html.parser')

    items = soup.find_all('div', class_='item')

    title = soup.title.string.split('-', 1)[1].strip()
    filename = slugify(title) + u'.json'

    yield_ = items[0].span.string.strip() if len(items) >= 1 else '1'
    activeTime = items[1].span.string.strip() if len(items) >= 2 else '0'
    totalTime = items[2].span.string.strip() if len(items) >= 3 else '0'
    categories = map(lambda c:c.strip(), items[3].span.string.strip().split(',')) if len(items) >= 4 else []

    output = merge_maps(output, {
        'title': title,
        'filename': filename,
        'yield': yield_,
        'activeTime': activeTime,
        'totalTime': totalTime,
        'categories': categories
    })

    # ingredients
    ingredients = []

    sections = soup.find_all('ul', class_='inggroupitems')

    remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)

    for section in sections:
        title = (section.previous_sibling.previous_sibling and section.previous_sibling.previous_sibling.string.strip() or '')
        o_section = {
            'title': title,
            'items': []
        }
        items = section.find_all('span', class_='content')
        for item in items:
            quantity = (item.span.string or '').strip()
            ingredient = (item.contents[2]).strip()
            unit = ''
            splitIngredient = ingredient.split(' ')
            for u in ingredientUnitsMap:
                splitIndex = 0
                for ingredientFragment in splitIngredient:
                    splitIndex = splitIndex + 1
                    igf = ingredientFragment.lower().translate(remove_punctuation_map)
                    if u == igf:
                        unit = igf
                        ingredient = string.join(splitIngredient[splitIndex:])
                        break
            o_section['items'].append({
                'quantity': quantity,
                'ingredient': ingredient,
                'unit': unit
            })
        ingredients.append(o_section)

    output = merge_maps(output, {
        'ingredients': ingredients
    })

    # instructions
    instructions = []

    sections = soup.find_all('ol', class_='dirgroupitems')

    for section in sections:
        title = (section.previous_sibling.previous_sibling and section.previous_sibling.previous_sibling.string.strip() or '')
        o_section = {
            'title': title,
            'items': []
        }
        items = section.find_all('span', class_='text')
        for item in items:
            if item.string.strip() == 'Instructions':
                continue
            o_section['items'].append(item.string.strip())
        instructions.append(o_section)

    output = merge_maps(output, {
        'instructions': instructions
    })

    # Write result to file
    outputFileName = outputDirectory + '/' + output['filename']

    outputFileContent = unicode(json.dumps(output))

    with io.open(outputFileName, 'w', encoding='utf-8') as f:
        f.write(outputFileContent)

    print '...done.'

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print 'ERROR: Missing command line argument: inputFile'
        sys.exit(1)

    print sys.argv

    parse_recipe_html(sys.argv[1])

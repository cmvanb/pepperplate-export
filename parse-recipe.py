import io
import re
import unicodedata
import json
from bs4 import BeautifulSoup

# -----------------------------------------------------------------------------
# Config
# -----------------------------------------------------------------------------

inputFile = 'result.html'
outputDirectory = 'parsed-recipes'

# -----------------------------------------------------------------------------
# Setup
# -----------------------------------------------------------------------------

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

# -----------------------------------------------------------------------------
# Script
# -----------------------------------------------------------------------------

print "Parsing..."

# Get recipe page
with io.open(inputFile, 'r', encoding='utf-8') as f:
    parseTarget = f.read()

# Parse recipe
soup = BeautifulSoup(parseTarget, 'html.parser')

items = soup.find_all('div', class_='item')

title = soup.title.string.split('-', 1)[1].strip()
filename = slugify(title) + u'.json'
yield_ = items[0].span.string.strip()
activeTime = items[1].span.string.strip()
totalTime = items[2].span.string.strip()
categories = map(lambda c:c.strip(), items[3].span.string.strip().split(','))

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
        o_section['items'].append({
            'quantity': quantity,
            'ingredient': ingredient
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

# final output
for k, v in output.iteritems():
    print k, v

# Write result to file
outputFileName = outputDirectory + '/' + output['filename']

outputFileContent = unicode(json.dumps(output))

with io.open(outputFileName, 'w', encoding='utf-8') as f:
    f.write(outputFileContent)

print '...done.'

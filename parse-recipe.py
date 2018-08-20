import io
from bs4 import BeautifulSoup

# -----------------------------------------------------------------------------
# Config
# -----------------------------------------------------------------------------

inputFile = 'result.html'

# -----------------------------------------------------------------------------
# Setup
# -----------------------------------------------------------------------------

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

# title
title = soup.title

# yield, active time, total time, categories
items = soup.find_all('div', class_='item')

output = merge_maps(output, {
    'title': title.string.strip(),
    'yield': items[0].span.string.strip(),
    'activeTime': items[1].span.string.strip(),
    'totalTime': items[2].span.string.strip(),
    'categories': items[3].span.string.strip()
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

print '...done.'

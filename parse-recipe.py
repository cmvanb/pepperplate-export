import io
from bs4 import BeautifulSoup

# -----------------------------------------------------------------------------
# Config
# -----------------------------------------------------------------------------

inputFile = 'result.html'

# -----------------------------------------------------------------------------
# Setup
# -----------------------------------------------------------------------------

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

metaData = {
    'yield': items[0].span.string.strip(),
    'activeTime': items[1].span.string.strip(),
    'totalTime': items[2].span.string.strip(),
    'categories': items[3].span.string.strip()
}

for k, v in metaData.iteritems():
    print k, v

# ingredients
ingredients = soup.find('div', class_='ingcontainer')

# instructions
instructions = soup.find('div', class_='dircontainer')

print '...done.'


# h = html2text.HTML2Text()
# h.ignore_links = True
# result = h.handle(rawHTML)
# cphMiddle_cphMain_lblTitle

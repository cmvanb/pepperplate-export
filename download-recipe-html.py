import io
import mechanize
import cookielib
from bs4 import BeautifulSoup
import html2text
import configparser

# -----------------------------------------------------------------------------
# Config
# -----------------------------------------------------------------------------

config = configparser.RawConfigParser()
config.read('credentials.ini')

email = config['DEFAULT']['email']
password = config['DEFAULT']['password']

urlLogin = 'https://www.pepperplate.com/login.aspx'
urlRecipe = 'http://www.pepperplate.com/recipes/view.aspx?id=20460714'

outputFile = 'result.html'

# -----------------------------------------------------------------------------
# Setup
# -----------------------------------------------------------------------------

# Use mechanize
br = mechanize.Browser()

# Store cookies in the cookie jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

br.addheaders = [('User-agent', 'Chrome')]

# -----------------------------------------------------------------------------
# Script
# -----------------------------------------------------------------------------

print "Downloading..."

# Read login page
br.open(urlLogin)

# View forms on page
for f in br.forms():
    print f

# Select login form, pass credentials and login
br.select_form(nr=0)

br.form['ctl00$cphMain$loginForm$tbEmail'] = email
br.form['ctl00$cphMain$loginForm$tbPassword'] = password

br.submit()

# Read recipe page
result = br.open(urlRecipe).read().decode('utf-8')

# Write result to file
with io.open(outputFile, 'w', encoding='utf-8') as f:
    f.write(result)

print '...done.'

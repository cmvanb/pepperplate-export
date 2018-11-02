# -----------------------------------------------------------------------------
# Download recipe HTML
# -----------------------------------------------------------------------------
def download_recipe_html(recipe_id):
    import configparser
    import cookielib
    import io
    import mechanize

    # ---- Config -------------------------------------------------------------

    config = configparser.RawConfigParser()
    config.read('credentials.ini')

    email = config['DEFAULT']['email']
    password = config['DEFAULT']['password']

    urlLogin = 'https://www.pepperplate.com/login.aspx'
    urlRecipe = 'http://www.pepperplate.com/recipes/view.aspx?id=' + str(recipe_id)

    outputFile = str(recipe_id) + '.html'

    # ---- Mechanize Setup ----------------------------------------------------

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

    # ---- Script -------------------------------------------------------------

    print 'Downloading ' + urlRecipe + ' ...'

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

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    import sys

    if not sys.argv[1]:
        print 'ERROR: Missing command line argument: recipe_id'
        sys.exit(1)

    download_recipe_html(sys.argv[1])

def download_from_json(recipes_json):
    import json
    import time
    import download_recipe_html

    print 'Downloading from ' + recipes_json + ' ...'

    # TODO: Download to directory.

    with open(recipes_json, 'r') as f:
        recipes = json.load(f)

        for r in recipes:
            url = r['url']
            time.sleep(1)
            download_recipe_html.download_recipe_html(url)
            # img = r['img']

    print '...done.'

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    import sys

    if not sys.argv[1]:
        print 'ERROR: Missing command line argument: recipes_json'
        sys.exit(1)

    download_from_json(sys.argv[1])

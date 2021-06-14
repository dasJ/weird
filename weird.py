#!/usr/bin/env python3

import argparse
import json
import requests
import sys
import uuid
from bs4 import BeautifulSoup

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('-8', '--x86',
                    default=False, action='store_true',
                    help='Request x86 instead of x64')
parser.add_argument('-l', '--language',
                    type=str, default='English',
                    help='Language to request link for')
parser.add_argument('edition',
                    type=str,
                    help='Edition to request - use "latest" for the latest version')
parser.add_argument('-L', '--list-langs',
                    default=False, action='store_true',
                    help='List languages instead of downloading')
parser.add_argument('-S', '--show-edition',
                    default=False, action='store_true',
                    help='Show edition number we would download (mainly useful for the latest edition)')
args = parser.parse_args()

# Prepare requests
sessionID = uuid.uuid1()
s = requests.Session()
s.headers.update({
    'User-Agent': 'Mozilla/5.0 (X11; Linux i586; rv:57.0) Gecko/1/1/2008 Firefox/57.0'
})

# Fetch latest version
if args.edition == 'latest':
    url = 'https://www.microsoft.com/en-us/software-download/windows10ISO'
    resp = s.get(url)
    assert resp.status_code == 200
    html = BeautifulSoup(resp.text, features='html.parser')
    edition = 0
    for opt in html.find_all('option'):
        value = opt['value']
        if value == '':
            continue
        if int(value) > edition:
            edition = int(value)
else:
    edition = args.edition

if args.show_edition:
    print(edition)
    sys.exit(0)

# Fetch languages
url = 'https://www.microsoft.com/en-US/api/controls/contentinclude/html' + \
    '?pageId=a8f8f489-4c7f-463a-9ca6-5cff94d8d041' + \
    '&host=www.microsoft.com' + \
    '&segments=software-download,windows10ISO' + \
    '&query=&action=getskuinformationbyproductedition' + \
    '&sessionId={}'.format(sessionID) + \
    '&productEditionId={}'.format(edition) + \
    '&sdVersion=2'

# Request all languages
resp = s.post(url)
assert resp.status_code == 200

# Parse languages into an object
skus = {}
html = BeautifulSoup(resp.text, features='html.parser')
for opt in html.find_all('option'):
    text = opt.text
    value = opt['value']
    if value == '':
        continue
    skus[text] = value

if args.list_langs:
    for name in skus.keys():
        print(name)
    sys.exit(0)

# Select language
sku = skus[args.language]
skuJson = json.loads(sku)
skuId = skuJson['id']
skuName = skuJson['language']

# Fetch download links
url = 'https://www.microsoft.com/en-US/api/controls/contentinclude/html' + \
    '?pageId=cfa9e580-a81e-4a4b-a846-7b21bf4e2e5b' + \
    '&host=www.microsoft.com' + \
    '&segments=software-download,windows10ISO' + \
    '&query=&action=GetProductDownloadLinksBySku' + \
    '&sessionId={}'.format(sessionID) + \
    '&skuId={}'.format(skuId) + \
    '&language={}'.format(skuName) + \
    '&sdVersion=2'

# Request downloads
resp = s.post(url)
assert resp.status_code == 200
html = BeautifulSoup(resp.text, features='html.parser')

# Parse downloads
downloads = html.find_all('a', {'class': 'button-flat'})
# This weird contraption is the Python equivalent of Nix's `!args.x86 -> 'IsoX64' in d.text` and `head`
download = filter(lambda d: args.x86 or 'IsoX64' in d.text, downloads).__next__()
print(download['href'])

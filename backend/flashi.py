#!/usr/bin/env python3
"""
Script to convert PDF into images and convert into text.

IMPORTANT: This script requires imagemagick to be installed on your system.
"""

import http.client
import subprocess
import urllib.request
import urllib.parse
import urllib.error
import base64
import json

KEY = ''
with open('api.key') as key:
    KEY = key.read().strip()

URI_BASE = 'westcentralus.api.cognitive.microsoft.com'

HEADERS = {
    # Request headers.
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': KEY,
}

PARAMS = urllib.parse.urlencode({
    # Request parameters.
    'language': 'en',
})


def ocr_request(body):
    """ Make an OCR request to Microsoft cognitive services Vision API."""
    try:
        # Execute the REST API call and get the response.
        conn = http.client.HTTPSConnection(URI_BASE)
        conn.request('POST', '/vision/v1.0/ocr?%s' % PARAMS, body, HEADERS)
        response = conn.getresponse()
        data = response.read()

        # 'data' contains the JSON data. The following formats the JSON data for display.
        parsed = json.loads(data)
        print("Response:")
        print(json.dumps(parsed, sort_keys=True, indent=2))
        conn.close()

    except Exception as err:
        print('An error occurred:')
        print(err)


def pagify_pdf(uri):
    """ Return individual images for each page of a PDF."""
    ## convert -density 250 input.pdf output.jpg
    subprocess.call()
    

if __name__ == '__main__':
    ocr_request("{'url':'https://raw.githubusercontent.com/jordanspooner/first-year-notes/master/112.pdf'}")

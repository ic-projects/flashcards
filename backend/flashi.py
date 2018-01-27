#!/usr/bin/env python3
"""
Script to convert PDF into images and request OCR
"""

import requests
from wand.image import Image
from wand.color import Color

KEY = ''
with open('api.key') as key:
    KEY = key.read().strip()

URI_BASE = 'https://westcentralus.api.cognitive.microsoft.com'

HEADERS = {
    # Request headers.
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': KEY,
}

PARAMS = {
    # Request parameters.
    'language': 'en',
}


def pagify_and_ocr(fname):
    """Print the text contained within a PDF document"""
    num_pages = pagify_pdf(fname)
    for page in range(num_pages):
        image = ''
        with open(fname+str(page+1)+'.png', 'rb') as file:
            image = file.read()
        ocr_request(image)


def ocr_request(image):
    """Make an OCR request to Microsoft cognitive services Vision API"""
    try:
        response = requests.post(url=URI_BASE+'/vision/v1.0/ocr',
                                 headers=HEADERS,
                                 params=PARAMS,
                                 data=image)
        data = response.json()
        for region in data['regions']:
            for line in region['lines']:
                for word in line['words']:
                    print(word['text'], end=' ')
                print('')
            print('')
        print('')

    except Exception as err:
        print('An error occurred:')
        print(err)


def pagify_pdf(fname):
    """Create a PNG image for each page of a PDF document"""
    all_pages = Image(filename=fname+'.pdf', resolution=250)
    count = 1
    for page in all_pages.sequence:
        img = Image(page)
        img.format = 'png'
        img.background_color = Color('white')
        img.alpha_channel = 'remove'
        img.save(filename=fname+str(count)+'.png')
        count += 1
    return count - 1


if __name__ == '__main__':
    pagify_and_ocr('test/140')

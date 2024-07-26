import mimetypes
import requests
import argparse
import sys

if len(sys.argv) == 2:
    if sys.argv[1] == 'list':
        r = requests.get('http://127.0.0.1:8888/list')
        print(r.text)
    else:
        print('Wrong argument')
elif len(sys.argv) == 3:
    if sys.argv[1] == 'upload':
        with open(sys.argv[2], 'r+b') as f:
            r = requests.post('http://127.0.0.1:8888/upload',
                              files={'file': (f.name[f.name.rfind('/'):], f, mimetypes.guess_type(f.name)[0])})
    else:
        print('Wrong argument')

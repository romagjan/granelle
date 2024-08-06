from flask import Flask
from parser import *
URLs = [
            'https://a101.ru/api/v2/flat/?filter_type=price&limit=50&complex=18',
         
            'https://a101.ru/api/v2/flat/?filter_type=price&limit=2000&complex=17',
            'https://a101.ru/api/v2/flat/?filter_type=price&limit=2000&complex=123',
            'https://a101.ru/api/v2/flat/?filter_type=price&limit=1000&complex=78',
            'https://a101.ru/api/v2/flat/?filter_type=price&limit=200&complex=127',
         
        ]


granel_objects = [
        '19',
#        '33',
#        '34',
#        '20',
#        '31',
#        '29'
        ]
dsk_objects = [
        '1-leningradskij',
        'uznaa-bitca'
        ]
URL_GRANEL='https://www.granelle.ru/flats/?group=0&complex=object_id&page=1'
app = Flask(__name__)


@app.route('/')
def home():
    result = ''
    for obj in granel_objects:
        
        result += scrape_site(URL_GRANEL.replace('object_id',obj))
    
    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8080)

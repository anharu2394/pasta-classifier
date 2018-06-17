import os
 
import time
import traceback
 
import flickrapi
from urllib.request import urlretrieve
 
import sys
from retry import retry
 
flickr_api_key = os.environ["FLICKR_API_KEY"]
secret_key = os.environ["FLICKR_SECRET_KEY"]
 
keyword = sys.argv[1]
 
 
@retry()
def get_photos(url, filepath):
    urlretrieve(url, filepath)
    time.sleep(1)
 
 
if __name__ == '__main__':
 
    flicker = flickrapi.FlickrAPI(flickr_api_key, secret_key, format='parsed-json')
    response = flicker.photos.search(
        text=keyword,
        per_page=300,
        media='photos',
        sort='relevance',
        safe_search=1,
        extras='url_q,license'
    )
    photos = response['photos']
 
    try:
        for photo in photos['photo']:
            url_q = photo['url_q']
            filepath = './../images/' + keyword + '/' + photo['id'] + '.jpg'
            get_photos(url_q, filepath)
 
    except Exception as e:
        traceback.print_exc()

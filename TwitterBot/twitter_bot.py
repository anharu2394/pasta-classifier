import tweepy
import datetime
import pickle
from sklearn import model_selection
from sklearn.linear_model import LogisticRegression
import numpy as np
import io
from skimage import io as data
import urllib.request
from PIL import Image
import os

def pasta_classifier(url):
    clf = pickle.load(open("./../classifier/pasta_model.sav", 'rb'))
    img_vec = np.array([get_img_vec(url)])
    img_vec = np.array(img_vec.reshape(len(img_vec), -1).astype(np.float64))
    print(img_vec)
    pred = clf.predict(np.array(img_vec))
    print(pred[0])
    return pred[0]
def get_img_vec(url):
    size = 75
    f = io.BytesIO(urllib.request.urlopen(url).read())
    img = Image.open(f)
    w, h = img.size
    left, top, right, bottom = 0, 0, 75,75
    new_width,  new_height = 75,75

    if w >= h:  # 横幅が大きかったときの処理
        new_width = size * w / h
        left = (new_width - size) / 2
        right = new_width - left
    else:  # 高さが大きかったときの処理
        new_height = size * h / w
        top = (new_height - size) / 2
        bottom = new_height - top

    img = img.resize((int(new_width), int(new_height)), Image.ANTIALIAS)
    img = img.crop((left, top, right, bottom))
    return np.array(img)
CK=os.environ["CK"]
CS=os.environ["CS"]
AT=os.environ["AT"]
AS=os.environ["AS"]

auth = tweepy.OAuthHandler(CK, CS)
auth.set_access_token(AT, AS)

api = tweepy.API(auth)

class Listener(tweepy.StreamListener):
    def on_status(self, status):
        status.created_at += datetime.timedelta(hours=9)
        print("aaaa")

        if str(status.in_reply_to_screen_name)=="pastaClassifier":
            print("will reply")
            status_id=status.id
            try:
                url = status.entities["media"][0]["media_url"]
                print(url)
                result = pasta_classifier(url)
                if result == 1:
                    tweet =  "この画像はカルボナーラです。\n https://twitter.com/" + status.user.screen_name + "/status/" +str(status_id) 
                else:
                    tweet = "この画像はボロネーゼです。 \n https://twitter.com/" + status.user.screen_name + "/status/" + str(status_id)
                api.update_status(status=tweet)
            except:
                tweet = "@" + str(status.user.screen_name) + " " + "こんにちは, このBotは\nカルボナーラかボロネーゼか\n分類できることができます。\n" 
                #import traceback
                #traceback.print_exc()
                api.update_status(status=tweet,in_reply_to_status_id=status_id)
        return True

    def on_error(self, status_code):
        print('Got an error with status code: ' + str(status_code))
        return True

    def on_timeout(self):
        print('Timeout...')
        return True

auth = tweepy.OAuthHandler(CK, CS)
auth.set_access_token(AT, AS)

listener = Listener()
stream = tweepy.Stream(auth, listener)
stream.userstream()

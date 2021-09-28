import tweepy
import time as timee
import re
from tokens import consumer_key, consumer_secret, access_token, access_token_secret
from PIL import Image, ImageDraw
from bhaskara import make_put_bhaskara
from datetime import *
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

def send_tweet(media, tweet, local):
    status = f"Opa {tweet.user.name}! Aqui está sua Bhaskara:"
    if local == 1:
        api.send_direct_message(recipient_id=tweet.user.id, text=status, attachment_type='media',
                                attachment_media_id=media.media_id)
    else:
        api.update_with_media(filename='bhaskaraFromTweet.png', status=status, in_reply_to_status_id=tweet.id,
                              auto_populate_reply_metadata=True)

def limit_handler(cursor):
    try:
        while True:
            yield cursor.next()
    except tweepy.RateLimitError:
        time.sleep(300)

def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id


def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

file_name = "last_seen_id.txt"
numberOfTweets = 20

def reply_tweets(file_name):
    now = datetime.now()
    print(now.date(), str(now.hour) + ":" + str(now.minute) + ":" + str(now.second))
    local = 0
    last_seen_id = retrieve_last_seen_id(file_name)
    mentions = api.mentions_timeline(last_seen_id, tweet_mode='extended')
    for tweet in reversed(mentions):
        try:
            img = Image.new('RGB', (250, 180), color=(144, 207, 241, 0))
            img_draw = ImageDraw.Draw(img)

            if 'a=' and 'b=' and 'c=' in tweet.full_text.lower():
                try:
                    last_seen_id = tweet.id
                    store_last_seen_id(last_seen_id, file_name)

                    a, b, c = '', '', ''
                    res = re.split('@joaop_dss|a= |b= |c= |\s+', tweet.full_text)
                    print(res)
                    for i in res:
                        if 'a=' in i:
                            a = int(i.split('a=')[1])
                        elif 'b=' in i:
                            b = int(i.split('b=')[1])
                        elif 'c=' in i:
                            c = int(i.split('c=')[1])
                    make_put_bhaskara(a, b, c, img_draw)
                    img.save('bhaskaraFromTweet.png')
                    media = api.media_upload(filename='bhaskaraFromTweet.png')

                    if 'dm' in tweet.full_text or 'direct' in tweet.full_text:
                        print(tweet.full_text)
                        local = 1
                    send_tweet(media, tweet, local)
                    timee.sleep(1)

                except ValueError as e:
                    print("This error occured: " + str(
                        e) + " due to tweet - " + tweet.full_text + " from " + tweet.user.name + "\n")

        except tweepy.TweepError as e:
            print(e.reason)
        except StopIteration:
            break


while True:
    reply_tweets(file_name)
    timee.sleep(40)
from math import factorial
from dapr.ext.grpc import App, BindingRequest
import json
from dapr.clients import DaprClient
from dapr.clients.grpc._state import StateItem
from dapr.clients.grpc._request import TransactionalStateOperation, TransactionOperationType

from time import sleep
import os 
import tweepy
from flask import Flask,request
fla = Flask(__name__)

#app = App()

DAPR_STORE_NAME = "blob-state-store"
#@app.binding('tweetqueuebinding')
@fla.route("/tweetqueuebinding", methods=['POST'])
def binding():#request: BindingRequest
    #print(request.get_data().decode())
    tweet = json.loads(request.get_data().decode())
    #tweet=json.loads(request.text())
    print("il  y a un tweet")
    print(tweet,flush=True)
    with DaprClient() as d:
        #consumer_key = d.get_secret(store_name="my-secrets-store", key="consumer-key")
        #consumer_secret = d.get_secret(store_name="my-secrets-store", key="consumer-secret")
        #access_token = d.get_secret(store_name="my-secrets-store", key="access-token")
        #access_secret = d.get_secret(store_name="my-secrets-store", key="access-secret")
        #auth = tweepy.OAuthHandler(consumer_key.secret["consumer-key"], consumer_secret.secret["consumer-secret"])
        #auth.set_access_token(access_token.secret["access-token"], access_secret.secret["access-secret"])
        auth = tweepy.OAuthHandler(os.getenv("CONSUMERKEY"), os.getenv("CONSUMERSECRET"))
        auth.set_access_token(os.getenv("ACCESSTOKEN"), os.getenv("ACCESSSECRET"))
        
        api = tweepy.API(auth)
        if(not tweet["user"].get("following",True)):
            
            todayFollow = d.get_state(DAPR_STORE_NAME, "gangogh-follow-bot")
        
            follow=todayFollow.json()["follow"]
            like=todayFollow.json()["like"]
            if(follow<400):
                try:
                    api.create_friendship(user_id=int(tweet["user"]["id_str"]))
                    follow=follow+1
                    print("follow")
                except tweepy.Forbidden as e:
                    print("Forbidden Error: {}".format(e))
                    if(e.api_codes.count(162)<0):#if it's a user who has block don't stop following others
                        follow=400
                except tweepy.TweepyException as e:
                    print("Tweepy Error: {}".format(e))
            

        if(not tweet.get("favorited",True)):
            if(tweet.get("retweeted_status",None) is None):
                idfav = int(tweet["id_str"])
            # elif(not tweet["retweeted_status"]["favorited"]):
            #     idfav = int(tweet["retweeted_status"]["id_str"])
                if(like<1000):
                    try:
                        api.create_favorite(idfav)
                        like=like+1
                        print("fav")
                    except tweepy.Forbidden as e:
                        print(str(idfav)+" Forbidden Error: {}".format(e))
                        if(e.api_codes.count(139)<0):
                            like=1000
                    except tweepy.NotFound as e:
                        print(str(idfav)+"Not Found: {}".format(e))
                    except tweepy.TweepyException as e:
                        print("Tweepy Error: {}".format(e))
        if(follow!=todayFollow.json()["follow"] or like!=todayFollow.json()["like"]):   
            d.save_state(DAPR_STORE_NAME, "gangogh-follow-bot", json.dumps({"follow":follow,"like":like})) 
    return "OK"

@fla.route("/tweetqueuebinding", methods=['OPIONS'])
@fla.route("/resetfollow", methods=['OPIONS'])
@fla.route("/unfollowtime", methods=['OPIONS'])
def Option():
    return "OK"

@fla.route("/unfollowtime", methods=['POST'])
def UnFollow():
    #consumer_key = d.get_secret(store_name="my-secrets-store", key="consumer-key")
    #consumer_secret = d.get_secret(store_name="my-secrets-store", key="consumer-secret")
    #access_token = d.get_secret(store_name="my-secrets-store", key="access-token")
    #access_secret = d.get_secret(store_name="my-secrets-store", key="access-secret")
    #auth = tweepy.OAuthHandler(consumer_key.secret["consumer-key"], consumer_secret.secret["consumer-secret"])
    #auth.set_access_token(access_token.secret["access-token"], access_secret.secret["access-secret"])
    auth = tweepy.OAuthHandler(os.getenv("CONSUMERKEY"), os.getenv("CONSUMERSECRET"))
    auth.set_access_token(os.getenv("ACCESSTOKEN"), os.getenv("ACCESSSECRET"))
    api = tweepy.API(auth,wait_on_rate_limit=True)
    followers = api.get_follower_ids()
    following = api.get_friend_ids()
    oldfolks = following[len(following)-400:]
    nofollow = list(filter(lambda x: not x in followers, oldfolks))
    for folk in nofollow:
        api.destroy_friendship(user_id=folk)
    print("unfollowed "+str(len(nofollow))+" folks")
    return "OK"

@fla.route("/resetfollow", methods=['POST'])
def Reset():
    with DaprClient() as d:   
        print("reset follow")
        d.save_state(DAPR_STORE_NAME, "gangogh-follow-bot", json.dumps({"follow":0,"like":0}))
    return "OK"

with DaprClient() as d:             
    todayFollow = d.get_state(DAPR_STORE_NAME, "gangogh-follow-bot")
    if(not todayFollow.data):       
        d.save_state(DAPR_STORE_NAME, "gangogh-follow-bot", json.dumps({"follow":0,"like":0}))
        print("init follow")
    else:
        print("starting... today follow "+todayFollow.text())
fla.run(host="localhost", port=5000, debug=False)
#app.run(5000)
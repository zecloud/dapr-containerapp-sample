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
                    follow=400
                
            

        if(not tweet.get("favorited",True)):
            if(tweet.get("retweeted_status",None) is None):
                idfav = int(tweet["id_str"])
            elif(not tweet["retweeted_status"]["favorited"]):
                idfav = int(tweet["retweeted_status"]["id_str"])
            if(like<1000):
                try:
                    api.create_favorite(idfav)
                    like=like+1
                    print("fav")
                except tweepy.Forbidden as e:
                    print("Forbidden Error: {}".format(e))
                    like=1000
                
        d.save_state(DAPR_STORE_NAME, "gangogh-follow-bot", json.dumps({"follow":follow,"like":like})) 
    return "OK"

@fla.route("/tweetqueuebinding", methods=['OPIONS'])
def Option():
    return "OK"

@fla.route("/resetfollow", methods=['OPIONS'])
def Option2():
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
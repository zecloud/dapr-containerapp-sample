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


#@app.binding('tweetqueuebinding')
@fla.route("/tweetqueuebinding", methods=['POST'])
def binding():#request: BindingRequest
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
            api.create_friendship(user_id=int(tweet["user"]["id_str"]))
            print("follow")
            if(not tweet.get("favorited",True) and (tweet.get("retweeted_status",None) is None)):
                api.create_favorite(int(tweet["id_str"]))
                print("fav")
    return "OK"

@fla.route("/tweetqueuebinding", methods=['OPIONS'])
def Option():
    return "OK"

fla.run(host="localhost", port=5000, debug=False)
#app.run(5000)
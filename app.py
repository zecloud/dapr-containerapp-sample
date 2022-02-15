from dapr.ext.grpc import App, BindingRequest
import json
from dapr.clients import DaprClient
from time import sleep
import os 

app = App()

@app.binding('tweets-binding')
def binding(request: BindingRequest):
    tweet=json.loads(request.text())
    jsonqueue={ "message": tweet}
    
    
    with DaprClient() as d:
        resp = d.invoke_binding('tweetqueuebinding', 'create', json.dumps(jsonqueue))

app.run(5000)
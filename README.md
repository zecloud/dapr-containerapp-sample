# dapr-containerapp-sample  
Sample dapr app deployed in containerapp  
  
Use the custom DevContainer with custom dockerfile to run this locally it contains all the necessary tools (dotnetcore, dapr cli, python, az cli)  
  
to run this locally  
  
create a secret.json file with the following keys   
{  
    "consumer-key":"",  
    "consumer-secret":"",  
    "access-token":"",  
    "access-secret":"",  
    "storage-account-name":"",  
    "storage-account-key":""  
}  
  
Get consumer-key, consumer-secret, access-token, access-secret by creating an app on dev.twitter.com  
Get storage-account-name and storage-account-key by creating and Azure Storage Account or using the Azure Account emulator  
  
To run the F# app 
   
dapr run --app-id twitter-text --app-port 5276 --components-path ../components  -- dotnet run  
  
To run the Python app
  
dapr run --app-id twitter-follow --app-port 5000 --app-protocol http --components-path ../components  -- python3 app.py  
  
To deploy it on Azure container app you need to have a container registry already created in your azure subscription and fill the following env var  
$RESOURCE_GROUP  Resource group Name  
$LOCATION  Location  
$LOG_ANALYTICS_WORKSPACE  Log Analytics Workspace Name  
$CONTAINERAPPS_ENVIRONMENT  Container Apps Environment Name  
$STORAGE_ACCOUNT  Storage Account name  
$CONTAINER_IMAGE_NAME  Container Image name  
$REGISTRY_SERVER  Azure Container Registry Server (needs to be already created)  
$CONSUMERKEY  Twitter App Key  
$CONSUMERSECRET Twitter App Key  
$ACCESSTOKEN  Twitter App Key  
$ACCESSSECRET  Twitter App Key  

Run Az login to connect to your azure subscription  
run infra.sh to create the necessary resources on Azure and to deploy   

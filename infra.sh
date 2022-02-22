az group create --name $RESOURCE_GROUP --location $LOCATION
az monitor log-analytics workspace create \
  --resource-group $RESOURCE_GROUP \
  --workspace-name $LOG_ANALYTICS_WORKSPACE
LOG_ANALYTICS_WORKSPACE_CLIENT_ID=`az monitor log-analytics workspace show --query customerId -g $RESOURCE_GROUP -n $LOG_ANALYTICS_WORKSPACE -o tsv | tr -d '[:space:]'`
LOG_ANALYTICS_WORKSPACE_CLIENT_SECRET=`az monitor log-analytics workspace get-shared-keys --query primarySharedKey -g $RESOURCE_GROUP -n $LOG_ANALYTICS_WORKSPACE -o tsv | tr -d '[:space:]'`
az extension add \
  --source https://workerappscliextension.blob.core.windows.net/azure-cli-extension/containerapp-0.2.2-py2.py3-none-any.whl
az provider register --namespace Microsoft.Web
az containerapp env create \
  --name $CONTAINERAPPS_ENVIRONMENT \
  --resource-group $RESOURCE_GROUP \
  --logs-workspace-id $LOG_ANALYTICS_WORKSPACE_CLIENT_ID \
  --logs-workspace-key $LOG_ANALYTICS_WORKSPACE_CLIENT_SECRET \
  --location "$LOCATION"
STORAGE_ACCOUNT="gangoghtwitterbot"
az storage account create \
  --name $STORAGE_ACCOUNT \
  --resource-group $RESOURCE_GROUP \
  --location "$LOCATION" \
  --sku Standard_LRS \
  --kind StorageV2
STORAGE_ACCOUNT_KEY=`az storage account keys list --resource-group $RESOURCE_GROUP --account-name $STORAGE_ACCOUNT --query '[0].value' --out tsv`
az acr build -t $CONTAINER_IMAGE_NAME:latest -r $REGISTRY_SERVER ./dotnetc/
az acr build -t $CONTAINER_IMAGE_NAME-follow:latest -r $REGISTRY_SERVER ./python/
REGISTRY_LOGIN_SERVER=`az acr show-endpoints --name $REGISTRY_SERVER --out tsv | tr -d '1[:space:]'`
REGISTRY_USERNAME=`az acr credential show -n $REGISTRY_SERVER --query username --out tsv`
REGISTRY_PASSWORD=`az acr credential show -n $REGISTRY_SERVER --query 'passwords[0].value' --out tsv`
az containerapp create \
  --name twitterbot \
  --resource-group $RESOURCE_GROUP \
  --environment $CONTAINERAPPS_ENVIRONMENT \
  --image  $REGISTRY_LOGIN_SERVER/$CONTAINER_IMAGE_NAME:latest \
  --registry-login-server $REGISTRY_LOGIN_SERVER \
  --registry-username $REGISTRY_USERNAME \
  --registry-password $REGISTRY_PASSWORD \
  --min-replicas 1 \
  --max-replicas 1 \
  --ingress internal \
  --transport http2 \
  --dapr-app-port 5276 \
  --target-port 5276 \
  --cpu 0.25 \
  --memory 0.5Gi \
  --enable-dapr \
  --dapr-app-id twitterbot \
  --dapr-components ./components.yaml \
  --secrets "storage-account-name=${STORAGE_ACCOUNT},storage-account-key=${STORAGE_ACCOUNT_KEY},consumer-key=${CONSUMERKEY},consumer-secret=${CONSUMERSECRET},access-token=${ACCESSTOKEN},access-secret=${ACCESSSECRET}"

az containerapp create \
  --name twitterfollowbot \
  --resource-group $RESOURCE_GROUP \
  --environment $CONTAINERAPPS_ENVIRONMENT \
  --image  $REGISTRY_LOGIN_SERVER/$CONTAINER_IMAGE_NAME-follow:latest \
  --registry-login-server $REGISTRY_LOGIN_SERVER \
  --registry-username $REGISTRY_USERNAME \
  --registry-password $REGISTRY_PASSWORD \
  --min-replicas 1 \
  --max-replicas 1 \
  --ingress internal \
  --transport http2 \
  --dapr-app-port 5000 \
  --target-port 5000 \
  --cpu 0.25 \
  --memory 0.5Gi \
  --enable-dapr \
  --dapr-app-id twitterbot \
  --dapr-components ../components.yaml \
  --environment-variables "CONSUMERKEY=${CONSUMERKEY},CONSUMERSECRET=${CONSUMERSECRET},ACCESSTOKEN=${ACCESSTOKEN},ACCESSSECRET=${ACCESSSECRET}"\
  --secrets "storage-account-name=${STORAGE_ACCOUNT},storage-account-key=${STORAGE_ACCOUNT_KEY},consumer-key=${CONSUMERKEY},consumer-secret=${CONSUMERSECRET},access-token=${ACCESSTOKEN},access-secret=${ACCESSSECRET}"
  


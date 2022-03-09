# dapr-containerapp-sample
Sample dapr app deployed in containerapp

dapr run --app-id twitter-text --app-port 5276 --components-path ../components  -- dotnet run

dapr run --app-id twitter-follow --app-port 5000 --app-protocol http --components-path ../components  -- python3 app.py


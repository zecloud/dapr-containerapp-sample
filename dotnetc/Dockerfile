FROM mcr.microsoft.com/dotnet/sdk:6.0-bullseye-slim AS build-env
WORKDIR /app

# Copy necessary files and restore as distinct layer
COPY dotnetc.fsproj ./
RUN dotnet restore

# Copy everything else and build
COPY . ./
RUN dotnet publish -c Release -o out dotnetc.fsproj

# Build runtime image
FROM mcr.microsoft.com/dotnet/aspnet:6.0-bullseye-slim
COPY --from=build-env /app/out .

# Expose ports
EXPOSE 5276/tcp
ENV ASPNETCORE_URLS http://*:5276

# Start
ENTRYPOINT ["dotnet", "dotnetc.dll"]
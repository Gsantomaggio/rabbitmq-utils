FROM mcr.microsoft.com/dotnet/runtime:7.0 AS base
WORKDIR /app
COPY ["bin/Release/net7.0", "/Caos/"]
ENTRYPOINT ["dotnet", "/Caos/Caos.dll", "test","test","10.44.1.208"]

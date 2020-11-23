# My Account Book Server

## How to Deploy
```sh
# DockerfileではRemote RepositoryのMaster-branchをpullしている
git add .
git commit -m 'make it better.'
git push origin master

# LocalでbuildしたimageをGoogle Container RegistryにPush
docker build -t my-account-book-server . --no-cache
docker tag my-account-book-server asia.gcr.io/my-account-book-bfdeb/my-account-book-server-gcrop
docker push asia.gcr.io/my-account-book-bfdeb/my-account-book-server-gcr

# Google Cloud RunのDeployはGoogle Container RegistryのContainer Imageから行う
gcloud run deploy --image gcr.io/my-account-book-bfdeb/my-account-book-server-gcr --platform managed --project my-account-book
```

または下記より最新のPush済Container Imageを選択してデプロイを実施  
[Cloud Run Deploy](https://console.cloud.google.com/run/deploy/asia-northeast1/my-account-book-server?project=my-account-book-bfdeb)

## How to run locally
```sh
git add .
git commit -m 'make it better.'
git push origin master

docker build -t my-account-book-server . --no-cache
# PORT番号を環境変数として渡す
docker run -dp 8080:8080 -e PORT=8080 my-account-book-server 
```

k


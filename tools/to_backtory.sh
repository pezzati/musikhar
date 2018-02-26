#!/usr/bin/env sh

token=$1
storageID=$2
file=$3
path=$4
#echo "CREATE FOLDER"
#curl -X POST --header "Authorization: Bearer $token" --header "X-Backtory-Storage-Id: $storageID" --header "Content-Type: application/json" -d '{"path" : "/path1/path2/"}' http://storage.backtory.com/directories

echo "UPLOAD THE FILE"
curl -X POST --header "Authorization: Bearer $token" --header "X-Backtory-Storage-Id: $storageID" --form fileItems[0].fileToUpload=@"$file"  --form fileItems[0].path="$path" --form fileItems[0].replacing=true http://storage.backtory.com/files
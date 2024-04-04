
BASE64_IMAGE=$(cat testimage.base64)
curl -X POST localhost:8080/detect -H "Content-Type: application/json" -v -d '{ "image": "'$BASE64_IMAGE'" }'
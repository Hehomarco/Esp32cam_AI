$BASE64_IMAGE = Get-Content testimage.base64
$BODY = @"
{
    "image": "$BASE64_IMAGE"
}
"@
echo $BODY
Invoke-RestMethod -Method Post -Uri "http://localhost:8080/detect" -ContentType "application/json" -Body $BODY
# Detect image 


#### use "pyenv" to manage your local python version
```
pyenv install 3.12.0`
```
#### setup a new virtual environment for this project
```
pyenv local image-detection
pyenv virtualenv 3.12.0 image-detection
````
#### install awscli and configure your security credentials 
```
aws configure
```

## Dependencies:
#### install with "pip3 install -r requirements.txt"

- flask (webserver for receiving POST requests)
- boto3 (aws sdk for textract)
- requests (sending http requests for webhook)
- jurigged (hot reloading for development)

## Run the Webserver
#### Start the webserver with jurigged for development

```
jurigged webserver.py
```
#### Webserver will automatically reload when the code changes and file is saved

## Test locally

### Test with test-image-detection.ps1 or .sh (windows / linux)

import flask;
import boto3;
import base64;
import requests;
import sys; 
import json;

listen_port = 8080
listen_ip = "0.0.0.0" # listen on all interfaces

server = flask.Flask(__name__)


webhook_url = None
aws_access_key_id = None
aws_secret_access_key = None





# check if /data/options.json exists, if so, we are running in home assistant
try:
    with open('/data/options.json') as f:
        content = f.read()
        data = json.loads(content)
        print("Running in Home Assistant")
        
        webhook_url = data['webhook_url']
        aws_access_key_id = data['aws_access_key_id']
        aws_secret_access_key = data['aws_secret_access_key']
except Exception as e:
    print("Error reading options.json: " + str(e))
    sys.exit(1)
except FileNotFoundError:
    print("Running locally")
    positive_text = "betr"
    webhook_url = "http://localhost:8123/api/webhook/your_webhook_id"



def send_telegram_message(text):
    print("sending telegram message: " + text)

def send_webhook(text):
    print("executing webhook: " + text)
    # send POST request to webhook
    response = requests.post(webhook_url, json = {"message": text}) # adjust json as needed for home assistant
    print("webhook response: " + str(response))

@server.route("/")
def get():
    return "running"



# create a post route 
@server.route('/detect', methods=['POST']) 
def post():
    base64_image = None
    try:
        base64_image = flask.request.json['image'] # get image from body as base64

        print("Image received")
        
    except Exception as e:
        return str("Error getting image from body: " + str(e)), 400
    try:
        image = base64.b64decode(base64_image) # decode base64 image
        boto3.setup_default_session(region_name='us-east-1')
        if aws_access_key_id is not None and aws_secret_access_key is not None:
            boto3.setup_default_session(aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name='us-east-1')
        textract = boto3.client('textract') # create textract client
        response = textract.detect_document_text( # detect text in image
            Document={
                'Bytes': image 
            }
        )
        for block in response['Blocks']: # loop through blocks
            if block['BlockType'] == 'LINE': # if block is a line
                text = block['Text'] # get text
                print('Detected: ' + text) # print text
                if text.lower().count("betr") > 0 or text.lower().count("ie") > 0:  # if positive text is in text
                    return "No alert: " + text, 200
                else:
                    # Alert has been detected
                    # use telegram bot to send alert
                    send_telegram_message(text)

                    # send webhook to Home Assistant
                    send_webhook(text)
                    return "ALERT: " + text, 200

    except Exception as e:
        return str("Error processing image: " + str(e)), 500
    return "No text detected", 404

if __name__ == '__main__':
    print("Starting server")
    server.run(host=listen_ip, port=listen_port, debug=True)
    print("Server stopped")

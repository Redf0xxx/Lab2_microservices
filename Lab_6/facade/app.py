import random
import uuid
import requests
import http.client
import pika
from urllib.request import urlopen
from http.client import RemoteDisconnected
from flask import Flask, request
import logging
logging.basicConfig()

app = Flask(__name__)

messager_service_url = "http://localhost:8081"
#logging_service_url = "http://localhost:5705"

@app.route('/facade-service', methods=['GET', 'POST'])
def fac_service():
    if request.method == 'POST':
        return post_request()
    else:
        return get_request()

def get_rand_logging_client():
    r=random.choice(["http://localhost:5711", "http://localhost:5712", "http://localhost:5713"])
    print(r)

    return r
def get_rand_msg_client():
    ran=random.choice(["http://localhost:8081", "http://localhost:8085"])
    print(ran)
    return ran

def get_request():
    print('forward GET-like request to logging service')
    log_response = requests.get(f'{get_rand_logging_client()}/logging-service')
    print('received from logging:', log_response)
    mess_resporse = requests.get(f'{get_rand_msg_client()}/messages')
    print('received from messages:', mess_resporse.content)
    return f'from logging: {str(log_response.text)}, ' \
           f'from messages: {str(mess_resporse.text)}'

def post_msg(msg: str):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()
    channel.queue_declare(queue='queu')
    channel.basic_publish(exchange='', routing_key="queu", body=msg,)
    print(f"Recieve : {msg}")
    connection.close()

def post_request():
    print('forward POST-like request to logging service')
    post_msg(request.json.get('msg'))
    post_log_request = {
        "uuid": str(uuid.uuid4()),
        "msg": request.json.get('msg')
    }
    post_log_response = requests.post(
        f'{get_rand_logging_client()}/logging-service',
        json=post_log_request
    )
    status = post_log_response.status_code
    print('received status from logging:', status)
    return app.response_class(status=status)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082, debug=True)
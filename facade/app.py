import uuid
import requests
from flask import Flask, request

app = Flask(__name__)

messager_service_url = "http://localhost:8081"
logging_service_url = "http://localhost:8080"

@app.route('/facade-service', methods=['GET', 'POST'])
def fac_service():
    if request.method == 'POST':
        return post_request()
    else:
        return get_request()

def get_request():
    print('forward GET-like request to logging service')
    log_response = requests.get(f'{logging_service_url}/logging-service')
    print('received from logging:', log_response)
    mess_resporse = requests.get(f'{messager_service_url}/messages')
    print('received from messages:', mess_resporse.content)
    return f'from logging: {str(log_response.text)}, ' \
           f'from messages: {str(mess_resporse.text)}'

def post_request():
    print('forward POST-like request to logging service')
    post_log_request = {
        "uuid": str(uuid.uuid4()),
        "msg": request.json.get('msg')
    }
    post_log_response = requests.post(
        f'{logging_service_url}/logging-service',
        json=post_log_request
    )
    status = post_log_response.status_code
    print('received status from logging:', status)
    return app.response_class(status=status)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082, debug=True)
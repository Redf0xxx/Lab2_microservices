
from flask import request, Flask

app = Flask(__name__)

messag={}

@app.route('/logging-service', methods=['GET', 'POST'])
def log_service():
    if request.method == 'POST':
        return proc_post_request()
    else:
        return ','.join([msg for msg in messag.values()])


def proc_post_request():
    print(f'RECEIVED request: {request}')
    messag.update({request.json["uuid"]: request.json["msg"]})
    print(f'SAVED to messages')
    return app.response_class(status=200)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

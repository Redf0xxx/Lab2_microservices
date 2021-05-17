
import threading
import pika
from flask import Flask
import logging
logging.basicConfig()


app = Flask(__name__)


@app.route('/messages')
def messages():
    print(msg2)
    return str(msg2)

def thread_rec(target):
    def run(*args, **kwargs):
        threads = threading.Thread(target=target, args=args, kwargs=kwargs)
        threads.start()
        return threads
    return run

@thread_rec
def consume(msg):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost")
    )
    channel = connection.channel()
    channel.queue_declare(queue='queu')

    for method_frame, properties, body in channel.consume('queu'):
        print("[*] Received messages:" % body)
        print('[*] Old: ', msg)

        msg.append(str(body))
        print('[*] New:', msg)

if __name__ == '__main__':
    msg2 = []
    consume(msg2)
    app.run(host='0.0.0.0', port=8085, debug=True)
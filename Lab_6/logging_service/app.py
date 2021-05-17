
from flask import request, Flask
import hazelcast
app = Flask(__name__)

client = hazelcast.HazelcastClient(
        cluster_name="dev",
        cluster_members=[
        "127.0.0.1:5703",
        "127.0.0.1:5704",
        "127.0.0.1:5705",
    ],
    lifecycle_listeners=[lambda state: print("State:", state), ]
)
distributed_map = client.get_map("map")

@app.route('/logging-service', methods=['GET', 'POST'])
def log_service():
    if request.method == 'POST':
        return proc_post_request()
    else:
        return ','.join([msg for msg in distributed_map.values().result()])


def proc_post_request():
    print(f'RECEIVED request: {request}')
    uuid = request.json["uuid"]
    msg = request.json["msg"]
    print("uuid: "+uuid+" "+"msg: "+msg )
    distributed_map.put(uuid, msg)
    print(f'SAVED to messages')
    return app.response_class(status=200)

def proc_get_request():
    distributed_map = client.get_map("map")
    messages = distributed_map.values().result()
    print('[*] Messages:', messages)
    return app.response_class(
    messages=messages
    )
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5711, debug=True)

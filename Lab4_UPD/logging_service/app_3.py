
from flask import request, Flask
import hazelcast
app = Flask(__name__)

client = hazelcast.HazelcastClient(
        cluster_name="dev",
        cluster_members=[
        "192.168.99.100:5703",
        "192.168.99.100:5704",
        "192.168.99.100:5705",
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5712, debug=True)

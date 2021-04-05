
from flask import request, Flask
import hazelcast
app = Flask(__name__)

messag={}


client = hazelcast.HazelcastClient(
        cluster_name="dev",
        cluster_members=[
        "192.168.99.100:5703",
        "192.168.99.100:5704",
        "192.168.99.100:5705",
    ],
    lifecycle_listeners=[lambda state: print("STATE:", state), ]
)

@app.route('/logging-service', methods=['GET', 'POST'])
def log_service():
    if request.method == 'POST':
        return proc_post_request()
    else:
        return ','.join([msg for msg in messag.values()])
distributed_map = client.get_map("map")

def proc_post_request():
    print(f'RECEIVED request: {request}')
    msg = request.json["uuid"]
    uuid = request.json["msg"]
    distributed_map.put(uuid, msg)
    #messag.update({request.json["uuid"]: request.json["msg"]})
    print(f'SAVED to messages')
    return app.response_class(status=200)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5703, debug=True)

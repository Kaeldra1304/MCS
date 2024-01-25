import socket
from subprocess import Popen
from flask import Flask, request, jsonify
app = Flask(__name__)
seed = 0

### TEST command line @ c:/
### curl -X GET http://localhost:5000
@app.route('/', methods=['GET'])
def get_IP():
    return socket.gethostbyname(socket.gethostname())

### TEST command line @ c:/ 
### curl -X POST http://localhost:5000 
@app.route('/', methods=['POST'])
def start_stress():
    #p = Popen("stress_cpu.py")
    p = Popen(['python3', 'stress_cpu.py'])
    return "1"
    
if __name__ == '__main__':
    app.run(port=5000,host='0.0.0.0')
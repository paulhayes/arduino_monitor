import serial.tools.list_ports
from datetime import datetime
import serial
import atexit
import flask
from flask import Response
from multiprocessing import Process, Manager

ports = serial.tools.list_ports.comports()

connections = list()

device_blacklist = ["/dev/ttyAMA0"]

#f = open("record.txt", "a")
manager = Manager()
messages = manager.list()
max_msgs = 500

for p in ports:
    if p.device in device_blacklist:
        continue
    print("connecting to: ".format(p.device))
    connection = serial.Serial(port=p.device)
    connections.append(connection)

def start_server():
    print("starting server");
    app.run(host="0.0.0.0",port=80)

def on_exit():
    print("exiting. Closing file")
    #f.close()
    server.terminate()
    server.join()


atexit.register(on_exit)

app = flask.Flask(__name__)
#app.config["DEBUG"] = True

@app.route('/')
def get_messages():
    return Response("\n".join(messages),mimetype="text/plain")


server = Process(target=start_server)
server.start()

while True:
    for c in connections:
        #print("meep")
        #print( c.in_waiting )
        if c.in_waiting>0:
            dt = datetime.now().strftime("%H:%M %d/%m/%Y")
            msg = "[{1} {2}] {0}".format( c.read(size=c.in_waiting).decode('utf-8').strip(), c.name, dt )
            print( msg )
            #help(c)
            #f.write("[{0}]".format(c.device))
            #f.write( msg )
            messages.insert(0,msg)
            if len(messages) > max_msgs:
                messages.pop()
            





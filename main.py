import serial.tools.list_ports
from datetime import datetime
from time import sleep
import serial
import atexit
import flask
from flask import Response
from multiprocessing import Process, Manager


connections = list()

device_blacklist = ["/dev/ttyAMA0"]

#f = open("record.txt", "a")
manager = Manager()
messages = manager.list()
max_msgs = 500

def find_devices():
    global connections
    ports = serial.tools.list_ports.comports()
    print("looking for devices")
    for c in connections:
        if c.is_open:
            c.close()
    connections = list()
    for p in ports:
        if p.device in device_blacklist:
            continue
        msg = ("connecting to: {0}".format(p.device))
        print(msg)
        messages.insert(0,msg)
        connection = serial.Serial(port=p.device)
        connections.append(connection)

find_devices()

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
    if len(connections) == 0:
        sleep(1)
        find_devices()
    for c in connections:
        #print("meep")
        #print( c.in_waiting )
        try:
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
        except OSError:
            messages.insert(0,"{0} disconnected".format(c.name))
            find_devices()
            





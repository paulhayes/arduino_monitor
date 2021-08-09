import serial.tools.list_ports
from datetime import datetime
import serial
import atexit
import flask
from flask import Response

ports = serial.tools.list_ports.comports()

connections = list()



#f = open("record.txt", "a")

messages = []
max_msgs = 500

for p in ports:
    print(p.device)
    connection = serial.Serial(port=p.device)
    connections.append(connection)

def on_exit():
    print("exiting. Closing file")
    #f.close()

atexit.register(on_exit)

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/index')
def get_messages():
    return Response("\n".join(messages),mimetype="text/plain")

app.run(port=8000)


while True:
    for c in connections:
        #print("meep")
        #print( c.in_waiting )
        if c.in_waiting>0:
            dt = datetime.now().strftime("%H:%M %d/%m/%Y")
            msg = "[{1} {2}] {0}".format( c.read(size=c.in_waiting).decode('utf-8'), c.name, dt )
            print( msg, end="" )
            #help(c)
            #f.write("[{0}]".format(c.device))
            #f.write( msg )
            messages.insert(0,msg)
            if len(messages) > max_msgs:
                messages.pop()
            





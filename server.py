import requests
import json
import socket
import sys
from thread import *
 
HOST = ''   # Symbolic name meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port

LOCATION = 'location1'
BASE_URL = 'https://incandescent-fire-7887.firebaseio.com/'
DATA_URL = BASE_URL + LOCATION + '.json'

r = requests.get(DATA_URL) 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print 'Socket created'
 
#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'
 
#Start listening on socket
s.listen(10)
print 'Socket now listening'

def updateData(data):
    global r
    new_data = r.json()
    if data[0] == 'n':
        new_data['temp'] = float(data[1:])
    if data[0] == 'r':
        new_data['trash'] = float(data[1:])
    r = requests.put(DATA_URL, data=json.dumps(new_data))

#Function for handling connections. This will be used to create threads
def clientthread(conn, addr):
    #Sending message to connected client
    conn.send('Welcome to the server. Type something and hit enter\n') #send only takes string
     
    #infinite loop so that function do not terminate and thread do not end.
    while True:
         
        #Receiving from client
        data = conn.recv(1024)
        reply = 'OK...' + data
        
        if not data: 
            break
        if data == 'exit\r\n':
        	break
        updateData(data)
     
        conn.sendall(reply)
   
    #came out of loop
    conn.close()
    print 'Disconnected with ' + addr[0] + ':' + str(addr[1])
 
#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
     
    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread ,(conn,addr,))
 
s.close()
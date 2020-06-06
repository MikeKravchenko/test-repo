
import socket

from hl7apy.parser import parse_message
from flask import Flask
app = Flask(__name__)

@app.route("/")
def h7query():
    res = query('localhost', 6789) # ,user
    print("Received response: ") #delete me
    return repr(res) 

# route poluchit parametru uzera
# parametry -> funk quire
# paremertu messege

def query(host, port): # ,user
    msg = \
        'MSH|^~\&|REC APP|REC FAC|SEND APP|SEND FAC|20110708163513||QBP^Q22^QBP_Q21|111069|D|2.5|||||ITA||EN\r' \
        'QPD|IHE PDQ Query|111069|@PID.5.2^SMITH||||\r' \
        'RCP|I|'
    # establish the connection
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, port))
        # send the message
        sock.sendall(parse_message(msg).to_mllp().encode('UTF-8'))
        # receive the answer
        received = sock.recv(1024*1024)
        return received
    finally:
        sock.close()


if __name__ == '__main__':
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)
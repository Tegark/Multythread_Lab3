from flask import Flask
import redis 
import zmq
app = Flask(__name__)



@app.route('/')
def index():
        #Establishing container context by initializing sockets
	context = zmq.Context()
	socket = context.socket(zmq.REQ)
	socket.connect("tcp://worker:5555")

	#Initializing connection to database
        dbConn = redis.Redis('redis_db')

        #Appending first numbers to database
        if(int (dbConn.llen("fibNum")) == 0):
                dbConn.rpush("fibNum", 2, 1)
        
	fibNum = int(dbConn.lindex("fibNum", 0))
	m = "Current Fibonacci num  = " + str(fibNum) + " ."

        #Updating Fibonacci number
	socket.send('poking workers...')	
	curFib = socket.recv()
        dbConn.lset("fibNum", 0, curFib)
	dbConn.lset("fibNum", 1, fibNum)
	return m

if __name__ == "__main__":
        app.run(host="0.0.0.0", debug=True)

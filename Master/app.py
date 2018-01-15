from flask import Flask
import redis 
import zmq
app = Flask(__name__)



@app.route('/', methods = ['GET'])
def index():
        

	fibNum = int(dbConn.lindex("fibNum", 0))
	m = "Current Fibonacci num  = " + str(fibNum) + " ."
	return m

@app.route('/', methods = ['POST'])
def increment():
        
        #Establishing container context by initializing sockets
	context = zmq.Context()
	socket = context.socket(zmq.REQ)
	socket.connect("tcp://worker:5555")

        #Updating Fibonacci number
	socket.send('poking workers...')	
	curFib = socket.recv()
        #dbConn.lset("fibNum", 0, curFib)
	#dbConn.lset("fibNum", 1, fibNum)

	return "Increase successful"
	

if __name__ == "__main__":

        #Initializing connection to database
        dbConn = redis.Redis('redis_db')
        try:
                dbConn.ping()
        except redis.ConnectionError:
                print('Connection to database is not established')
        
         #Appending first numbers to database
        if(int (dbConn.llen("fibNum")) == 0):
                dbConn.rpush("fibNum", 2, 1)
     
        app.run(host="0.0.0.0", debug=True)

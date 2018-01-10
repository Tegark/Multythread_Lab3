import redis
import zmq 

def calcFib():
        #Establishing connection to database
	dbConn = redis.Redis('redis_db')

	#Getting last fibonacci number
	fibNum1 = int(dbConn.lindex("fibNum", 1))

	#Getting current fibonacci number 
	fibNum2 = int(dbConn.lindex("fibNum", 0))

	sumFib = fibNum1 + fibNum2
	return str(sumFib)

# Binding worker to net context 
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
        #Receiving poke from master
	poke = socket.recv()

	#Updating fibonacci number 
	curFib = calcFib()
	socket.send(curFib)

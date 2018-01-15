import redis
import zmq 

def calcFib(dbConn):

        pipe = dbConn.pipeline()
        while 1:
                try:
                        print('TRYING TO CALCULATE')
                        pipe.watch("fibNum")
                        #Establishing connection to database
                        #dbConn = redis.Redis('redis_db')

                        #Getting last fibonacci number
                        fibNum1 = int(pipe.lindex("fibNum", 1))

                        #Getting current fibonacci number 
                        fibNum2 = int(pipe.lindex("fibNum", 0))

                        sumFib = fibNum1 + fibNum2

                        print('CALCULATED')
                        
                        pipe.lset("fibNum", 0, sumFib)
                        pipe.lset("fibNum", 1, fibNum2)

                        pipe.execute()
                        break

                except redis.WatchError:
                        continue
                finally:
                        pipe.reset()
                        #return str(sumFib)
        return

# Binding worker to net context
print('BIND WORKER')
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

dbConn = redis.Redis('redis_db')
print('BINDED')
while True:
        #Receiving poke from master
	poke = socket.recv()
        print('RECEIVED POKE FROM MASTER')
	#Updating fibonacci number 
	calcFib(dbConn)
	print('METHOD calcFib executed')
	socket.send('New Fibonacci number calculated')
	print ('SENT ENDMESSAGE')

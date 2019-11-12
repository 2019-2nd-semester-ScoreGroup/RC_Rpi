from socket import *
from time import sleep
import RPi.GPIO as GPIO
#잠금, 속도조절 추가해야함

HIGH = 1
LOW = 0
cnt1 = 50
cnt2 = 50

def setPinNum():
    leftMotar = [19,26]
    rightMotar = [20,21]
    enableButton = [6, 12]

def setGPIO():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(leftMotar[0], GPIO.OUT)
    GPIO.setup(leftMotar[1], GPIO.OUT)
    GPIO.setup(rightMotar[0], GPIO.OUT)
    GPIO.setup(rightMotar[1], GPIO.OUT)

    GPIO.output(leftMotar[0], LOW)
    GPIO.output(leftMotar[1], LOW)
    GPIO.output(rightMotar[0], LOW)
    GPIO.output(rightMotar[1], LOW)

    GPIO.setup(enableButton[0], GPIO.OUT)
    GPIO.setup(enableButton[1], GPIO.OUT)

def setPwm():
    pwm1 = GPIO.PWM(enableButton[0], cnt1)
    pwm2 = GPIO.PWM(enableButton[1], cnt2)

    pwm1.start(cnt1)
    pwm2.start(cnt2)	
	
def connectNet():
    
    #ip = '192.168.43.7'
	ip = input("ip주소를 입력하시오")
    	
    #port = 43566
	port = input("port번호를 입력하시오")

    addr = (ip,port)

    serverSocket = socket(AF_INET, SOCK_STREAM)
	
	try:
        serverSocket.bind(addr)
    except:
        connectNet()
		
    serverSocket.listen(1)
	connectionSocket, connectAddr = serverSocket.accept();
    print("connect")
	
	return connectSocket, serverSocket 

def moving(connectSocket, serverSocket, pwm1, pwm2):	
    try:
        while True:
            cntlFlag = [LOW, LOW, LOW, LOW]
            cntlMsg = connectionSocket.recv(1)
            cntlMsg = cntlMsg.decode('utf-8')
        
            print(cntlMsg)

			if cntlMsg == 'E':
			    close(connectSocket, serverSocket, pwm1, pwm2)
            if cntlMsg == 'L':
                cntlFlag = [LOW, LOW, HIGH, LOW]
            elif cntlMsg == 'R':
                cntlFlag = [HIGH, LOW, LOW, LOW]
            elif cntlMsg == 'F':
                cntlFlag = [HIGH, LOW, HIGH, LOW]
            elif cntlMsg == 'N':
                cntlFlag = [LOW, LOW, LOW, LOW]
            elif cntlMsg == 'B':
                cntlFlag = [LOW, HIGH, LOW, HIGH]
            else:
                changeSpeed(cntlMsg[0])
                
            leftMotarFlag = cntlFlag[0:2]
            rightMotarFlag = cntlFlag[2:4]    
    
            '''
			changeSpeed()
            speed change = pwm1.changeDutyCycle(speed)
            '''
        
            GPIO.output(leftMotar[0], leftMotarFlag[0])
            GPIO.output(leftMotar[1], leftMotarFlag[1])
            GPIO.output(rightMotar[0], rightMotarFlag[0])
            GPIO.output(rightMotar[1], rightMotarFlag[1])
    except:
        continue	

def changeSpeed(speed):
    pwm1.changeDutyCycle(speed)
	
def close():
    connectionSocket.close()
	serverSocket.close()
    pwm1.stop()
	pwm2.stop()
	GPIO.cleanup()
	sys.exit()
	

	

	
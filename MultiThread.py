#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#import socket module
from socket import *
import threading

# 여러 요청을 동시에 처리할 수 있는 멀티스레드 서버를 Threading 모듈을 활용하여 구현한다.
# 각 클라이언트는 clinet_number로 구분한다.
client_number = 1
 
class Thread(threading.Thread):
	#1. init 메소드를 통해 threading.Thread를 초기화한다.    
	def __init__(self, connect, address):   
		threading.Thread.__init__(self)
		self.connectionSocket = connect
		self.addr = address
		
	#2. Thread.start()시 실제로 실행되는 부분을 작성한다.
	def run(self):
		while True:
			try:
				#3. 클라이언트 소켓으로부터 한 번에 최대 1024바이트 크기의 TCP 메시지를 받는다.
				message = connectionSocket.recv(1024)
				if not message:
					break
                    
				#4. 클라이언트 소켓으로부터 받은 메시지를 통해 요청하는 파일 이름을 추출한다.
				filename = message.split()[1]
				f = open(filename[1:])
				outputdata = f.read() 
				print ("outputdata:", outputdata)
				print ("\n")

				#5. 클라이언트에 전송할 서버 응답 메시지에 필요한 헤더 필드를 구성한다.
				first_header = "HTTP/1.0 200 OK"
				header_info = {
					"Content-Length": len(outputdata),
					"Keep-Alive": "timeout=%d,max=%d" %(10,100),
					"Connection": "Keep-Alive",
					"Content-Type": "text/html"
				}
				following_header = "\r\n".join("%s:%s" % (item, header_info[item]) for item in header_info)
                
				#6. 전송할 메시지의 형태는 바이트 스트림으로 제공되어야 하므로, 문자열을 encode()해야한다.
				connectionSocket.send((first_header+"\r\n"+following_header+"r\n\r\n").encode())
				for i in range(0, len(outputdata)):
					connectionSocket.send(outputdata[i].encode())
                    
			except IOError:
				connectionSocket.send(("HTTP/1.0 404 Not Found\r\n\r\n").encode())

if __name__ == '__main__':
	#7. 서버에 대한 정보를 입력하고, 연결에 필요한 소켓을 구성한다.
	serverSocket = socket(AF_INET, SOCK_STREAM) #IPv4(AF_INET) 주소체계를 사용하는 TCP 소켓(SOCK_STREAM) 생성
	server_host = '127.0.0.1' # 서버의 IP 주소 
	server_port = 1756 # 서버의 포트 번호
	serverSocket.bind((server_host,server_port)) # host(IP 주소)와 port(포트 번호)로 소켓을 연결한다.
	serverSocket.listen(5) # 최대 5개의 클라이언트가 순차적으로 접속할 때까지 대기한다.
	threads=[] # 스레드 객체를 저장할 관리 리스트를 선언한다.
    
	#8. 각 요청,응답 쌍에 대해 별도의 스레드와 별도의 TCP 연결을 생성한다.
	while True:
		print ('Ready to serve...')
		connectionSocket, addr = serverSocket.accept() # 연결을 허용하여, connectionSocket 변수에는 클라이언트 소켓이 저장되고 addr에는 클라이언트의 IP 주소를 저장한다.
		print ("Client #",client_number) # 클라이언트 번호를 출력한다.
		client_number += 1 # 클라이언트 번호에 대한 연산을 수행한다.
		print ("addr:\n", addr) # 서버와 연결된 클라이언트의 IP주소 및 포트 번호를 출력한다.
		client_thread = Thread(connectionSocket,addr) # 스레드 객체를 생성한다.
		client_thread.start() # 스레드를 시작한다.
		threads.append(client_thread) # 스레드 객체를 리스트에 저장한다.
        
#9. 서버 소켓을 종료한다.
serverSocket.close()


# In[ ]:





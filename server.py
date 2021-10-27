#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#import socket module
from socket import *
import sys # In order to terminate the program

#IPv4(AF_INET) 주소체계를 사용하는 TCP 소켓(SOCK_STREAM) 생성
serverSocket = socket(AF_INET, SOCK_STREAM) 

#Prepare a sever socket (클라이언트의 접근을 허용하기 위해, 서버 소켓을 준비한다.)
serverSocket.bind(('', 1756)) # host(IP 주소)와 port(포트 번호)로 소켓을 연결한다.
serverSocket.listen(1) # 최대 1개의 클라이언트가 순차적으로 접속할 때까지 대기한다.

while True:
    #Establish the connection
    print ('Ready to serve...')
    connectionSocket, addr = serverSocket.accept() # 연결을 허용하여, connectionSocket 변수에는 클라이언트 소켓이 저장되고 addr에는 클라이언트의 IP 주소를 저장한다.
    try:
        #클라이언트 소켓으로부터 한 번에 최대 1024바이트 크기의 TCP 메시지를 받는다.
        message = connectionSocket.recv(1024)

        #클라이언트 소켓으로부터 받은 메시지를 통해 요청하는 파일 이름을 추출한다.
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.read()
        f.close()
        
        #Send one HTTP header line into socket
        #서버에서 클라이언트 소켓으로 응답 성공 메시지를 전송한다.
        connectionSocket.send('HTTP/1.0 200 OK\r\n\r\n'.encode())
        
        #Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())
        #Close client socket (클라이언트 소켓을 종료한다.)
        connectionSocket.close()
        
    except IOError:
        #Send response message for file not found (파일을 찾지 못했을 때, 응답 메시지를 전송한다.)
        connectionSocket.send('404 Not Found'.encode())
        #Close client socket (클라이언트 소켓을 종료한다.)
        connectionSocket.close()

#Close server socket (서버 소켓을 종료한다.)
serverSocket.close() 
#Terminate the program after sending the corresponding data  (응답 메시지를 전송한 뒤, 프로그램을 종료한다.)
sys.exit() 


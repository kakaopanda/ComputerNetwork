#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from socket import *
import sys

#1. 명령줄 인수 : 서버의 IP주소(argv[1]), 서버가 수신 중인 포트(argv[2]), 서버가 요청할 개체(argv[3]) 설정
# argv[0] -> 항상 프로그램명 혹은 프로그램 실행 경로가 지정된다.
# server_host = sys.argv[1], server_port = sys.argv[2], filename = sys.argv[3]

# 프로그램 검증 상의 편의를 위해, 명령줄 인수로 대입될 값들을 미리 지정하여 사용한다.
server_host = '127.0.0.1'
server_port = 1756
filename = 'HelloWorld.html'
host_port = "%s:%s" %(server_host, server_port)

#2. TCP 연결을 사용하여 서버에 연결한다.
try:
    #IPv4(AF_INET) 주소체계를 사용하는 TCP 소켓(SOCK_STREAM) 생성
	client_socket = socket(AF_INET,SOCK_STREAM)
	client_socket.connect((server_host,int(server_port)))
    
    #3. 서버에 HTTP 요청을 전송한다.
    # filename과 host_port의 값을 추가하여 HTTP 헤더를 정의한다.
	header = {
	"first_header" : "GET /%s HTTP/1.1" %(filename),
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
	"Accept-Language": "en-us",
	"Host": host_port,
	}
	http_header = "\r\n".join("%s:%s" %(item,header[item]) for item in header)
    # 생성된 HTTP 헤더를 출력한다.
	print (http_header)
    
    # 전송할 메시지의 형태는 바이트 스트림으로 제공되어야 하므로, 문자열을 encode()해야한다.
	client_socket.send((http_header+"\r\n\r\n").encode())

except IOError:
	sys.exit(1)
    
#4. 서버 응답을 출력으로 표시한다.
ServerResponse=""
response_message=client_socket.recv(1024)
while response_message:
    # 서버의 응답 메시지(response_message)는  바이트 스트림 형태로 제공되므로, 문자열로 변환하기 위해 decode()해야한다.
	ServerResponse += response_message.decode() 
	response_message = client_socket.recv(1024)

# 문자열로 변환한 서버의 응답 메시지를 출력한다.
print ("ServerResponse:",ServerResponse)

# 클라이언트 소켓을 종료한다.
client_socket.close()


# In[ ]:





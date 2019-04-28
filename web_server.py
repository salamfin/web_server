import socket
import re
import os

server_path = "python_server/"

def read_file(browser,req):
	req_file = re.match(".+/.+H",req).group()[:-2].split("/")[1]
	filename =server_path + re.match(".+/.+H",req).group()[:-2].split("/")[1]
	print(f"[+] - Client Requested File : {filename}")
	try:
		file = open(filename,"r",encoding="utf8")
		if os.path.isdir(filename) != True:
			content_type = file_type(filename)
			if content_type != 1:
				file_contents = file.read()
				write_response(browser,len(file_contents),content_type,file_contents)
				print("[+] - File Founded .")
		else:
			print("else")

	except FileNotFoundError:
		write_error(browser,"404 Not Found")
		print("[+] - File Not Found .")

def file_type(filename):
	ext = ("txt","csv","json","js","css","html")
	headers = ("Content-Type: text/plain","Content-Type: text/html")
	file_ext = filename.split(".")
	for x in range(6):
		if file_ext[-1] != ext[-1]:
			return headers[0]
		elif file_ext[-1] == ext[-1]:
			return headers[-1]
		elif x == len(ext):
			return 1


def write_response(browser,length,content_t,body):
	eol = "\r\n"
	response = "HTTP/1.1 200 OK" + eol
	response += "Content-Length: " + str(length) + eol
	response += content_t + eol + eol
	response += body
	browser.send(response.encode("utf-8"))

def write_error(browser,type):
	file_code = open("python_server/others/404.html","r")
	code = file_code.read()
	file_code.close()
	eol = "\r\n"
	response = "HTTP/1.1 " + type + eol
	response += "Content-Length: 433" + eol
	response += "text/html" + eol + eol
	response += code
	browser.send(response.encode("utf-8"))


port = input("Server Port ? : ")

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print("[+] - Server Starting...")
server.bind(("",int(port)))
print(f"[+] - Listening on port {port}...")
server.listen()
print("[+] - Server Started Successfully...")
print(f"[+] - Server files directory : {server_path}")
while True:
	browser,addr = server.accept()
	headers = browser.recv(1024).decode("utf-8").split("\r\n")
	read_file(browser,headers[0])


	



	

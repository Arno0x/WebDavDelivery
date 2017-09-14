#!/usr/bin/python
# -*- coding: utf8 -*-

import argparse
import socket
from datetime import datetime
import base64
from BaseHTTPServer import BaseHTTPRequestHandler
from StringIO import StringIO

#======================================================================================================
#											HELPERS FUNCTIONS
#======================================================================================================
def color(string, color=None):
    """
    Author: HarmJ0y, borrowed from Empire
    Change text color for the Linux terminal.
    """
    
    attr = []
    
    if color:
        if color.lower() == "red":
            attr.append('31')
        elif color.lower() == "green":
            attr.append('32')
        elif color.lower() == "blue":
            attr.append('34')
        return '\x1b[%sm%s\x1b[0m' % (';'.join(attr), string)

    else:
    	# bold
    	attr.append('1')
        if string.strip().startswith("[!]"):
            attr.append('31')
            return '\x1b[%sm%s\x1b[0m' % (';'.join(attr), string)
        elif string.strip().startswith("[+]"):
            attr.append('32')
            return '\x1b[%sm%s\x1b[0m' % (';'.join(attr), string)
        elif string.strip().startswith("[?]"):
            attr.append('33')
            return '\x1b[%sm%s\x1b[0m' % (';'.join(attr), string)
        elif string.strip().startswith("[*]"):
            attr.append('34')
            return '\x1b[%sm%s\x1b[0m' % (';'.join(attr), string)
        else:
            return string

#------------------------------------------------------------------------
def splitInChunks(s, n):
	"""
	Author: HarmJ0y, borrowed from Empire
	Generator to split a string s into chunks of size n.
	"""
	for i in xrange(0, len(s), n):
		yield s[i:i+n]

#------------------------------------------------------------------------
def b64encode(data):
	return base64.b64encode(data)

#------------------------------------------------------------------------
def httpdate(dt):
    """Return a string representation of a date according to RFC 1123
    (HTTP/1.1).
    The supplied date must be in UTC.
    """

    weekday = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][dt.weekday()]
    month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep",
             "Oct", "Nov", "Dec"][dt.month - 1]
    return "%s, %02d %s %04d %02d:%02d:%02d GMT" % (weekday, dt.day, month, dt.year, dt.hour, dt.minute, dt.second)

#------------------------------------------------------------------------
def webdavdate(dt):

    return "%02d-%02d-%02dT%02d:%02d:%02dZ" % (dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
    
#------------------------------------------------------------------------
def powershellEncode(data):
	"""
	Author: HarmJ0y, borrowed from Empire
	Encode a PowerShell command into a form usable by powershell.exe -enc ...
	"""
	return b64encode("".join([char + "\x00" for char in unicode(data)]))

#------------------------------------------------------------------------
# Class handling WebDav request parsing
#------------------------------------------------------------------------
class WebDavRequest(BaseHTTPRequestHandler):
    def __init__(self, request_text):
        self.rfile = StringIO(request_text)
        self.raw_requestline = self.rfile.readline()
        self.error_code = self.error_message = None
        self.parse_request()

    def send_error(self, code, message):
        self.error_code = code
        self.error_message = message

#------------------------------------------------------------------------
def optionsResponse():

	responseHeader = "HTTP/1.1 200 OK\r\n"
	responseHeader += "Server: nginx/1.6.2\r\n"
	responseHeader += "Date: {}\r\n".format(httpdate(datetime.now()))
	responseHeader += "Content-Length: 0\r\n"
	responseHeader += "DAV: 1\r\n"
	responseHeader += "Allow: GET,HEAD,PUT,DELETE,MKCOL,COPY,MOVE,PROPFIND,OPTIONS\r\n"
	responseHeader += "Proxy-Connection: Close\r\n"
	responseHeader += "Connection: Close\r\n"
	responseHeader += "Age: 0\r\n\r\n"

	return responseHeader

#------------------------------------------------------------------------
def propfindResponse(data=None, encode=True):

	# Get current time
	now = datetime.now().replace(microsecond=0)

	# Prepare the response's body
	body = "<?xml version=\"1.0\" encoding=\"utf-8\" ?>\r\n"
	body += "<D:multistatus xmlns:D=\"DAV:\">\r\n"
	body += "<D:response>\r\n"
	body += "<D:href>/</D:href>\r\n"
	body += "<D:propstat>\r\n"
	body += "<D:prop>\r\n"
	body += "<D:creationdate>{}</D:creationdate>\r\n".format(webdavdate(now))
	body += "<D:displayname></D:displayname>\r\n"
	body += "<D:getcontentlanguage/>\r\n"
	body += "<D:getcontentlength>4096</D:getcontentlength>\r\n"
	body += "<D:getcontenttype/>\r\n"
	body += "<D:getetag/>\r\n"
	body += "<D:getlastmodified>{}</D:getlastmodified>\r\n".format(httpdate(now))
	body += "<D:lockdiscovery/>\r\n"
	body += "<D:resourcetype><D:collection/></D:resourcetype>\r\n"
	body += "<D:source/>\r\n"
	body += "<D:supportedlock/>\r\n"
	body += "</D:prop>\r\n"
	body += "<D:status>HTTP/1.1 200 OK</D:status>\r\n"
	body += "</D:propstat>\r\n"
	body += "</D:response>\r\n"

	if data:
		encodedData = b64encode(data) if encode else data
		
		# Check if the encoded data contains special characters not suited for a 'Windows' filename
		if (encodedData.find('/') != -1):
			encodedData = encodedData.replace('/','_')
		chunks = list(splitInChunks(encodedData, 250))
	
		i = 0
		for chunk in chunks:
			body += "<D:response>\r\n"
			body += "<D:href>/{}</D:href>\r\n".format(chunk)
			body += "<D:propstat>\r\n"
			body += "<D:prop>\r\n"
			body += "<D:creationdate>{}</D:creationdate>\r\n".format(webdavdate(now.replace(minute=(i%59))))
			body += "<D:displayname>{}</D:displayname>\r\n".format(chunk)
			body += "<D:getcontentlanguage/>\r\n"
			body += "<D:getcontentlength>0</D:getcontentlength>\r\n"
			body += "<D:getcontenttype/>\r\n"
			body += "<D:getetag/>\r\n"
			body += "<D:getlastmodified>{}</D:getlastmodified>\r\n".format(httpdate(now.replace(minute=(i%59))))
			body += "<D:lockdiscovery/>\r\n"
			body += "<D:resourcetype/>\r\n"
			body += "<D:source/>\r\n"
			body += "<D:supportedlock/>\r\n"
			body += "</D:prop>\r\n"
			body += "<D:status>HTTP/1.1 200 OK</D:status>\r\n"
			body += "</D:propstat>\r\n"
			body += "</D:response>\r\n"
			i+=1

	body += "</D:multistatus>\r\n"

	responseHeader = "HTTP/1.1 207 Multi-Status\r\n"
	responseHeader += "Server: nginx/1.6.2\r\n"
	responseHeader += "Date: {}\r\n".format(httpdate(datetime.now()))
	responseHeader += "Content-Length: {}\r\n".format(len(body))
	responseHeader += "Proxy-Connection: Keep-Alive\r\n"
	responseHeader += "Connection: Keep-Alive\r\n\r\n"

	return responseHeader + body

#======================================================================================================
#											MAIN FUNCTION
#======================================================================================================
if __name__ == '__main__':
	#------------------------------------------------------------------------
	# Parse arguments
	parser = argparse.ArgumentParser()
	#parser.add_argument("type", help="Type of base64 encoding to be used", choices=['powershell', 'standard'])
	parser.add_argument("-f", "--singleFile", help="Path to the only file to be delivered", dest="singleFile")
	parser.add_argument("-v", "--verbose", help="Path to the only file to be delivered", action="store_true", default=False, dest="verbose")
	args = parser.parse_args() 
	
	#------------------------------------------------------------------------
	# Setup a TCP server listening on port 80
	tcps = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	tcps.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	tcps.bind(('',80))
	tcps.listen(1)
	print color("[*] Pseudo WebDav server listening on port 80")
	print color("[*] Waiting for incoming requests")

	#------------------------------------------------------------------------
	# Main server loop
	try:
		while True:
			connection, clientAddr = tcps.accept()
		
			try:
				print color("[+] Connection received from [{}]".format(clientAddr))
		
				# Receiving request - max size 4096 bytes - should fit any supported WebDav request
				data = connection.recv(4096)

				# Parsing the data received into a proper request object
				request = WebDavRequest(data)
				
				# If there's no error in parsing the data
				if not request.error_code:
					if args.verbose:
						print color("[+] Data received:")
						print color ("{}".format(data),'blue')
					
					#-------------------------- OPTIONS --------------------------
					if request.command == 'OPTIONS':
						response = optionsResponse()
	
					#-------------------------- PROPFIND --------------------------	
					if request.command == 'PROPFIND':
						
						# WebDav client requesting metadata about a directory
						if request.headers['Depth'] == '0':
							response = propfindResponse()
					
						# WebDav client requesting content of a directory
						if request.headers['Depth'] == '1':

							# If the script is supposed to deliver always the same file
							if args.singleFile:
								fileName = args.singleFile
							# Else deliver the file requested in the path
							else:
								fileName = 'servedFiles' + request.path # The directory path is actually the file name requested

							# Read all bytes from the file
							try:
								with open(fileName) as fileHandle:
									fileBytes = bytearray(fileHandle.read())
									fileHandle.close()
									response = propfindResponse(fileBytes)
									print color("[+] Delivering file [{}]".format(fileName))
							except IOError:
								print color("[!] Could not open or read file [{}]".format(fileName))
								response = propfindResponse()

					print color("[+] Sending WebDav response")
					if args.verbose:
						print color("[+] Data sent:")
						print color("{}".format(response),'blue')
					connection.send(response)
			finally:
				connection.close()

	except KeyboardInterrupt:
		pass
	finally:
		print color("[!] Stopping WebDav Server")
		tcps.close()
		

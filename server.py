#  coding: utf-8 
import socketserver
from pathlib import Path  # for checking if files exist

# Copyright 2013 Abram Hindle, Eddie Antonio Santos, Peter Weckend
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        # print ("Got a request of: %s\n" % self.data)
        split_req_data = self.data.decode("utf-8").split('\n')[0].split(' ')
        try:
            inside_slashes = split_req_data[1].split('/')
        except:
            inside_slashes = -1

        response_proto = 'HTTP/1.1 '
        response_status = '200 OK\r\n'
        response_content_type = 'Content-Type: text/html\r\n'  # use html by default
        location = ''

        returned_content = ''

        if split_req_data[0] != 'GET':
            response_status = '405 Method Not Allowed\r\n'
        else:
            # default home page
            if len(inside_slashes) == 2 and split_req_data[1][1:] == '':
                returned_content = self.fetch_content('./www/index.html')

            elif Path('./www/'+split_req_data[1][1:]).is_file() \
                    and (split_req_data[1][-3:] == 'css' or split_req_data[1][-4:] == 'html'):
                returned_content = self.fetch_content('./www/' + split_req_data[1][1:])

                # support css mime type
                if split_req_data[1][-3:] == 'css':
                    response_content_type = 'Content-Type: text/css\r\n'

            # paths ending in /
            elif Path('./www/'+split_req_data[1][1:]).is_dir() and split_req_data[1][1:] != 'etc':

                # if no slash at the end, return a 301 and the address with the slash
                if split_req_data[1][-1] != '/':
                    response_status = '301 Moved Permanently\r\n'
                    location = 'Location: ' + split_req_data[1] + '/' + '\r\n'
                else:
                    returned_content = self.fetch_content('./www/' + split_req_data[1][1:] + "/index.html")

                    # support css mime type
                    if split_req_data[1][-3:] == 'css':
                        response_content_type = 'Content-Type: text/css\r\n'

            else:
                response_status = '404 Not Found\r\n'
                returned_content = '''404 - The page you're looking for could not be found.'''

        response = response_proto + response_status + location + response_content_type + '\r\n' + returned_content + '\r\n'
        self.request.sendall(bytearray(response, 'utf-8'))

    def fetch_content(self, file_path):
        content_file = open(file_path, 'r')
        content_string = ''

        for line in content_file:
            content_string += line

        content_file.close()

        return content_string


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()

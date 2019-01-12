#  coding: utf-8 
import socketserver

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
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
        print ("Got a request of: %s\n" % self.data)
        newData = self.data.decode("utf-8").split('\n')[0].split(' ')
        print(newData)

        newline = '\n'
        response_proto = 'HTTP/1.1 '
        response_status = '200 OK\n'
        response_content_type = 'Content-Type: text/html\n'

        returned_content = ''

        if newData[0] != 'GET':
            response_status = '405 Method Not Allowed\n'

        else:
            if newData[1] == '/' or newData[1][1:] == 'index.html':
                returned_content = self.fetch_content('./www/index.html')

            elif newData[1][1:] == 'base.css':
                response_content_type = 'Content-Type: text/css\n'
                returned_content = self.fetch_content('./www/base.css')

            elif newData[1][1:] in ['deep', 'deep/', 'deep/index.html']:
                returned_content = self.fetch_content('./www/deep/index.html')

            elif newData[1][1:] in ['deep/deep.css']:
                response_content_type = 'Content-Type: text/css\n'
                returned_content = self.fetch_content('./www/deep/deep.css')

            else:
                response_status = '404 Not Found\n'
                returned_content = '''404 - The page you're looking for could not be found.'''

        response = response_proto + response_status + response_content_type + newline + returned_content + '\n'
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

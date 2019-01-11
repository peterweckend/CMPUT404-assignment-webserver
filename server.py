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
        response_status = '200 '
        response_status_text = 'OK\n'
        response_content_type = 'Content-Type: text/html\n'

        html_content = ''

        if newData[0] != 'GET':
            response_status = '405 '
            response_status_text = 'Method Not Allowed\n'
        else:
            if newData[1] == '/' or newData[1][1:] == 'index.html':
                html_file = open('./www/index.html', 'r')

                for line in html_file:
                    html_content += line
            elif newData[1][1:] not in ['deep', 'deep/index.html']:
                response_status = '404 '
                response_status_text = 'Not Found\n'
                html_content = '''404 - The page you're looking for does not exist'''
            elif newData[1][1:] == 'deep':
                html_file = open('./www'+newData[1]+'/index.html', 'r')

                for line in html_file:
                    html_content += line

            elif newData[1][1:] == 'deep/index.html':
                html_file = open('./www' + newData[1], 'r')

                for line in html_file:
                    html_content += line


        response = response_proto + response_status + response_status_text + response_content_type + newline + html_content + '\n'

        self.request.sendall(bytearray(response, 'utf-8'))

        # remember to close html_file


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()

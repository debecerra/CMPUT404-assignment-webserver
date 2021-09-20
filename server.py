#  coding: utf-8
import socketserver
from http_objects import parse_http_request, HttpRequest, HttpResponse

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# Modifications Copyright 2021 Diego Becerra
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

    ROOT_DIR = "www"

    def handle(self):
        self.data = self.request.recv(1024).strip()
        request = parse_http_request(self.data)
        print(request.get_byte_buffer())
        response = self.handle_request(request)
        self.request.sendall(response.get_byte_buffer())

    def handle_request(self, request):
        # Python Software Foundation, "Reading and Writing Files"
        # https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files
        # PSF License Agreement and the Zero-Clause BSD license
        body = self.get_response_body(request)
        headers = self.get_response_headers(request, body)
        return HttpResponse(200, headers, body)

    def get_response_headers(self, request, body):
        headers = {}

        # pawan_asipu, https://auth.geeksforgeeks.org/user/pawan_asipu/articles, "Python String endswith() Method",
        # https://www.geeksforgeeks.org/python-string-endswith-method/, CCBY-SA
        if request.route.endswith(".css"):
            headers["Content-Type"] = "text/css"
        elif request.route.endswith(".html") or request.route.endswith("/"):
            headers["Content-Type"] = "text/html"
        
        headers["Connection"] = "close"

        return headers
            

    def get_response_body(self, request):
        path = self.ROOT_DIR + request.route
        if path[-1] == '/':
            path += "index.html"
        
        # Python Software Foundation, "Reading and Writing Files"
        # https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files
        # PSF License Agreement and the Zero-Clause BSD license
        with open(path, "r") as f:
            data = f.read()

        return data


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()

# Copyright 2021 Diego Becerra

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


HTTP_VERSION = "HTTP/1.1"

# Mozilla Contributors, https://developer.mozilla.org/en-US/docs/MDN/About/contributors.txt,
# "HTTP response status codes", https://developer.mozilla.org/en-US/docs/Web/HTTP/Status,
# 2021-09-10, CC-BY-SA 2.5
RESPONSE_MSG = {
    200: "OK",

    301: "Moved Permanently",

    404: "Not Found",
    405: "Method Not Allowed",

    500: "Internal Server Error"
}


def parse_http_request(payload):
    print("Got a request of: \n%s\n" % payload)

    assert type(payload) is bytes, "Expected byte string for payload"
    lines = payload.decode("utf-8").replace("\r", "").split("\n")
    i = 0

    # parse request line
    (method, request_uri, http_protocol) = lines[i].split()
    assert http_protocol == HTTP_VERSION, f"Expecting {HTTP_VERSION} protocol"
    i += 1

    # parse header fields
    header_fields = {}
    while i < len(lines) and lines[i] != "":
        name, value = lines[i].split(":", 1)
        header_fields[name.strip()] = value.strip()
        i += 1

    # parse body
    body = None
    if i < len(lines):
        body = '\n'.join(lines[i+1:])

    return HttpRequest(method, request_uri, header_fields, body)


class HttpRequest:

    def __init__(self, method, route, headers={}, body=None):
        self.method = method
        self.route = route
        self.headers = headers
        self.body = body

    def get_byte_buffer(self):
        request_line = f"{self.method} {self.route} {HTTP_VERSION}\r\n"
        headers = "" if self.headers == None else "\r\n".join([f"{key}: {value}" for key, value in self.headers.items()]) + "\r\n"
        body = "" if self.body == None else "\r\n" + self.body
        message = request_line + headers + body
        return bytes(message, 'utf-8')


class HttpResponse:

    def __init__(self, status_code, headers={}, body=None):
        self.status_code = status_code
        self.headers = headers
        self.body = body

    def get_byte_buffer(self):
        status_line = f"{HTTP_VERSION} {self.status_code} {RESPONSE_MSG[self.status_code]}\r\n"
        headers = "" if self.headers == None else "\r\n".join([f"{key}: {value}" for key, value in self.headers.items()]) + "\r\n"
        body = "" if self.body == None else "\r\n" + self.body
        message = status_line + headers + body
        return bytes(message, 'utf-8')

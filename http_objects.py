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

def parse_http_request(payload):
    print("Got a request of: \n%s\n" % payload.decode("utf-8"))

    assert type(payload) is bytes, "Expected byte string for payload"
    lines = payload.decode("utf-8").replace("\r", "").split("\n")
    i = 0

    # parse request line
    (method, request_uri, http_protocol) = lines[i].split()
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
        body = '\r\n'.join(lines[i+1:])

    return HttpRequest(method, request_uri, http_protocol, header_fields, body)


class HttpRequest:
    def __init__(self, method, route, protocol, headers, body=None):
        self.method = method
        self.route = route
        self.protocol = protocol
        self.headers = headers
        self.body = body

    def get_method(self):
        return self.method

    def get_route(self):
        return self.route

    def get_header(self, name):
        if name in self.headers:
            return self.headers[name]
        else:
            raise ValueError(f"No header field for {name}")

    def get_body(self):
        return self.body


class HttpResponse():
    def __init__():
        pass

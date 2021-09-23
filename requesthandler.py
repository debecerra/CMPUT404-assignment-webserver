#!/usr/bin/env python
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


import os.path
from http_objects import HttpRequest, HttpResponse
from constants import ROOT_DIR, HOST

class RequestHandler:

    def __init__(self, request):
        if type(request) is not HttpRequest:
            raise ValueError(
                "RequestHandler constructor expected param of type HttpRequest")
        self.request = request

    def handle_request(self):
        try:
            if self.request.method == "GET":
                response = self.__handle_get_request()
            else:
                raise MethodNotAllowed405()

        except MovedPermanently301 as e:
            # return 301 Moved Permanently
            headers = {
                "Location": e.location
            }
            response = HttpResponse(301, headers)

        except NotFound404:
            # return 404 Not Found
            response = HttpResponse(404, {}, "404 Not Found :(")

        except MethodNotAllowed405:
            # return 405 Method Not Allowed
            response = HttpResponse(405)

        except Exception as e:
            # unexpected error
            response = HttpResponse(500)
            print(e)

        finally:
            print(f"Sending the following response:\n{response.get_byte_buffer()}\n")
            return response

    def __handle_get_request(self):
        # do not allow file path outside of www
        if "/.." in self.request.route:
            raise NotFound404()

        body = self.__read_file(self.request.route)
        print(f"Read the following from {self.request.route}: \n{body}")

        headers = self.__generate_OK_response_headers()

        # return 200 OK
        return HttpResponse(200, headers, body)

    def __read_file(self, route):
        relative_path = ROOT_DIR + route
        if relative_path[-1] == '/':
            relative_path += "index.html"

        # ihritik, https://auth.geeksforgeeks.org/user/ihritik/articles, "Python | os.path.isdir() method",
        # https://www.geeksforgeeks.org/python-os-path-isdir-method/, 2019-08-26, CC BY-SA
        print(relative_path)
        if os.path.isdir(relative_path):
            raise MovedPermanently301(f"{HOST}{route}/")

        try:
            # Python Software Foundation, "Reading and Writing Files"
            # https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files
            # PSF License Agreement and the Zero-Clause BSD license
            with open(relative_path, "r") as f:
                data = f.read()

            return data

        except FileNotFoundError:
            raise NotFound404()

    def __generate_OK_response_headers(self):
        headers = {}

        # identify content type for HTML/CSS
        # pawan_asipu, https://auth.geeksforgeeks.org/user/pawan_asipu/articles, "Python String endswith() Method",
        # https://www.geeksforgeeks.org/python-string-endswith-method/, 2021-08-05, CC BY-SA
        if self.request.route.endswith(".css"):
            headers["Content-Type"] = "text/css"
        elif self.request.route.endswith(".html") or self.request.route.endswith("/"):
            headers["Content-Type"] = "text/html"
        else: 
            headers["Content-Type"] = "application/octet-stream"

        headers["Connection"] = "close"

        return headers

# Python Software Foundation, "User-defined Exceptions"
# https://docs.python.org/3/tutorial/errors.html#user-defined-exceptions
# 2021-09-21, PSF License Agreement and the Zero-Clause BSD license

# Parent class for all HttpErrors
class HttpError(Exception):
    pass

# Error for when status code 301 is thrown
class MovedPermanently301(HttpError):

    def __init__(self, location, message=""):
        self.location = location
        self.message = message
        super().__init__(self.message)

# Error for when status code 404 is thrown
class NotFound404(HttpError):
    pass

# Error for when status code 405 is thrown
class MethodNotAllowed405(HttpError):
    pass

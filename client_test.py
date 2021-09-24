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

import requests
from urllib import request

base = "http://127.0.0.1:8080"

# CSS Unit Test
def css_test():
    url = base + "/base.css"
    req = request.urlopen(url, None, 3)
    # Expecting status code 200
    print("Status code:", req.getcode())
    # Expecting content type text/css
    print("Headers: ", req.getheaders())
    print(req.read().decode('utf-8'))


# Root Unit Test
def root_test():
    url = base + "/"
    req = request.urlopen(url, None, 3)
    # Expecting status code 200

# Index Unit Test
def index_test():
    url = base + "/index.html"
    req = request.urlopen(url, None, 3)
    # Expecting status code 200

# Not found error Unit Test
def not_found_test():
    url = base + "/do-not-implement-this-page-it-is-not-found"
    try:
        req = request.urlopen(url, None, 3)
    # Expecting a HTTP error
    except request.HTTPError as e:
        pass
        # Expecting 404 not found

def custom():
    url = base + "/"
    #url = "http://www.google.com" 
    req = request.urlopen(url, None, 3)
    print(req.getcode(), "\n")
    print(req.getheaders(), "\n")
    print(req.read(), "\n")

# Run a test here
custom()

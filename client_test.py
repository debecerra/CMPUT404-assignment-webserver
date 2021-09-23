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
    req = request.urlopen(url, None, 3)
    print(req.getcode(), "\n")
    print(req.getheaders(), "\n")
    print(req.read(), "\n")

custom()

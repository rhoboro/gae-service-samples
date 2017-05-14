#!/usr/bin/env python


class CORSMiddleware:
    def __init__(self):
        pass

    def process_request(self, req, resp):
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header('Access-Control-Allow-Method', 'GET, POST, PUT')
        resp.set_header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept')

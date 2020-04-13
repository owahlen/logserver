#!/usr/bin/env python3

import argparse
import logging
from http.server import BaseHTTPRequestHandler, HTTPServer


class RequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_headers()
        self.wfile.write("<html><body><h1>GET request</h1><p>{}</p></body></html>".format(self.path).encode('utf-8'))

    def do_HEAD(self):
        logging.info("HEAD request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_headers()
        self.wfile.write("<html><body><h1>HEAD request</h1><p>{}</p></body></html>".format(self.path).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        post_data_string = post_data.decode('utf-8')
        logging.info("POST request\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                     str(self.path), str(self.headers), post_data_string)

        self._set_headers()
        self.wfile.write(
            "<html><body><h1>POST request</h1><p>{}</p><p>{}</p></body></html>".format(
                self.path, post_data_string).encode('utf-8')
        )


def run(port=8080):
    server_address = ('', port)
    logserver = HTTPServer(server_address, RequestHandler)
    logging.info("Starting logserver on port {}...\n".format(port))
    try:
        logserver.serve_forever()
    except KeyboardInterrupt:
        pass
    logging.info("Stopping logserver...\n")
    logserver.server_close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("port", nargs='?', type=int, default=8080, help="TCP port to listen on.")
    args = parser.parse_args()
    run(port=args.port)


if __name__ == '__main__':
    logging.basicConfig(format='%(message)s', level=logging.INFO)
    main()

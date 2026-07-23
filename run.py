from http.server import HTTPServer
from router import RequestHandler


def run():
    port = 8000
    server = HTTPServer(('', port), RequestHandler)
    print(f"Server running on http://localhost:{port}")
    server.serve_forever()


if __name__ == '__main__':
    run()

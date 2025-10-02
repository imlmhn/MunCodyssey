import http.server
import socketserver
import time

PORT = 8080


class MyHandler(http.server.SimpleHTTPRequestHandler):
    """
    HTTP 요청을 처리하는 핸들러 클래스.
    """

    def do_GET(self):
        """
        GET 요청을 처리하는 메소드.
        """
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

        # 접속 정보 출력
        client_address, _ = self.client_address
        print(f"접속 시간: {time.ctime()}")
        print(f"접속한 클라이언트의 IP address: {client_address}")

        try:
            with open('2-week2/index.html', 'rb') as file:
                self.wfile.write(file.read())
        except FileNotFoundError:
            self.wfile.write(b"File not found.")


def run_server():
    """
    웹 서버를 실행하는 함수.
    """
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()


if __name__ == '__main__':
    run_server()
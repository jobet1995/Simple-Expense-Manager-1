import http.server
import socketserver
import json

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    expenses = []

    def do_GET(self):
        if self.path == '/get_expenses':
            response = json.dumps(self.expenses)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(response.encode('utf-8'))
        elif self.path == '/':
            self.path = 'templates/index.html' 
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        if self.path == '/add_expense':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            self.expenses.append(data)
            response = {'message': 'Expense added successfully'}
            self.send_response(201)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))

    def do_PUT(self):
        if self.path.startswith('/update_expense/'):
            expense_index = int(self.path.split('/')[-1])
            if 0 <= expense_index < len(self.expenses):
                content_length = int(self.headers['Content-Length'])
                put_data = self.rfile.read(content_length)
                data = json.loads(put_data.decode('utf-8'))
                self.expenses[expense_index] = data
                response = {'message': 'Expense updated successfully'}
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode('utf-8'))
            else:
                self.send_response(404)
                self.end_headers()

    def do_DELETE(self):
        if self.path.startswith('/delete_expense/'):
            expense_index = int(self.path.split('/')[-1])
            if 0 <= expense_index < len(self.expenses):
                del self.expenses[expense_index]
                response = {'message': 'Expense deleted successfully'}
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode('utf-8'))
            else:
                self.send_response(404)
                self.end_headers()

def main():
    PORT = 5000
    with socketserver.TCPServer(("", PORT), MyHttpRequestHandler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    main()
              
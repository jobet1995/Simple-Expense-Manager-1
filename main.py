import sqlite3
from http.server import BaseHTTPRequestHandler, HTTPServer
import json


conn = sqlite3.connect("expense_manager.sqlite")
cursor = conn.cursor()


cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY,
        description TEXT NOT NULL,
        amount REAL NOT NULL,
        date TEXT NOT NULL
    )
""")
conn.commit()

class ExpenseRequestHandler(BaseHTTPRequestHandler):
    def _set_response(self, status_code=200, content_type="application/json"):
        self.send_response(status_code)
        self.send_header("Content-type", content_type)
        self.end_headers()

    def do_GET(self):
        self._set_response()
        cursor.execute("SELECT * FROM expenses")
        expenses = cursor.fetchall()
        response_data = [{"id": row[0], "description": row[1], "amount": row[2], "date": row[3]} for row in expenses]
        self.wfile.write(json.dumps(response_data).encode("utf-8"))

    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        expense_data = json.loads(post_data.decode("utf-8"))

        description = expense_data.get("description")
        amount = expense_data.get("amount")
        date = expense_data.get("date")

        if description is None or amount is None or date is None:
            self._set_response(400)
            return

        try:
            cursor.execute("""
                INSERT INTO expenses (description, amount, date)
                VALUES (?, ?, ?)
            """, (description, amount, date))
            conn.commit()

            self._set_response(201)
            response_message = json.dumps({"message": "Expense added successfully"})
            self.wfile.write(response_message.encode("utf-8"))
        except Exception as e:
            print("Error:", e)
            self._set_response(500)

    def do_PUT(self):
        content_length = int(self.headers["Content-Length"])
        put_data = self.rfile.read(content_length)
        expense_data = json.loads(put_data.decode("utf-8"))

        expense_id = expense_data.get("id")
        description = expense_data.get("description")
        amount = expense_data.get("amount")
        date = expense_data.get("date")

        if expense_id is None or description is None or amount is None or date is None:
            self._set_response(400)
            return

        try:
            cursor.execute("""
                UPDATE expenses
                SET description = ?, amount = ?, date = ?
                WHERE id = ?
            """, (description, amount, date, expense_id))
            conn.commit()

            self._set_response(200)
            response_message = json.dumps({"message": "Expense updated successfully"})
            self.wfile.write(response_message.encode("utf-8"))
        except Exception as e:
            print("Error:", e)
            self._set_response(500)

    def do_DELETE(self):
        content_length = int(self.headers["Content-Length"])
        delete_data = self.rfile.read(content_length)
        expense_data = json.loads(delete_data.decode("utf-8"))

        expense_id = expense_data.get("id")

        if expense_id is None:
            self._set_response(400)
            return

        try:
            cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
            conn.commit()

            self._set_response(200)
            response_message = json.dumps({"message": "Expense deleted successfully"})
            self.wfile.write(response_message.encode("utf-8"))
        except Exception as e:
            print("Error:", e)
            self._set_response(500)

def run(server_class=HTTPServer, handler_class=ExpenseRequestHandler, port=8000):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
      
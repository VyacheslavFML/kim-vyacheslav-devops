"""Small HTTP application for the personalized DevOps laboratory."""
import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer


def student_info():
    return {
        'Name': os.getenv('STUDENT_NAME', 'Vyacheslav'),
        'Surname': os.getenv('STUDENT_SURNAME', 'Kim'),
        'Group': os.getenv('STUDENT_GROUP', 'IT2-2312'),
        'Student ID': os.getenv('STUDENT_ID', '37746'),
    }


def message():
    return ('================================\nDevOps Student Application\n'
            '================================\n\n' +
            '\n'.join(f'{key}: {value}' for key, value in student_info().items()) +
            '\n\nApplication is running successfully!\n')


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            body, content_type = b'{"status":"ok"}', 'application/json'
        elif self.path == '/student':
            body, content_type = json.dumps(student_info()).encode(), 'application/json'
        elif self.path == '/':
            body, content_type = message().encode(), 'text/plain; charset=utf-8'
        else:
            self.send_error(404)
            return
        self.send_response(200)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == '__main__':
    print(message(), flush=True)
    HTTPServer(('0.0.0.0', int(os.getenv('APP_PORT', '8080'))), Handler).serve_forever()

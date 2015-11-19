from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SimpleHTTPServer
import SocketServer
import sys
import dataManager
import json



class MyHttpRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        self.DM = dataManager.DataManager('db',10)
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)

    def do_GET(self):
        rootdir = './pages/' #file location
        try:
            if self.path.endswith('.html'):
                f = open(rootdir + self.path) #open requested file
     
                #send code 200 response
                self.send_response(200)
         
                #send header first
                self.send_header('Content-type','text-html')
                self.end_headers()
         
                #send file content to client
                self.wfile.write(f.read())
                f.close()
        except IOError:
          self.send_error(404, 'file not found')
        return


    def do_POST(self):
        try:
            if self.headers['Content-type'] == "application/json":
                length = int(self.headers['Content-Length'])
                self.send_response(200)
                data  = json.loads(self.rfile.read(length))
                username = data['username']
                encryptedPattern = data['cyphertext']

        except IOError as e:
            self.send_error(str(e))
        pass




if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "Usage: python server.py ip_addr port"
        sys.exit(0)

    print('http server is starting...')
    #ip and port of servr
    server_address = (sys.argv[1], int(sys.argv[2]))
    httpd = HTTPServer(server_address, MyHttpRequestHandler)
    print('http server is running...')
    httpd.serve_forever()
     








from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SimpleHTTPServer
import SocketServer
import sys



class MyHttpRequestHandler(BaseHTTPRequestHandler):
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
                return
          
        except IOError:
          self.send_error(404, 'file not found')


    def do_POST(self):
        if self.headers['Content-type'] == "application/json":
            length = int(self.headers['Content-Length'])
            self.send_response(200)
            print self.rfile.read(length)
        pass




if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "Usage: python server.py ip_addr port"
        sys.exit(0)

    print('http server is starting...')
    #ip and port of servr
    #by default http server port is 80
    server_address = (sys.argv[1], int(sys.argv[2]))
    httpd = HTTPServer(server_address, MyHttpRequestHandler)
    print('http server is running...')
    httpd.serve_forever()
     








from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SimpleHTTPServer
import SocketServer
import sys
import dataManager
import json
from match import match, train



class MyHttpRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        self.DM = dataManager.DataManager('db',10)
        self.count = 0
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
            if self.path.endswith('train.html'):
                if self.headers['Content-type'] == "application/json":
                    length = int(self.headers['Content-Length'])
                    data  = json.loads(self.rfile.read(length))
                    username = data['username']
                     
                    #need decryption
                    pattern = data['ciphertext']


                    #Check user credential


                    #predict
                    model = self.DM.getUserTrainedPattern(username)
                    predict_rlt, similarity = match(pattern, model)

                   
                    #train
                    if predict_rlt:
                        self.DM.insertUserPattern(username, pattern)
                        self.count = self.count+1
                        if self.count >= 10:
                            self.count = 0
                            #retrain and update trainedPattern
                            allPatterns = self.DM.getAllPatterns(username)
                            new_model = train(allPatterns)
                            self.DM.updateUserTrainedPattern(username, new_model)
                    else:
                        pass
                    

                    #send result
                    self.send_response(200)
                    self.send_header('Content-type','text-html')
                    self.end_headers()
                    self.wfile.write("result")



            elif self.path.endswith('auth.html'):
                #create the account
                pass
                

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
     








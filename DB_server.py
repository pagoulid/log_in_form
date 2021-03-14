from DB import db
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
import requests
import hashlib
#from form1 import test

###########Database
info = ["localhost","panosg","%PaGou17846","Mydb"]
tname = 'Links'
db_srv = db(tname,info)

############


class DBHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200,message=None)
       
     # SOS in sign in/sign up HTTP SERVER sends different payloads to the DB SERVER
     #payload ={'uname':name,'hash':h,'salt':salt , 'sign':'sign up'} for sign up
     #payload = {'uname':name,'pswd':hassh,'sign':'sign in'} for sign in
     #SOS payload's pswd in sign in is the hash of the user's passsword so we can check with db.salt if password is correct
     #(see line 64)
     # payload's hash in sign up case is the final hash->(hash(salt+password_hash))  to store it in db  
    def do_POST(self):
        
         values = int(self.headers.get('Content-length', 0))# see self.DBcomm in form1.py
         values = self.rfile.read(values).decode()          # db server handles post requests from http server
         values = parse_qs(values)                          # retrieve informtion from payload HTTP server sends
         
         print('Info from HTTP server :',values) # payload consists of {'uname':name,'pswd':hassh,'sign':'sign in'/'sign up'}
        
         uname =values['uname']
         
         submit=values['sign'] # 
         
         if submit[0]=='sign up':# store info to db
             self.send_response_only(200,message=None) # send response back to HTTP server
             self.end_headers() # works finally!!!! fucking buggggggg
             hash =values['hash']
             salt = values['salt']
             db_srv.c.execute("INSERT INTO {} (name,hash,salt) VALUES ('{}','{}','{}')".format(db_srv.table,uname[0],hash[0],salt[0]))
             db_srv.db.commit()
         else:
             db_srv.c.execute("SELECT * FROM {} WHERE name = '{}' ".format(db_srv.table,uname[0]))
             # retrieve info from db for a given user
             info = db_srv.c.fetchall()
             
             # status  and msg will be stored in db.comm of form1.py
             if len(info)==0:# fetchall returns [] if name dont exist in db
                 self.send_response(404)
                 self.send_header('Content-type', 'text/plain; charset=utf-8')
                 self.end_headers()
                 self.wfile.write('0'.encode())# msg: 0 for non account 1 for non pswd
                 
             else: # to avoid confusion values : info client send , info : info of db 
                 # if user exists check if encrypted password is correct
                info = info[0] # cause : [(name,hash,salt)]
                h=info[1] # db.hash
                s = info[2]# db.salt
                hpswd=values['pswd'] # given.hash passwd
                given_h = hashlib.sha512((s+hpswd[0]).encode('utf-8')).hexdigest()# Bug : order of add is important cause we add 
                #strings (hash(db.salt+given.hash))
                if given_h != h: # compare given hash with db hash
                    self.send_response(404)
                    self.send_header('Content-type', 'text/plain; charset=utf-8')
                    self.end_headers()
                    self.wfile.write('1'.encode())
                else:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/plain; charset=utf-8')
                    self.end_headers()
                    self.wfile.write(given_h.encode())

if __name__ == '__main__' :
   bind = ('',5000)
   srv = HTTPServer(bind,DBHandler)
   srv.serve_forever()
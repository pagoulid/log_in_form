
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
from randtest import SALT
from DB import db
import time
import requests
import hashlib
import random


memory = []
dmem = {}
FAVICO = False
encrypt = hashlib.sha512()
form ='''
<!DOCTYPE html>
<html>
   <form method = "POST">
      <input type='text' id='uname' name='uname'>
      <label for='uname'>Username</label><br>
      <input type='password' id='pswd' name='pswd'>
      <label for='pswd'>Password</label><br>
      
      
     
      <input type='submit'  id ='sign' name = 'sign' value='sign up'><br>
       <input type='submit'  id ='sign' name = 'sign' value='sign in'>
       <pre>
         {}
         </pre>
      </form>
   </html>
   '''


userform = '''
<html lang="en">
<head>
  <meta charset="utf-8">

  <title>The HTML5 Herald</title>
  
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <meta name="description" content="The HTML5 Herald">
  <meta name="author" content="SitePoint">



</head>
<body>
<header class="header-area header-sticky">
   <label>
      <form method = "GET">
         <input name="Logout" type="submit" id="Log out" value="Log out">
         </form>
         </label>

  <div class="container">
      <div class="row">
          <div class="col-12">
              <nav class="main-nav">
                
                  <!-- ***** Menu Start ***** -->
                  <ul class="nav">
                      <li><a href="#welcome" class="active">Home</a></li>
                      <li><a href="#features">About</a></li>
                      <li><a href="#work-process">Work Process</a></li>
                      <li><a href="#testimonials">Testimonials</a></li>
                      <li><a href="#pricing-plans">Pricing Tables</a></li>
                      <li><a href="#blog">Blog Entries</a></li>
                      <li><a href="#contact-us">Contact Us</a></li>
                  </ul>
                  <a class='menu-trigger'>
                      <span>Menu</span>
                  </a>
                  <!-- ***** Menu End ***** -->
              </nav>
          </div>
      </div>
  </div>
</header>
<!-- ***** Header Area End ***** -->
    <!-- ***** Welcome Area Start ***** -->
    <div class="welcome-area" id="welcome">

      <!-- ***** Header Text Start ***** -->
      <div class="header-text">
          <div class="container">
              <div class="row">
                  <div class="offset-xl-3 col-xl-6 offset-lg-2 col-lg-8 col-md-12 col-sm-12">
                      <h1>Welcome {} !!!</h1>
                      <h1>We provide the best <strong>strategy</strong><br>to grow up your <strong>business</strong></h1>
                      <p>Softy Pinko is a professional Bootstrap 4.0 theme designed by Template Mo 
                      for your company at absolutely free of charge</p>
                      <a href="#features" class="main-button-slider">Discover More</a>
                  </div>
              </div>
          </div>
      </div>
      <!-- ***** Header Text End ***** -->
  </div>
  <!-- ***** Welcome Area End ***** -->

</body>


</html>

'''

###########Database
#info = ["localhost","panosg","%PaGou17846","Mydb"]
#tname = 'Links'
#db_srv = db(tname,info)

############

class Handler(BaseHTTPRequestHandler):
   def DBcomm(self,payload): # communication with the database server
      
      s = requests.Session()
                  
      resp = s.post('http://localhost:5000',data = payload)
    
      msg = resp.text # we need msg only to send the pswd if all correct, otherwise 0 for wrong acc and 1 for wrong pswd
      return resp.status_code,s,msg
      
   def getresp(self,resp): # get response
      return resp+''   
   def OK(self): # send just the response
      
      self.send_response(200)
      
   def sign(self,name,pswd):  # Set cookies parameters for user
      self.send_response(200)
      self.send_header("Set-Cookie","UserID = {};\r\n charset=utf-8".format(name))
      self.send_header("Set-Cookie","Password = {};\r\n charset=utf-8".format(pswd))
      self.send_header("Set-Cookie","Path = /;\n charset=utf-8")
      self.send_header('Content-type', 'text/html;\r\n\r\n charset=utf-8')
      self.end_headers()

   def send(self): # sned ok status headers
       
       self.send_response(200)
       self.send_header('Content-type', 'text/html; charset=utf-8')
       self.end_headers()

   def homeredir(self): # send redirection to homepage
      
      self.send_response(303)
      self.send_header('Location','/home')
      self.end_headers()

   def redir(self,name,pswd): # send redirection
      
      self.send_response(303)
      self.send_header('Location','/?uname={}+pswd={}'.format(name,pswd))
      self.end_headers()


   def redirError(self): # send redirection
      
      self.send_response(303)
      self.send_header('Location','/AccErr')
      self.end_headers()
      
      time.sleep(3.0)
    

   def content(self):# returns the query values and the keys of a request
      values = int(self.headers.get('Content-length', 0))
      values = self.rfile.read(values).decode()
      values = parse_qs(values)

      return values.keys(),values
   
   def check(self,index): #checks if both fields are filled (username,password)
      count = 0 
      for i in index:
         if i == 'uname' or i=='pswd': # want to check if in uri we have uname and pswd
            count = count + 1
      if count == 2 :
         return True
      return False



   def do_GET(self):
      global FAVICO
      if self.path == '/favicon.ico':
         
            self.OK() # don't send headers for favicon
           
               

      elif self.path == '/AccErr': 
          
          self.homeredir()
         
      
      elif self.path == '/?Logout=Log+out':
         self.homeredir()

      elif self.path == '/' or self.path == '/home':
        
         self.send()
         
         self.wfile.write(form.encode())
     
      else :
        

         _,user = self.path.split('?')
         user,password = user.split('+')
         _,user = user.split('=')
         _,password = password.split('=') # extract name and pswd from uri path
         self.sign(user,password)     # set cookie
         print(self.headers)
         self.wfile.write(userform.format(user).encode()) # get the username to pass it to the welcome section


   def do_POST(self):
      
      #Our uri after a post request contains query values of uname pswd and sign
      ##################reading values uname pswd sign probably not in get##########
      keys,input = self.content()
     
      checkpoint=self.check(keys)# if both fields are filled then uri  will contain query keys uname and pswd
      submit = input['sign'][0] # sign = sign in or sign up
      
      
      #########################################################################
      if checkpoint :
            name = input['uname'][0]
            pswd = input['pswd'][0]
            hassh = hashlib.sha512(pswd.encode('utf-8')).hexdigest()
            
               #SUBMIT SECTION#
            if submit == 'sign up':
         
              
                  
               salt,h = SALT(hassh) # return  salt and hash(hash(pswd)+salt)
                  
                
                 
                  
               
               payload ={'uname':name,'hash':h,'salt':salt , 'sign':'sign up'}#the data http server will send to db server
               
               
               _,s,_ = self.DBcomm(payload)  # communicate with db to store new user
               
               s.close()
               self.redir(name,hassh)  # redirect to account
            else:
               payload = {'uname':name,'pswd':hassh,'sign':'sign in'}# the hash of the pswd without the salt
               status,s,msg = self.DBcomm(payload)  # communicate with db to store new user
               s.close()
               
               
               print(msg)# msg is 0 if user don't exist, is 1 if user exists but wrong password
                         # else msg is hash to pass it to the query
               if status==404 and msg == '0':# we need status if returns 404 name don't exist in db else returns 200
                  print('Account dont exist!!')   
                  self.redirError() # redirect in account error
               else :
                  
                  if status == 200: # acc exists so either acc verified either the pswd client gives is wrong
                     print("Authentication verified!!")
                     self.redir(name,msg)  # msg is our hash               
                  else:
                     print('Wrong Password')
                     self.homeredir()
                        
               #SUBMIT SECTION#
      else:
         self.homeredir()


        # search or store info in memory and after the redirection


      
      

if __name__ == '__main__' :
   bind = ('',3000)
   srv = HTTPServer(bind,Handler)
   srv.serve_forever()
import mysql.connector as conn
#  CREATE USER 'panosg'@'localhost' IDENTIFIED BY '%PaGou17846'; at mysql
# SELECT user FROM user //to list all users
# port = 3306
#Access mysql via root
# At start of mysql execute : GRANT ALL PRIVILEGES ON *.* TO 'panosg'@'localhost'
#ALWAYS before closing mysql execute GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost'


# [host,user,password,database]

'''
mydb = conn.connect(
  host="localhost",
  user="panosg",        # Added panosg user at mysql
  password="%PaGou17846",
  database = "Mydb"
  
)
'''
class db :
    
    def __init__(self,table,db): # db is a list with the parameters
        self.table = table
        self.db = conn.connect(
            host = db[0],
            user = db[1],
            password = db[2],
            database = db[3]
        )
        self.c = self.db.cursor()
        self.test()
    def check(self):
        self.c.execute("""
            SELECT COUNT(*)
            FROM information_schema.tables
            WHERE table_name = '{0}'
            """.format(self.table.replace('\'', '\'\'')))
        if self.c.fetchone()[0] == 1:
            return True
        return False 
    def test(self):
        exists = self.check()
        if not exists: # if not create the table else do nothing
            self.c.execute("CREATE TABLE {} (name VARCHAR(255), hash VARCHAR(255), salt VARCHAR(255))".format(self.table))
        else:
            print("Table exists!!!!")





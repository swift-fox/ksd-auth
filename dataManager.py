import sqlite3 as db
import json




class DataManager:
    def __init__(self,root, maxRecordNum):
        root = root if root[-1] == '/' else root+'/'
        self.dbfile = root+'project.db'
        self.maxRecordNum = maxRecordNum



    def getUserCredential(self, username):
        try:
            conn = db.connect(self.dbfile)
            cur = conn.cursor()
            cur.execute("SELECT credential FROM users WHERE username = '%s'" % username)
            credential = cur.fetchone()[0]
            conn.close()
        except db.Error as e:
            dme = DataManagerError("Database error while getting user's credential, due to: %s" % e.args[0])
            raise dme
        return credential
    


    def insertUserCredential(self, username, credential):
        try:
            conn = db.connect(self.dbfile)
            cur = conn.cursor()
            cur.execute("INSERT INTO users(username, credential) VALUES('%s', '%s')" % (username, credential))
            conn.commit()
            conn.close()
        except db.Error as e:
            dme = DataManagerError("Database error while inserting user's credential, due to: %s" % e.args[0])
            raise dme



    def insertUserPattern(self, username, pattern):
        try:
            conn = db.connect(self.dbfile)
            cur = conn.cursor()
            if self.maxRecordNum > 0:
                cur.execute('SELECT id FROM patterns')
                totalRowNum = len(cur.fetchall())
                if totalRowNum >= self.maxRecordNum:
                    n = totalRowNum - self.maxRecordNum + 1
                    cur.execute("DELETE FROM patterns WHERE id IN (SELECT id FROM patterns ORDER BY id ASC LIMIT %d)" % n)
            pstr = json.dumps(pattern)
            cur.execute("INSERT INTO patterns(username, pattern) VALUES('%s','%s')" % (username, pstr))
            conn.commit()
            conn.close()
        except db.Error as e:
            dme = DataManagerError("Database error while inserting a new pattern, due to: %s" % e.args[0])
            raise dme



    def getUserTrainedPattern(self, username):
        try:
            conn = db.connect(self.dbfile)
            cur = conn.cursor()
            cur.execute("SELECT trainedPattern FROM users WHERE username = '%s'" % username)
            trainedPattern = cur.fetchone()[0]
            conn.close()
            pass
        except db.Error as e:
            dme = DataManagerError("Database error while getting user's trained pattern , due to: %s" % e.args[0])
            raise dme
        return trainedPattern



    def updateUserTrainedPattern(self, username, pattern):
        try:
            conn = db.connect(self.dbfile)
            cur = conn.cursor()
            cur.execute("UPDATE users SET trainedPattern = '%s' WHERE username = '%s'" % (pattern, username))
            conn.commit()
            conn.close()
            
        except db.Error as e:
            dme = DataManagerError("Database error while updating user's trained pattern, due to: %s" % e.args[0])
            raise dme
        pass



class DataManagerError(Exception):
    def __init__(self, error):
        self.error = error
    
    def __str__(self):
        return repr(self.error)




if __name__ == '__main__':
    M = DataManager('db', 10)
    u1 = 'batman'
    p1 = [[1,2,3],[4,5,6]]
    c1 = 'helloworld'
    
    u2 = 'catwomen'
    p2 = [[4,5,6],[7,8,9]]
    c2 = 'Keep it simple'
    #M.insertUserPattern(u,p)
    #M.insertUserCredential(u2, c2)
    #M.updateUserTrainedPattern(u2, 'hahah')
    print M.getUserCredential(u1)
    print M.getUserCredential(u2)
    print M.getUserTrainedPattern(u1)
    print M.getUserTrainedPattern(u2)


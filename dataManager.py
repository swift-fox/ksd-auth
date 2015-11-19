import sqlite3 as db
import json




class DataManager:
    def __init__(self,root, maxRecordNum):
        root = root if root[-1] == '/' else root+'/'
        self.dbfile = root+'project.db'
        self.maxRecordNum = maxRecordNum



    def getUserCredential(self, username):
        #username is a string
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
        #username is a string, credential is a string
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
        #username is a string, pattern is something like [[...],[...]]
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



    def getAllPatterns(self, username):
        #username is a string, return a list of patterns, where pattern likes [[...],[...]]
        try:
            conn = db.connect(self.dbfile)
            cur = conn.cursor()
            cur.execute("SELECT pattern FROM patterns WHERE username = '%s'" % username)
            data = []
            for r in cur.fetchall():
                data.append(json.loads(r[0]))
        except db.Error as e:
            dme = DataManagerError("Database error while getting user's all patterns , due to: %s" % e.args[0])
            raise dme
        return data



    def getUserTrainedPattern(self, username):
        #username is a string, return pattern like [[...],[...]]
        try:
            conn = db.connect(self.dbfile)
            cur = conn.cursor()
            cur.execute("SELECT trainedPattern FROM users WHERE username = '%s'" % username)
            trainedPattern = json.loads(cur.fetchone()[0])
            conn.close()
            pass
        except db.Error as e:
            dme = DataManagerError("Database error while getting user's trained pattern , due to: %s" % e.args[0])
            raise dme
        return trainedPattern



    def updateUserTrainedPattern(self, username, pattern):
        #username is a string, pattern is something like [[...],[...]]
        try:
            conn = db.connect(self.dbfile)
            cur = conn.cursor()
            pstr = json.dumps(pattern)
            cur.execute("UPDATE users SET trainedPattern = '%s' WHERE username = '%s'" % (pstr, username))
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
    p11 = [[11,12,13],[14,15,16]]
    c1 = 'helloworld'
    
    u2 = 'catwomen'
    p2 = [[4,5,6],[7,8,9]]
    p21 = [[14,15,16],[17,18,19]]
    c2 = 'Keep it simple'
    M.insertUserPattern(u1,p1)
    M.insertUserPattern(u1,p11)
    M.insertUserPattern(u2,p2)
    M.insertUserPattern(u2,p21)
    #M.insertUserCredential(u1, c1)
    #M.insertUserCredential(u2, c2)
    #M.updateUserTrainedPattern(u1, 'balabla')
    #M.updateUserTrainedPattern(u2, 'hahah')
    print M.getUserCredential(u1)
    print M.getUserCredential(u2)
    print M.getUserTrainedPattern(u1)
    print M.getUserTrainedPattern(u2)
    print M.getAllPatterns(u1)


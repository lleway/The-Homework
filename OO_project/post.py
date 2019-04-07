import re
import sqlite3
import time
from actions import db,set_id,now_time
import socket

class IP:
    def __init__(self):
        self.ip = str(socket.gethostbyname(socket.getfqdn(socket.gethostname())))

    def add_ip(self):
        print(self.ip)
        sql = 'insert or ignore into ip(ip) values (\'' + self.ip +'\')'
        conn = db()
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()  # 提交数据库改动
        cursor.close()  # 关闭游标
        conn.close()

    @staticmethod
    def ip():
        return str(socket.gethostbyname(socket.getfqdn(socket.gethostname())))

    def get_ip(self):
        return self.ip

class Author:
    def __init__(self,addr):
        self.addr = addr

    def articlelist(self):
        sql = 'select * from article where address=\''+self.addr+'\''
        conn = db()
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        conn.commit()  # 提交数据库改动
        cursor.close()  # 关闭游标
        conn.close()  # 关闭数据库连接
        return rows

    def commentlist(self):
        sql = 'select * from comment where addr=\'' + self.addr + '\''
        conn = db()
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        conn.commit()  # 提交数据库改动
        cursor.close()  # 关闭游标
        conn.close()  # 关闭数据库连接
        return rows

class Blacklist:
    def __init__(self,address):
        self.address = address

    @staticmethod
    def query():
        sql = "select * from blacklist"
        conn = db()
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        conn.commit()  # 提交数据库改动
        cursor.close()  # 关闭游标
        conn.close()  # 关闭数据库连接
        return rows

    def is_in_blacklist(self):
        conn = db()
        cursor = conn.cursor()
        sql = 'select * from blacklist where address=\''+self.address+'\''
        cursor.execute(sql)
        value = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        if value == []:
            return False
        else:
            return True

class Evil_comment:
    def __init__(self,comment):
        self.comment = comment

    @staticmethod
    def query():
        sql = "select * from evil_comment"
        conn = db()
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        conn.commit()  # 提交数据库改动
        cursor.close()  # 关闭游标
        conn.close()  # 关闭数据库连接
        return rows

    @staticmethod
    def is_evil_comment(comment):
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        sql = 'select * from evil_comment'
        cursor.execute(sql)
        rows = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        flag = False
        for i in rows:
            if i[1] in comment:
                flag = True
        return flag

class Forums(object):
    def __init__(self):
        pass

    @staticmethod
    def query():
        conn = db()
        cursor = conn.cursor()
        sql = 'select * from forums'
        cursor.execute(sql)
        rows = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return rows


    def forum_add(self,subject,introduce):
        conn = db()
        cursor = conn.cursor()
        sql = 'insert into forums(subject,introduce) values (?,?)'
        cursor.execute(sql,(subject,introduce))
        conn.commit()
        cursor.close()
        conn.close()


class Sub_Forums(Forums):
    def __init__(self,subject,introduce,sub_subject):
        self.subject=subject
        self.introduce=introduce
        self.sub_subject=sub_subject

    def query(self):
        sql = 'select * from sub_forums where subject = \''+self.subject+'\''
        conn = db()
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        conn.commit()  # 提交数据库改动
        cursor.close()  # 关闭游标
        conn.close()  # 关闭数据库连接
        return rows

    def sub_forum_add(self):
        sql = 'insert into sub_forums(subject, introduce, sub_subject) values (?,?,?)'
        conn = db()
        cursor = conn.cursor()
        cursor.execute(sql,(self.subject,self.introduce,self.sub_subject))
        conn.commit()  # 提交数据库改动
        cursor.close()  # 关闭游标
        conn.close()  # 关闭数据库连接

    @staticmethod
    def sub_forum_list(a):
        sql = 'select * from sub_forums where subject=\''+a+'\''
        conn = db()
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        l = []
        for row in rows:
            l.append(row[3])
        return l



class Article:
    #,title,address,date,abstract,describle,forum,up
    def __init__(self,id):
        self.id = id

    @staticmethod
    def query(forum):
        sql = "select * from article where forum=\'"+forum+"\'"
        conn = db()
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        conn.commit()  # 提交数据库改动
        cursor.close()  # 关闭游标
        conn.close()  # 关闭数据库连接
        return rows

    @staticmethod
    def time_limit(addr):
        sql = "select * from article where address=\'" + addr + "\'"
        conn = db()
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        conn.commit()  # 提交数据库改动
        cursor.close()  # 关闭游标
        conn.close()  # 关闭数据库连接
        if rows == []:
            return 1
        time = rows[-1][3]
        time = int(re.sub("\D", "", time))
        now = now_time()
        now = int(re.sub("\D", "", now))
        if now-time < 5:
            return 0
        else:
            return 1

    def content(self):
        sql = "select * from article where id=\'" + self.id + "\'"
        conn = db()
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        conn.commit()  # 提交数据库改动
        cursor.close()  # 关闭游标
        conn.close()  # 关闭数据库连接
        return rows

    @staticmethod
    def article_add(title,address,abstract,describle,forum):
        conn = db()
        cursor = conn.cursor()
        id = set_id()
        date = time.strftime("%Y-%m-%d %H:%M", time.localtime())
        sql = 'insert into article(id, title, address, "date", abstract, describe, forum,up,down,times) VALUES (?,?,?,?,?,?,?,0,0,0)'
        cursor.execute(sql,(id,title,address,date,abstract,describle,forum))
        sql = 'insert into article_record(id) values (\'' + id + '\')'
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()


    @staticmethod
    def voted_up(id):
        ip = str(IP.ip())
        conn = db()
        cursor = conn.cursor()
        sql = 'select * from up_record where id=\''+id+'\' and ip=\''+ip+'\''
        cursor.execute(sql)
        rows = cursor.fetchall()
        if rows == []:
            sql = 'update article set up=up+1 where id=\'' + id + '\''
            cursor.execute(sql)
            sql = 'insert into up_record(id, ip) VALUES (?,?)'
            cursor.execute(sql,(id,ip))
        else:
            sql = 'update article set up=up-1 where id=\'' + id + '\''
            cursor.execute(sql)
            sql = 'delete from up_record where id=\''+id+'\' and ip=\''+ip+'\''
            cursor.execute(sql)

        sql = 'select * from article where id = \''+id+'\''
        cursor.execute(sql)
        rows = cursor.fetchall()
        for i in rows:
            upvote = i[7]
        conn.commit()
        cursor.close()
        conn.close()
        return str(upvote)



    @staticmethod
    def voted_down(id):
        ip = str(IP.ip())
        conn = db()
        cursor = conn.cursor()
        sql = 'select * from down_record where id=\'' + id + '\' and ip=\'' + ip + '\''
        cursor.execute(sql)
        rows = cursor.fetchall()
        if rows == []:
            sql = 'update article set down=down+1 where id=\'' + id + '\''
            cursor.execute(sql)
            sql = 'insert into down_record(id, ip) VALUES (?,?)'
            cursor.execute(sql, (id, ip))
        else:
            sql = 'update article set down=down-1 where id=\'' + id + '\''
            cursor.execute(sql)
            sql = 'delete from down_record where id=\'' + id + '\' and ip=\'' + ip + '\''
            cursor.execute(sql)

        sql = 'select * from article where id = \'' + id + '\''
        cursor.execute(sql)
        rows = cursor.fetchall()
        for i in rows:
            upvote = i[8]
        conn.commit()
        cursor.close()
        conn.close()
        return str(upvote)


    def score(self):
        conn = db()
        cursor = conn.cursor()
        sql = 'select * from article where id=\'' + self.id + '\''
        cursor.execute(sql)
        rows = cursor.fetchall()
        row = rows[0]
        score = row[7]*2 - row[8]*2 + row[9]
        sql = 'select count(*) from comment where articleID=\''+self.id+'\''
        cursor.execute(sql)
        num = cursor.fetchall()
        n=int(num[0][0])
        score+=n*3
        conn.commit()
        cursor.close()
        conn.close()
        return score


class Comment:
    def __init__(self,id):
        self.id = id

    @staticmethod
    def addComment(articleID,comment,addr,forum):
        conn = db()
        cursor = conn.cursor()
        time = now_time()
        sql = 'insert into comment(articleID, comment,up,down,addr,forum,time) VALUES (?,?,0,0,?,?,?)'
        cursor.execute(sql,(articleID,comment,addr,forum,time))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def queryComment(articleID):
        conn = db()
        cursor = conn.cursor()
        sql = 'select * from comment where articleID = \''+articleID+'\''
        cursor.execute(sql)
        rows = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return rows

    @staticmethod
    def NumComment(articleID):
        conn = db()
        cursor = conn.cursor()
        sql = 'select * from comment where articleID = \'' + articleID + '\''
        cursor.execute(sql)
        rows = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return len(rows)

    @staticmethod
    def time_limit(addr):
        sql = "select * from comment where addr=\'" + addr + "\'"
        conn = db()
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        conn.commit()  # 提交数据库改动
        cursor.close()  # 关闭游标
        conn.close()  # 关闭数据库连接
        if rows == []:
            return 1
        time = rows[-1][7]
        time = int(re.sub("\D", "", time))
        now = now_time()
        now = int(re.sub("\D", "", now))
        if now - time < 5:
            return 0
        else:
            return 1

    def score(self):
        conn = db()
        cursor = conn.cursor()
        sql = 'select * from comment where id=\'' + self.id + '\''
        cursor.execute(sql)
        rows = cursor.fetchall()
        row = rows[0]
        score = row[3] - row[4]
        conn.commit()
        cursor.close()
        conn.close()
        return score

    @staticmethod
    def voted_up(id):
        ip = str(IP.ip())
        conn = db()
        cursor = conn.cursor()
        sql = 'select * from up_record where id=\'' + id + '\' and ip=\'' + ip + '\''
        cursor.execute(sql)
        rows = cursor.fetchall()
        if rows == []:
            sql = 'update comment set up=up+1 where id=\'' + id + '\''
            cursor.execute(sql)
            sql = 'insert into up_record(id, ip) VALUES (?,?)'
            cursor.execute(sql, (id, ip))
        else:
            sql = 'update comment set up=up-1 where id=\'' + id + '\''
            cursor.execute(sql)
            sql = 'delete from up_record where id=\'' + id + '\' and ip=\'' + ip + '\''
            cursor.execute(sql)
        sql = 'select * from comment where id = \'' + id + '\''
        cursor.execute(sql)
        rows = cursor.fetchall()
        for i in rows:
            upvote = i[3]
        conn.commit()
        cursor.close()
        conn.close()
        return str(upvote)

    @staticmethod
    def voted_down(id):
        ip = str(IP.ip())
        conn = db()
        cursor = conn.cursor()
        sql = 'select * from down_record where id=\'' + id + '\' and ip=\'' + ip + '\''
        cursor.execute(sql)
        rows = cursor.fetchall()
        if rows == []:
            sql = 'update comment set down=down+1 where id=\'' + id + '\''
            cursor.execute(sql)
            sql = 'insert into down_record(id, ip) VALUES (?,?)'
            cursor.execute(sql, (id, ip))
        else:
            sql = 'update comment set down=down-1 where id=\'' + id + '\''
            cursor.execute(sql)
            sql = 'delete from down_record where id=\'' + id + '\' and ip=\'' + ip + '\''
            cursor.execute(sql)

        sql = 'select * from comment where id = \'' + id + '\''
        cursor.execute(sql)
        rows = cursor.fetchall()
        for i in rows:
            upvote = i[4]
        conn.commit()
        cursor.close()
        conn.close()
        return str(upvote)

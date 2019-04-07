import random
import re
import sqlite3
import time
import socket
import Image, ImageDraw, ImageFont, ImageFilter


def db():
    return sqlite3.connect('db.sqlite3')

def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


def is_valid_email(addr):
    if re.match(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$',addr):
        return True
    else :
        return False

def set_id():
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    sql = 'SELECT * from article where id like \'' + time.strftime("%Y%m%d", time.localtime()) + '%\''
    cursor.execute(sql)
    rows = cursor.fetchall()
    if rows == []:
        return time.strftime("%Y%m%d", time.localtime())+'1'
    else:
        id = rows[-1][0]
        new = ''
        f = ''
        for i in range(len(id)):
            if i < 8:
                new += id[i]
            else:
                f += id[i]
        f = int(f) + 1
        new += str(f)
        sql = 'select * from article_record where id = \''+new+'\''
        cursor.execute(sql)
        rows = cursor.fetchall()
        if rows != []:
            new = int(new)+1
            new = str(new)
        conn.commit()
        cursor.close()
        conn.close()
        return new

# 用于判断文件后缀
def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['pdf'])
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def browse(id):
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    ip = get_host_ip()
    sql = 'select * from browse_record where articleID=\''+id+'\' and IP =\''+ip+'\''
    cursor.execute(sql)
    value = cursor.fetchall()
    if value == []:
        sql = 'insert into browse_record(articleID, IP) VALUES (?,?)'
        cursor.execute(sql,(id,ip))
        sql = 'update article set times=times+1 where id=\''+id+'\''
        cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()

def score(id):
    conn = db()
    cursor = conn.cursor()
    sql = 'select * from article where id=\'' + id + '\''
    cursor.execute(sql)
    rows = cursor.fetchall()
    row = rows[0]
    score = row[7] * 2 - row[8] * 2 + row[9]
    sql = 'select count(*) from comment where articleID=\'' + id + '\''
    cursor.execute(sql)
    num = cursor.fetchall()
    n = int(num[0][0])
    score += n * 3
    conn.commit()
    cursor.close()
    conn.close()
    return score

def popularity():
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    sql = 'select * from article'
    cursor.execute(sql)
    rows = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    list = sorted(rows,key=lambda s:(score(s[0])),reverse=True)
    return list





def searchinfo(keyword):
    result = []
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    sql = 'select * from article where title like \'%'+keyword+'%\''
    cursor.execute(sql)
    for i in cursor.fetchall():
        if i not in result:
            result.append(i)
    sql = 'select * from article where abstract like \'%' + keyword + '%\''
    cursor.execute(sql)
    for i in cursor.fetchall():
        if i not in result:
            result.append(i)
    sql = 'select * from article where describe like \'%' + keyword + '%\''
    cursor.execute(sql)
    for i in cursor.fetchall():
        if i not in result:
            result.append(i)
    sql = 'select * from article where address like \'%' + keyword + '%\''
    cursor.execute(sql)
    for i in cursor.fetchall():
        if i not in result:
            result.append(i)

    comments = []
    sql = 'select * from comment where addr like \'%'+keyword+'%\''
    cursor.execute(sql)
    for i in cursor.fetchall():
        if i not in comments:
            comments.append(i)
    sql = 'select * from comment where comment like \'%' + keyword + '%\''
    cursor.execute(sql)
    for i in cursor.fetchall():
        if i not in comments:
            comments.append(i)


    conn.commit()
    cursor.close()
    conn.close()
    return result,comments


def rndChar():
    total = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ012345789'
    return random.choice(total)

def rndColor():
    return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))

def rndColor2():
    return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))

def valid_code():
    # 240 x 60:
    width = 60 * 4
    height = 60
    image = Image.new('RGB', (width, height), (255, 255, 255))
    # 创建Font对象:
    font = ImageFont.truetype('arial.ttf', 36)
    # 创建Draw对象:
    draw = ImageDraw.Draw(image)
    # 填充每个像素:
    for x in range(width):
        for y in range(height):
            draw.point((x, y), fill=rndColor())
    # 输出文字:
    valid = []
    for t in range(4):
        i = rndChar()
        draw.text((60 * t + 10, 10), i, font=font, fill=rndColor2())
        valid.append(i)
    return image,''.join(valid)


def now_time():
    date = time.strftime("%Y-%m-%d %H:%M", time.localtime())
    return date


def repeat(subject):
    sql = 'select * from forums'
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    sql = 'select * from sub_forums'
    cursor.execute(sql)
    rows2 = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    s = ['computer science', 'Computer Science', 'ComputerScience', 'CompSci', 'CS']
    flag = False
    for row in rows:
        if row[1] in s:
            flag = True
    for row in rows2:
        if row[3] in s:
            flag = True
    if flag:
        if subject in s:
            return True
    else:
        return  False

def addr_protect(addr):
    addr = list(addr)
    i = '@'
    n = addr.index(i)
    addr[n - 1] = '*'
    if n >= 3:
        addr[n - 2] = '*'
    if n >= 5:
        addr[n - 3] = '*'
    return ''.join(addr)

def subject_repeat(subject):
    sql = 'select * from forums where subject=\''+subject+'\''
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute(sql)
    rows1 = cursor.fetchall()
    sql = 'select * from sub_forums where sub_subject=\''+subject+'\''
    cursor.execute(sql)
    rows2 = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    if rows1 == [] and rows2 == []:
        return False
    else:
        return True

def exchange(id):
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    sql = 'select * from article where id = \''+id+'\''
    cursor.execute(sql)
    rows = cursor.fetchall()
    row = rows[0]
    conn.commit()
    cursor.close()
    conn.close()
    return str(row[1])

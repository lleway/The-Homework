import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()
print('Do you want change the article or comment?')
i = input('Please enter article or comment:')
if i == 'article':
    print('Article,what do you want? hide or remove?')
    j = input('Please enter hide or remove or recovery:')
    if j == 'hide':
        id = input('Please enter you want modify the article\'s id:')
        sql = 'select * from article where id=\''+id+'\''
        cursor.execute(sql)
        rows = cursor.fetchall()
        if rows == []:
            print('Not exist!')
        else:
            row = rows[0]
            sql = 'insert into hiden_article(id, title, address, "date", abstract, "describe", forum, up, down, times) VALUES (?,?,?,?,?,?,?,?,?,?)'
            cursor.execute(sql,(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9]))
            cursor.execute('delete from article where id=\''+id+'\'')
            print('Hide '+id+' success')
    elif j == 'remove':
        id = input('Please enter you want modify the article\'s id:')
        sql = 'select * from article where id=\'' + id + '\''
        cursor.execute(sql)
        rows = cursor.fetchall()
        sql = 'select * from hiden_article where id=\'' + id + '\''
        cursor.execute(sql)
        rows1 = cursor.fetchall()
        if rows == [] and rows1 == []:
            print('Not exist!')
        else:
            cursor.execute('delete from article where id=\'' + id + '\'')
            cursor.execute('delete from hiden_article where id=\'' + id + '\'')
            print('Remove ' + id + ' success')
    elif j =='recovery':
        id = input('Please enter you want modify the article\'s id:')
        sql = 'select * from hiden_article where id=\'' + id + '\''
        cursor.execute(sql)
        rows = cursor.fetchall()
        if rows == []:
            print('Not exist!')
        else:
            row = rows[0]
            sql = 'insert into article(id, title, address, "date", abstract, "describe", forum, up, down, times) VALUES (?,?,?,?,?,?,?,?,?,?)'
            cursor.execute(sql,(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9]))
            cursor.execute('delete from hiden_article where id=\'' + id + '\'')
            print('Recovery ' + id + ' success')
    else:
        print('Wrong instructions')

elif i == 'comment':
    print('Comment,what do you want? hide , remove or recovery?')
    j = input('Please enter hide or remove or recovery:')
    if j == 'hide':
        id = input('Please enter you want modify the comment\'s id:')
        sql = 'select * from comment where id=\'' + id + '\''
        cursor.execute(sql)
        rows = cursor.fetchall()
        if rows == []:
            print('Not exist!')
        else:
            row = rows[0]
            sql = 'insert into hiden_comment(id, articleID, comment, up, down, addr, forum, "time") values (?,?,?,?,?,?,?,?)'
            cursor.execute(sql, (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
            cursor.execute('delete from comment where id=\'' + id + '\'')
            print('Hide ' + id + ' success')
    elif j == 'remove':
        id = input('Please enter you want modify the comment\'s id:')
        sql = 'select * from comment where id=\'' + id + '\''
        cursor.execute(sql)
        rows = cursor.fetchall()
        sql = 'select * from hiden_comment where id=\'' + id + '\''
        cursor.execute(sql)
        rows1 = cursor.fetchall()
        if rows == [] and rows1 == []:
            print('Not exist!')
        else:
            cursor.execute('delete from comment where id=\'' + id + '\'')
            cursor.execute('delete from hiden_comment where id=\'' + id + '\'')
            print('Remove ' + id + ' success')
    elif j == 'recovery':
        id = input('Please enter you want modify the comment\'s id:')
        sql = 'select * from hiden_comment where id=\'' + id + '\''
        cursor.execute(sql)
        rows = cursor.fetchall()
        if rows == []:
            print('Not exist!')
        else:
            row = rows[0]
            sql = 'insert into comment(id, articleID, comment, up, down, addr, forum, "time") values (?,?,?,?,?,?,?,?)'
            cursor.execute(sql, (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
            cursor.execute('delete from hiden_comment where id=\'' + id + '\'')
            print('Recovery ' + id + ' success')
    else:
        print('Wrong instructions')
else:
    print('Wrong instructions,please re-star!')
conn.commit()
cursor.close()
conn.close()






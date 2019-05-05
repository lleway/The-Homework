import os
import re
from io import BytesIO

from flask import Flask, render_template, redirect, request, url_for, send_from_directory, make_response, session
from werkzeug.utils import secure_filename
from post import Forums,Article,Blacklist,Comment,Author,Evil_comment,IP,Sub_Forums
import actions
# from actions import is_valid_email,set_id,allowed_file,browse,popularity,searchinfo
import time
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024

@app.route('/')
def index():
    ip = IP()
    ip.add_ip()
    f = Forums.query()
    top = actions.popularity()
    article = Article(top[0][0])
    t = list(top[0])
    t.append(actions.addr_protect(t[2]))
    t.append(article.score())
    forums=[]
    for i in f:
        l=list(i)
        l.append(Sub_Forums.sub_forum_list(i[1]))
        forums.append(l)
    return render_template('index.html',forums = forums,top = t)


@app.route('/ip_record',methods=['GET','POST'])
def ip_record():
    list=[]
    for i in IP.getIpList():
        list.append(i)
    return render_template('ip_record.html',list=list);


@app.route('/donation')
def donation():
    return render_template('donation.html')

@app.route('/search',methods=['GET','POST'])
def search():
    if request.method == 'POST':
        keyword = request.form.get('keyword')
        keyword = str(keyword)
        if keyword == '':
            return redirect(url_for('index'))
        result,c= actions.searchinfo(keyword)
        result.reverse()
        b = Blacklist.query()
        blacklist = []
        articles = []
        for i in result:
            article = Article(str(i[0]))
            i = list(i)
            i.append(actions.addr_protect(i[2]))
            i.append(article.score())
            articles.append(i)
        comments = []
        for i in c:
            comment = Comment(str(i[0]))
            i = list(i)
            i.append(actions.addr_protect(i[5]))
            i.append(comment.score())
            i.append(actions.exchange(str(i[1])))
            comments.append(i)
        for i in b:
            blacklist.append(i[1])
        return render_template('search.html',keyword=keyword,articles=articles,blacklist=blacklist,comments=comments)
    else:
        return redirect(url_for('index'))

@app.route('/forum/<forum>')
def forum(forum):
    art = Article.query(forum)
    a = sorted(art,key=lambda s:s[3],reverse=True)
    articles = []
    for i in a:
        article = Article(i[0])
        i = list(i)
        i.append(actions.addr_protect(i[2]))
        i.append(article.score())
        articles.append(i)
    b = Blacklist.query()
    blacklist = []
    for i in b:
        blacklist.append(i[1])
    a1 = sorted(articles,key=lambda s:s[11],reverse=True)
    if a1 == []:
        top=[]
    else:
        top = a1[0]
    return render_template('forum.html',articles = articles,forum=forum,blacklist=blacklist,top=top)

@app.route('/addforum',methods=['GET','POST'])
def add_forum():
    if request.method =='GET':
        return render_template('addforum.html')
    else:
        subject = request.form['subject']
        introduce = request.form.get('introduce')
        if actions.subject_repeat(subject):
            return 'Repeat subject'
        if actions.repeat(subject):
            return 'Repeat subject'
        f = Forums()
        f.forum_add(subject,introduce)
        return redirect(url_for('index'))

@app.route('/AddSubForum',methods=['GET','POST'])
def add_sub_forum():
    if request.method =='GET':
        forum_list=[]
        for i in Forums.query():
            forum_list.append(i[1])
        return render_template('addsubforum.html',forums=forum_list)
    else:
        subject = request.form['subject']
        introduce = request.form.get('introduce')
        sub_subject = request.form.get('sub_subject')
        if actions.subject_repeat(sub_subject):
            return 'Repeat subject'
        if actions.repeat(subject):
            return 'Repeat subject'
        a = Sub_Forums(subject,introduce,sub_subject)
        a.sub_forum_add()
        return redirect(url_for('index'))

@app.route('/author/<address>')
def author(address):
    author = Author(address)
    li = author.articlelist()
    l = sorted(li,key=lambda s:s[3],reverse=True)
    b = Blacklist.query()
    blacklist = []
    for i in b:
        blacklist.append(i[1])
    articles = []
    for i in l:
        article = Article(i[0])
        i = list(i)
        i.append(actions.addr_protect(i[2]))
        i.append(article.score())
        articles.append(i)
    c1 = author.commentlist()
    c = sorted(c1, key=lambda s: s[7], reverse=True)
    comments = []
    for i in c:
        i = list(i)
        i.append(actions.addr_protect(i[5]))
        comments.append(i)
    addr = actions.addr_protect(address)
    return render_template('author.html',articles=articles,addr = addr,blacklist=blacklist,comments=comments)

@app.route('/view_articles/<f>/<id>')
def text(f,id):
    article = Article(id)
    actions.browse(id)
    score = article.score()
    aaa = Article(id)
    a = aaa.content()
    c = Comment.queryComment(id)
    e=Evil_comment.query()
    comments = []
    for i in c:
        flag = True
        for j in e:
            if j[1] in i[2]:
                flag = False
        if flag == True:
            comments.append(i)
    n = len(comments)
    c = []
    for i in comments:
        comment = Comment(str(i[0]))
        i = list(i)
        i.append(actions.addr_protect(i[5]))
        i.append(comment.score())
        c.append(i)
    com = sorted(c,key=lambda s:s[0],reverse=True)
    addr = actions.addr_protect(a[0][2])
    return render_template('article.html',content=a[0],comments = com,num = n,addr=addr,score=score)

@app.route('/vote_up',methods=['GET','POST'])
def voteup():
    if request.method == 'GET':
        id = request.args.get('id')
        id = re.sub("\D", "", id)
        i = Article.voted_up(id)
        a = Article(id)
        score = a.score()
        result = str(i) +','+str(score)
        return result
    else:
        pass

@app.route('/vote_down',methods=['GET','POST'])
def votedown():
    if request.method == 'GET':
        id = request.args.get('id')
        id = re.sub("\D", "", id)
        i = Article.voted_down(id)
        a = Article(id)
        score = a.score()
        result = str(i) + ',' + str(score)
        return result
    else:
        pass

@app.route('/commentvote/vote_up')
def comment_up():
    if request.method == 'GET':
        id = request.args.get('id')
        id = re.sub("\D", "", id)
        i = Comment.voted_up(id)
        c = Comment(id)
        score = c.score()
        result = str(i) + ',' + str(score)
        return result
    else:
        pass

@app.route('/commentvote/vote_down')
def comment_down():
    if request.method == 'GET':
        id = request.args.get('id')
        id = re.sub("\D", "", id)
        i = Comment.voted_down(id)
        c = Comment(id)
        score = c.score()
        result = str(i) + ',' + str(score)
        return result
    else:
        pass

@app.route('/publish/<forum>',methods=['GET','POST'])
def publish(forum):
    if request.method == 'GET':
        return render_template('publish.html',forum = forum)
    else:
        address = request.form.get('address')
        title = request.form.get('title')
        abstract = request.form.get('abstract')
        describe = request.form.get('describe')
        f = request.files['file']

        i = request.form.get('i')
        i = str(i).lower()
        code = str(session.get('code')).lower()

        b = Blacklist(address)
        if b.is_in_blacklist():
            return 'Sorry,you are in black list'
        if actions.is_valid_email(address) == False:
            return 'Please enter valid e-mail'

        if Evil_comment.is_evil_comment(title) == True:
            return 'Evil title! Publish failed'
        if Evil_comment.is_evil_comment(abstract) == True:
            return 'Evil abstract! Publish failed'
        if Evil_comment.is_evil_comment(describe) == True:
            return 'Evil describe! Publish failed'

        if i != code:
            return 'Error Verification Code'

        if Article.time_limit(address) == 0:
            return 'You can not publish a article in a very short period. '
        if address != '' and title != '' and abstract != '' and describe != '':
            if actions.allowed_file(secure_filename(f.filename)) == False:
                return 'You only can upload pdf file! '
            basepath = os.path.dirname(__file__)  # 当前文件所在路径
            filename = actions.set_id()+'.pdf'
            upload_path = os.path.join(basepath, 'static/uploads',filename)
            f.save(upload_path)
            Article.article_add(title, address, abstract, describe, forum)
        else:
            return 'Please enter all information'
        return redirect(url_for('forum', forum=forum))

@app.route('/code')
def get_code():
    image, code = actions.valid_code()
    buf = BytesIO()
    image.save(buf, 'jpeg')
    buf_str = buf.getvalue()
    response = make_response(buf_str)
    response.headers['Content-Type'] = 'image/gif'
    session['code'] = code
    return response


@app.route("/download/<filename>", methods=['GET'])
def download_file(filename):
    filename += '.pdf'
    return send_from_directory('static/uploads', filename, as_attachment=True)

@app.route('/add_comment/<forum>/<articleID>',methods=['POST'])
def add_comment(forum,articleID):
    comment = request.form.get('comment')
    addr = request.form.get('addr')
    if actions.is_valid_email(addr)==False:
        return 'Sorry,it is not valid e-mail'
    b = Blacklist(addr)
    if b.is_in_blacklist():
        return 'Sorry,you are in black list'
    if Evil_comment.is_evil_comment(comment) == True:
        return 'Evil comment! Comment failed'
    if Comment.time_limit(addr) == 0:
        return 'You can not publish a article in a very short period. '
    Comment.addComment(articleID,comment,addr,forum)
    return redirect(url_for('text',f=forum,id=articleID))

if __name__ == '__main__':
    app.run()

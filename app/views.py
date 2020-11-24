from app import app
from flask import Flask, flash, jsonify, redirect, render_template, request, session,jsonify
from models.Model import User,Post,Comment,likes
# from models.posts import Post
import os
from models import db
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
import moment,timeago
import datetime
from functools import wraps
app.config["SECRET_KEY"] = "OCML3BRawWEUeaxcuKHLpw"
app.config["IMAGE_UPLOADS"] ='app/static/upload'
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]


def allowed_image(filename):

    # We only want files with a . in the filename
    if not "." in filename:
        return False

    # Split the extension from the filename
    ext = filename.rsplit(".", 1)[1]

    # Check if the extension is in ALLOWED_IMAGE_EXTENSIONS
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


@app.route('/',methods=['GET','POST'])
def index():
    if request.method == "POST":
 
        if request.files:

            image = request.files["image"]
            if image.filename == "":
                print("No filename")
                flash('no photo','error')
                return redirect(request.url)

            if allowed_image(image.filename):

                filename = secure_filename(image.filename)
                print(filename)
                print(request.form.get("caption"))
                image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
                imagepath='/static/upload/'+filename
                print(imagepath)
                post = Post(caption=request.form.get("caption"), user_id=session.get("user_id"),foto=imagepath)
                db.session.add(post)
                db.session.commit()
                return redirect(request.url)
            else:
                print("That file extension is not allowed")
                flash('That file extension is not allowed','error')
                return redirect(request.url)
    # db.create_all()
    res=Post.query.order_by(Post.id.desc()).limit(10).all()
    
    # print(res.data(session.get("user_id")))
    return render_template('index.html',data=res)
    # print(generate_password_hash("password"))
    # post1=Post.query.filter(Post.id == 1)
    # res=Comments
    # res=Post.query.all()

    # for data in res:

    #     print(data.data(2))

    # if session.get("user_id"):
    #     print("adad")
    # users = User(username='dino', password=generate_password_hash("password"))
    # users2 = User(username='caiyo', password=generate_password_hash("password"))
    # db.session.add(users)
    # db.session.add(users2)
    # db.session.commit()
    # users = User(username='dino', password=generate_password_hash("password"))
    # post2=Post(id=2)
    # result = db.session.execute('select * from user where id=:id',{"id":1})
    # users=User.query.all()
    # print(users[0].posts)
    # res[0].likes.append(users[0])
    # db.session.add(like)
    # db.session.add(post2)
    # db.session.commit()
    # db.create_all()
    # print(users,'coba')
    # print(admin)

    # result = db.session.execute('select * from user where id=:id',{"id":1}).fetchall() //query
    
    # print (result)
    # return render_template('index.html')

@app.route('/like')
def like():
    userid = request.args.get('userid')
    postid = request.args.get('postid')
    post=Post.query.filter(Post.id == postid).first()
    user=User.query.filter(User.id == userid).first()
    print(post)
    print(user)
    post.userlikes.append(user)
    db.session.commit()
    return jsonify({"message":"berhasil","totallike":post.data(userid)["totallike"]})

@app.route('/unlike')
def unlike():
    userid = request.args.get('userid')
    postid = request.args.get('postid')
    post=Post.query.filter(Post.id == postid).first()
    user=User.query.filter(User.id == userid).first()
    print(post)
    print(user)
    post.userlikes.remove(user)
    db.session.commit()
    return jsonify({"message":"berhasil","totallike":post.data(userid)["totallike"]})

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            flash('must have username','error')
            return redirect(request.url)
        # Ensure password was submitted
        elif not request.form.get("password"):
            flash('must have password','error')
            return redirect(request.url)
        
        res=User.query.filter(User.username == request.form.get("username")).all()

        if len(res) != 1 or not check_password_hash(res[0].password, request.form.get("password")):
            flash('pass/username wrong','error')
            return redirect(request.url)
        session["user_id"] = res[0].id
        return redirect('/')
    else:
        if session.get("user_id"):
            return redirect('/')   
        return render_template('login.html')

@app.route("/post/<postid>",methods=['GET','POST'])
def postdetail(postid):
    if request.method == "POST":
        if not request.form.get("comment"):
            flash('must have comment','error')
            return redirect(request.url)
        if not session.get("user_id"):
            flash('harus login','error')
            return redirect(request.url)
        print(request.form.get("comment"))
        userid=session.get("user_id")
        print(userid)
        # post=Post.query.filter(Post.id == postid).first()
        # Comm=Comment(post_id=postid,user_id=userid,comments=request.form.get("comment"))
        # users=User.query.filter(User.id == userid).first()
        # Comm.user = User.query.filter(User.id == userid).first()
        # Comm.user.append(users)
        # p = Post.query.filter(Post.id == postid).first()
        # a = Comment(comments=request.form.get("comment"))
        # a.user = User.query.filter(User.id == 2).first()
        # p.UserComment.append(a)
        # for assoc in p.UserComment:
        #     print(assoc.comments)
        #     print(assoc.user)
        try:
            a = Comment(comments=request.form.get("comment"),user_id=userid,post_id=postid)
            db.session.add(a)
            db.session.commit()
        except IntegrityError:
            print('lewat sini')
            flash('harus contraint','error')
        return redirect(request.url)
    else:
        post=Post.query.filter(Post.id == postid).first()
        result = db.session.execute('select p.username,c.comments,c.created_date from Comment c join user p on p.id =c.user_id where c.post_id=:postid ;',{"postid":postid}).fetchall()
        
        comments=[]
        
        for comment in result:
            tanggal=moment.date(comment["created_date"]).strftime("%Y-%m-%d %H:%M:%S")
            now = datetime.datetime.now()
            comments.append({
                "username":comment.username,
                "comments":comment.comments,
                "created_date":timeago.format(tanggal,now)
            })
            # comment["tanggal"]=timeago.format(tanggal,now)
            # print(timeago.format(tanggal,datetime.datetime.now()))
            # print (timeago.format(tanggal, now))
        print(comments)
        return render_template('postdetail.html',postid=postid,data=post,comments=comments)

@app.route('/user/<iduser>',methods=['GET','POST'])
def UserDetail(iduser):

    if request.method == "POST":
        if request.files:
            image = request.files["image"]
            if image.filename == "":
                print("No filename")
                flash('no photo','error')
                return redirect(request.url)
            if allowed_image(image.filename):
                filename = secure_filename(image.filename)
                print(filename)
                print(request.form.get("caption"))
                image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
                imagepath='/static/upload/'+filename
                print(imagepath)
                post = Post(caption=request.form.get("caption"), user_id=iduser,foto=imagepath)
                db.session.add(post)
                db.session.commit()
                return redirect(request.url)
            else:
                print("That file extension is not allowed")
                flash('That file extension is not allowed','error')
                return redirect(request.url)

    post=Post.query.filter(Post.user_id == iduser).all()
    res=User.query.filter(User.id == iduser).first()
    return render_template('userProfile.html',iduser=iduser,data=post,post=len(post),datauser=res)

@app.route("/passwordchange",methods=['GET','POST'])
@login_required
def PasswordChange():
    return render_template('passwordchange.html')


@app.route("/register",methods=['GET','POST'])
def Register():
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            flash('must have username','error')
            return redirect(request.url)
        # Ensure password was submitted
        elif not request.form.get("password"):
            flash('must have password','error')
            return redirect(request.url)
        elif not request.form.get("confirmation"):
            flash('must have Confirmation','error')
            return redirect(request.url)
        elif request.form.get("confirmation") != request.form.get("password"):
            flash('pass dan confirm harus sama','error')
            return redirect(request.url)      
        usernameuser=request.form.get("username")
        passworduser=request.form.get("password")

        checkres=User.query.filter(User.username == usernameuser).all()
        if len(checkres) > 0 :
            flash('username telah terdaftar','error')
            return redirect(request.url)
        else:
            users = User(username=usernameuser, password=generate_password_hash(passworduser))
            db.session.add(users)
            db.session.commit()
            res=User.query.filter(User.username == usernameuser).all()
            session["user_id"] = res[0].id
            return redirect('/')
    return render_template('register.html')

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")
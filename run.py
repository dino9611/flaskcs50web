# from flask import Flask,render_template
# from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
# from werkzeug.security import check_password_hash, generate_password_hash
# from flask_sqlalchemy import SQLAlchemy
# # from sqlalchemy.tex from text
# from models.User import User 

# app=Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///social.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)


# @app.route('/')
# def index():
#     # print(generate_password_hash("password"))
#     # users = User(username='caiyo', password=generate_password_hash("password"))
#     users=User.query.all()
#     print(type(users[0]),'coba')
#     # db.session.add(users)
#     # db.session.commit()
#     # print(admin)
#     # sql = text()
#     # result = db.session.execute('select * from user where id=:id',{"id":1}).fetchall() //query
    
#     # print (result)
#     return render_template('index.html',data=users[1].username)


# @app.route('/login')
# def login():
#     return render_template('login.html')

from app import app

# if __name__ == "__main__":
#     app.run()

if __name__=="__main__":
    app.run(debug=True)

# def errorhandler(e):
#     """Handle error"""
#     if not isinstance(e, HTTPException):
#         e = InternalServerError()
#     return apology(e.name, e.code)


# Listen for errors
# for code in default_exceptions:
#     app.errorhandler(code)(errorhandler)
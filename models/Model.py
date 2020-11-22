from models import db
from datetime import datetime

likes = db.Table('likes',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)
# Comments = db.Table('Comments',
#     db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True),
#     db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
#     db.Column('commenttext',db.String(50))
# )
class Comment(db.Model):
    __tablename__ = 'Comment'
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), primary_key=True,unique=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True,unique=False)
    comments = db.Column(db.String(100))
    created_date = db.Column(db.DateTime,default=datetime.now,nullable=True)
    # child = relationship("Child")
    posts = db.relationship("Post")
    user = db.relationship("User",backref=db.backref("comment", lazy="joined"), lazy="select")
    def __repr__(self):
        return '<Comment  %r %r %r>' % (self.user_id,self.post_id,self.user)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(120),  nullable=False)
    posts = db.relationship('Post', backref='post')
    prodlikes = db.relationship('Post', secondary=likes,
        backref=db.backref('likes', lazy='dynamic'))
    UserComment = db.relationship('Comment')
    # comment=db.relationship('Comment',backref='Comment')    
    def __repr__(self):
        return '<User %r %r>' % (self.id,self.username)

def checkdata(param,data):
    
    for da in data:
        if da.id == param:
            return True 
    return False

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    caption = db.Column(db.String(80),  nullable=False)
    foto = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
    users = db.relationship('User', backref='user')
    userlikes = db.relationship('User', secondary=likes,
        backref=db.backref('likes', lazy='dynamic'))
    # UserComment = db.relationship('User', secondary=Comments,
    #     backref=db.backref('Comment', lazy='dynamic'))
    UserComment = db.relationship('Comment')
    created_date = db.Column(db.DateTime,
                                    default=datetime.now,
                                    nullable=True)

    def __repr__(self):
        return '<Post %r %r>' % (self.id,self.caption)

    def data(self,a):
 
        return{
            "id":self.id,
            "caption":self.caption,
            "foto":self.foto,
            "users":self.users.username,
            "totallike":len(self.userlikes)  ,
            "userlikes":checkdata(a,self.userlikes ) 
        }

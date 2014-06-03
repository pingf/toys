'''
Created on Jun 2, 2014

@author: jesse
'''

from sqlalchemy import Column, ForeignKey, Integer, String, Text, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'user_alc'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True, index=True)

    def __init__(self,id,name):
        self.id=id
        self.name=name
    def __repr__(self):
        return '<User %d,%r>' % (self.id,self.name)

class Post(Base):
    __tablename__ = 'post_alc'
    id = Column(Integer, primary_key=True)
    title = Column(String(32), unique=True, index=True)
    content = Column(Text())
    user_id = Column(Integer)

    def __init__(self,id,title,content,user_id):
        self.id=id
        self.title=title
        self.content=content
        self.user_id=user_id
    def __repr__(self):
        return '<User %d,%r,%r,%d>' % (self.id,self.title,self.content,self.user_id)

if __name__ == '__main__':
    engine=create_engine('mysql://root@localhost/blog',echo=True) 
    Session = sessionmaker(bind=engine)
    #Session.configure(bind=engine)
    session = Session()
    user = User(1,'jesse')
    session.add(user) 
    session.commit()
    post = Post(1,'hello','world',1)
    session.add(post) 
    session.commit()
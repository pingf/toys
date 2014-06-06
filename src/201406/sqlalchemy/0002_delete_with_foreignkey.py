#coding=utf-8
'''
Created on Jun 2, 2014

@author: jesse
'''

from sqlalchemy import Column, ForeignKey, Integer, String, Text, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=1)
    name = Column(String(64), index=True)
    post = relationship("Post",backref="user")

    def __init__(self,name):
        
        self.name=name
    def __repr__(self):
        return '<User %d,%r>' % (self.id,self.name)

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True, autoincrement=1)
    title = Column(String(32), index=True)
    content = Column(Text())
    user_id = Column(Integer, ForeignKey('user.id',onupdate="CASCADE", ondelete="CASCADE"))
    
    #user = relationship("User",backref="post")
    #前面用backref定义过了,后面就不需要了,relation是让alchemy知道从一个实例中如何查找另一个表中与之匹配的元素
    #好像描述不太好....语文是政治老湿教的,sigh
    def __init__(self,title,content,user_id): 
        self.title=title
        self.content=content
        self.user_id=user_id
    def __repr__(self):
        return '<Post %d,%r,%r,%d>' % (self.id,self.title,self.content,self.user_id)

if __name__ == '__main__':
    engine=create_engine('mysql://root@localhost/blog',echo=False) 
    #Base.metadata.create_all(engine)
    
    Post.__table__.drop(engine,checkfirst=True)
    User.__table__.drop(engine,checkfirst=True)
    User.__table__.create(engine,checkfirst=False)
    Post.__table__.create(engine,checkfirst=False)
    Session = sessionmaker(bind=engine)
    #Session.configure(bind=engine)
    session = Session()
    #session.autoflush = False
    users = [User('jesse'),User('jessie'),User('john'),User('josh')]
    for user in users:
        session.add(user) 
 
    session.commit()#如果不commit,下面的id都是空了
    posts = [Post('hello1','world1',users[0].id),
             Post('hello2','world2',users[0].id),
             Post('hello1','world1',users[1].id),
             Post('hello2','world2',users[1].id),
             Post('hello1','world1',users[2].id),
             Post('hello2','world2',users[2].id),
             Post('hello1','world1',users[2].id),
             Post('hello2','world2',users[2].id),]
    
    session.add_all(posts)
     
    session.commit()
    
    user2=session.query(User).filter_by(id=2)
    a = session.query(Post).all()
    
    
    print 'before ',a
    user2.delete()
    session.commit() #如果木有commit,查询的是session缓存的,数据库里不会变滴
    #另外session的flush是刷缓存的,commit是刷到库里的
    a = session.query(Post).all()
    print 'delete ',a
 
# -*- coding: utf-8 -*-

from app import db
from app.models import User, Party

db.drop_all() #added drop all so it wont duplicate anything every db_creation.
db.create_all()
db.session.commit()

admon = User(123456,'tomer', 'admon',False)
tomer = User(1234567,u'תומר', u'אדמון',False)
mark = User(321894925,'Mark','Davydov',False)
max = User(316946540, 'Maxim','Zhuravsky',False)
edi = User(307218214,'Eduard', 'Medvednic',False)


avoda = Party(u'העבודה', 'static/images/avoda.jpg',0)
likud = Party(u'הליכוד', 'static/images/likud.png',0)
lavan = Party(u'פתק לבן', 'static/images/white.jpg',0)
yarok = Party(u'עלה ירוק','static/images/yarok.jpeg',0)

db.session.add(avoda)
db.session.add(likud)
db.session.add(lavan)
db.session.add(yarok)
db.session.add(admon)
db.session.add(tomer)
db.session.add(mark)
db.session.add(max)
db.session.add(edi)
db.session.commit()
users = User.query.all()
#print users

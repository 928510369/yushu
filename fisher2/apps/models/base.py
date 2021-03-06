from datetime import datetime
from contextlib import contextmanager

from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery
from sqlalchemy import Column, SmallInteger, Integer
from sqlalchemy import text


class SQLAlchemy(_SQLAlchemy):

    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e


class Query(BaseQuery):
    def filter_by(self, **kwargs):
        if "status" not in kwargs.keys():
            kwargs["status"]=1
        return super(Query,self).filter_by(**kwargs)

db=SQLAlchemy(query_class=Query)

class Base(db.Model):
    __abstract__=True
    status=Column(SmallInteger,server_default=text("1"))#default设置默认值失败
    create_time=Column("create_time",Integer)

    def __init__(self):
        self.create_time=int(datetime.now().timestamp())

    def set_attrs(self,attr_dict):
        for k,v in attr_dict.items():
            if hasattr(self,k) and k!="id":
                setattr(self,k,v)


    @property
    def create_datatime(self):
        if self.create_time:
            return datetime.fromtimestamp(self.create_time)
        else:
            return None

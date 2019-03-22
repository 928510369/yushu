from sqlalchemy import Integer, Column, String, Boolean

from apps.models.base import Base


class Test(Base):
    id=Column(Integer,primary_key=True)

    ssss=Column(Boolean,default=False)
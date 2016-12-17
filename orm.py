import db_utils
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sqla

Base = declarative_base()

class Source(Base):
    __tablename__ = 'sources'
    url = sqla.Column(sqla.String(2048),primary_key=True)
    name = sqla.Column(sqla.Text) #display name for the source
    active = sqla.Column(sqla.Boolean) #Should we scrape the source?

    def repr(self):
        return "<Source(url={})>".format(url)

class Article(Base):
    __tablename__ = 'articles'
    id = sqla.Column(sqla.Integer,primary_key=True)
    url = sqla.Column(sqla.String)
    source = sqla.Column(sqla.String(2048), sqla.ForeignKey('sources.url'))
    title = sqla.Column(sqla.types.Unicode())
    date_added = sqla.Column(sqla.types.DateTime())
    date_written = sqla.Column(sqla.types.DateTime())
    raw = sqla.Column(sqla.types.Unicode())
    text = sqla.Column(sqla.types.Unicode())
    summary = sqla.Column(sqla.types.Unicode())
    
    def repr(self):
        return "<Article(url={})>".format(url)
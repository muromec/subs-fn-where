from google.appengine.ext import db
from tipfy.ext.db import JsonProperty
from aetycoon import TransformProperty

from util import get_starts

class Title(db.Model):
  name = db.StringProperty()
  subbers = db.StringListProperty(default=[])
  show = db.BooleanProperty(default=False)

  def __init__(self, *a, **kw):
    super(Title, self).__init__(
        key_name=kw.get("name"), 
        *a, **kw)

  def key(self):
    return db.Key.from_path(self.kind(), self.name)

class TitleHint(db.Model):
  name = db.StringProperty()

  start = TransformProperty(name, get_starts)

  def __init__(self, *a, **kw):
    super(TitleHint, self).__init__(
        key_name=kw.get("name"),
        *a, **kw)


class Ep(db.Model):

  def __init__(self, *a, **kw):
    uniq = kw.get('link') or "%s/%s" % (kw['subber'], kw['number'] )

    key = db.Key.from_path(
        Title.kind(), kw['title'],
        self.kind(), uniq
    )

    if 'key' not in kw:
      kw['key'] = key

    super(Ep, self).__init__(*a, **kw)


  title = db.StringProperty()
  subber = db.StringProperty()
  number = db.IntegerProperty()
  link = db.StringProperty()
  encoded = db.StringListProperty()

  date_modify = db.DateTimeProperty( auto_now_add=True )

class Rename(db.Model):
  name = db.StringProperty()
  typs = db.StringListProperty()

class Drop(db.Model):
  owner = db.StringProperty()
  data = db.ListProperty(db.Key, default=[])

  @classmethod
  def load(cls, email):
    ent = cls.get_by_key_name(email)

    if not ent:
      ent = cls(owner=email, key_name=email)

    return ent

class Token(db.Model):
  owner = db.StringProperty()

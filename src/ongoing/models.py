from google.appengine.ext import db

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

class Ep(db.Model):

  def __init__(self, *a, **kw):
    key = db.Key.from_path(
        Title.kind(), kw['title'],
        self.kind(), "%s/%s" % (kw['subber'], kw['number'])
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

from google.appengine.ext import db
from google.appengine.ext import deferred

from tipfy import RequestHandler, Response

from models import Title, Ep, Rename

class Fix(RequestHandler):
  def get(self):
    deferred.defer(fix)

    return Response("nua")


def fix(cursor=None):
  ttq = Title.all()
  ttq.with_cursor(cursor)

  title = ttq.get()

  if not title:
    return

  rename = Rename.get_by_key_name(title.name)

  if rename:
    if rename.name != title.key().name():
      title_r = Title(name=rename.name, 
          show=title.show,
          subbers = title.subbers)
      deferred.defer(fix_ep, title.key(), rename.name)

      title_r.put()
      title.delete()

    if rename.name == rename.key().name():
      rename.delete()



  deferred.defer(fix, ttq.cursor())



def fix_ep(parent, title):
  epq = Ep.all()
  epq.ancestor(parent)

  for ep in epq:
    kw = dict(ep._entity)
    kw['title'] = title

    ep_r = Ep(
        title=title, 
        subber=ep.subber,
        number = ep.number,
        link = ep.link,
        encoded = ep.encoded )

    ep_r.put()
    ep.delete()


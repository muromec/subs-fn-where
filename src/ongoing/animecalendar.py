import urllib
import re

from google.appengine.ext import deferred

from tipfy import Response, RequestHandler
from models import Title

title_re = re.compile(r'(disable">|) <a href="/show/[0-9]+/.*">(.*)</a>') 


class Import(RequestHandler):
  def get(self):

    remote = urllib.urlopen('http://www.animecalendar.net/shows/list/all')

    titles = re.findall(title_re, remote.read())
    titles = [ (bool(d),t.decode('utf8')) for d,t in titles]
    deferred.defer(titles_update, titles)

    return Response("nom-nom-nom")

def titles_update(titles):
  mode,t = titles.pop()

  title_db = Title.get_by_key_name(t)

  if title_db:
    title_db.show = mode
    title_db.put()

  if not titles:
    return

  deferred.defer(titles_update, titles)



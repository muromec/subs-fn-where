import logging
from google.appengine.ext import db
from google.appengine.ext import deferred

from tipfy import RequestHandler, Response, Forbidden, NotFound
from tipfy.ext.jinja2 import render_response
import uplinks
import models

class Index(RequestHandler):
  MAX_T = 20

  def get(self, start_from=None):
    titles = models.Title.all()
    titles.filter("show", True)
    if start_from:
      key = db.Key.from_path("Title", start_from)
      titles.filter("__key__ >", key)

    return render_response(
        "welcome.html",
        boards = [ ("a", "Animu") ],
        titles = titles.fetch(self.MAX_T),
    )

class Title(RequestHandler):
  def get(self, title):
    title_db = renamed(title)

    if not title_db:
      raise NotFound

    eps = models.Ep.all()
    eps.order("date_modify")
    eps.ancestor(title_db)

    return render_response(
        "title.html",
        title = title_db,
        eps = eps,
    )

class Import(RequestHandler):
  def get(self):

    releases = {}
    to_save = []
    for title_ep in uplinks.get_titles():
      #logging.info("t: %r" % title_ep)

      ep = models.Ep(**title_ep)

      subbers = releases.get(ep.title, [])
      if ep.subber not in subbers:
        subbers.append(ep.subber)
      releases[ep.title] = subbers

      to_save.append(ep)

    db.put(to_save)
  
    deferred.defer(releasers_update, releases.items())


    return Response("loaded")

# XXX: move
def renamed(title_name):
  rename = models.Rename.get_by_key_name(title_name)


  if rename:
    title_name = rename.name

  return models.Title.get_by_key_name(title_name)

def releasers_update(releases):
  title_name, groups = releases.pop()

  title_db =  renamed(title_name)
  
  if not title_db:
    title_db = models.Title(name=title_name)

  save = False
  for group in groups:
    if group and group not in title_db.subbers:
      title_db.subbers.append(group)
      save = True

  if save:
    title_db.put()

  if releases:
    deferred.defer(releasers_update, releases)


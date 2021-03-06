import logging
from uuid import uuid4
import simplejson
import simpleyaml

from google.appengine.ext import db
from google.appengine.ext import deferred
from google.appengine.api.users import get_current_user

import  google.appengine.api.prospective_search as matcher

from tipfy import RequestHandler, Response, Forbidden, NotFound, redirect_to
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

    r = models.Rename.get_by_key_name(title)

    if r and r.name != title:
      return redirect_to("title",title=r.name)

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

    for ep in to_save:
      matcher.match(
          ep,
          result_key=str(ep.key()),
          result_return_document=False
      )
  
    deferred.defer(releasers_update, releases.items())


    return Response("loaded")

# XXX: move
def renamed(title_name):
  rename = models.Rename.get_by_key_name(title_name)


  if rename:
    title_name = rename.name

  return models.Title.get_by_key_name(title_name)

def releasers_update(releases):
  if not releases:
    return

  title_name, groups = releases.pop()

  title_db =  renamed(title_name)
  
  if not title_db:
    title_db = models.Title(name=title_name)

    title_hint = models.TitleHint(name=title_name)
    title_hint.put()

  save = False
  for group in groups:
    if group and group not in title_db.subbers:
      title_db.subbers.append(group)
      save = True

  if save:
    title_db.put()

  deferred.defer(releasers_update, releases)

class ShowDrop(RequestHandler):
  dumper = simplejson.dumps
  CT = 'application/json'
  def get(self, token=None):
    if token:
      token_db = models.Token.get_by_key_name(token)
      if not token_db:
        raise NotFound

      email = token_db.owner
    else:
      user = get_current_user()
      email = user.email()

    drop = models.Drop.load(email)

    eps = db.get(drop.data)

    try:
      dumps = self.dumper.__func__
    except AttributeError:
      dumps = self.dumper.im_func

    out = dumps([
      dict(
        link=ep.link,
        number=ep.number,
        title=ep.title,
        subber = ep.subber,
      )
      for ep in eps if ep
      ])

    return Response(out, content_type=self.CT)

class YShowDrop(ShowDrop):
  dumper = simpleyaml.dumps
  CT = 'text/x-yaml'


class GenToken(RequestHandler):
  def get(self):
    user = get_current_user()

    token_str = str(uuid4())

    token = models.Token(owner=user.email(), key_name = token_str)
    token.put()

    return Response("token: %s" % token_str)

class RebuildNames(RequestHandler):
  def get(self):
    from rebuild import rebuild_starts
    rebuild_starts()
    return Response("ya-ya")

# encoding=utf8

import urllib
import logging
from xml import sax

from google.appengine.ext import deferred
from google.appengine.ext import db

from tipfy import RequestHandler, Response
from models import Rename

TITLES = 'http://anidb.net/api/animetitles.xml.gz'

class Import(RequestHandler):
  def get(self):

    deferred.defer(load)

    return Response("nya")

def load():
  remote = urllib.urlopen(TITLES)

  handler = AnidbHandler()

  try:
    sax.parse(remote, handler)
  except ValueError:
    pass

class AnidbHandler(sax.ContentHandler):
  aid = None
  titles = []
  def startElement(self, name, attrs):
    self.current = name
    f = getattr(self, 'start_%s' % name, None)
    if f:
      f(attrs)

  def endElement(self, name):
    self.current = None
    f = getattr(self, 'end_%s' % name, None)
    if f:
      f()

  def characters(self, content):
    if not self.current:
      return

    f = getattr(self, 'content_%s' % self.current, None)
    if f:
      f(content)

  def content_title(self, content):
    self.titles[-1][-1] += content

  def start_anime(self, attrs):
    self.aid = int(attrs.getValue("aid"))

  def end_anime(self):
    #logging.info("commit %d %r" % (self.aid, self.titles))
    deferred.defer(renamed, self.aid, self.titles)
    self.titles = []

  def start_title(self, attrs):
    typ = attrs.getValue("type")
    lang = attrs.getValue("xml:lang")

    self.titles.append( [typ,lang,u""] )

def renamed(aid, names):
  put = []
  main = None
  for typ,lang,name in names:
    if 'main' == typ:
      main = name

  if not main:
    return

  put.append(Rename(key_name = "anidb%d" % aid, name=main, typs=["anidb"]))
  for typ,lang,name in names:
    put.append(Rename(
      key_name=name,
      typs=[typ,lang],
      name=main)
    )

  db.put(put)


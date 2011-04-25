# encoding=utf8

import urllib
import logging
from xml.dom import minidom

from google.appengine.ext import deferred
from google.appengine.ext import db

from tipfy import RequestHandler, Response
from models import Rename

TITLES = 'http://anidb.net/api/animetitles.xml.gz'

class Import(RequestHandler):
  def get(self):
    remote = urllib.urlopen(TITLES)

    dom = minidom.parse(remote)

    ac = []
    for name in parse(dom):
      if type(name) == int and ac:
        aid = ac.pop(0)
        deferred.defer(renamed, aid, ac)
        ac = []

      ac.append(name)

    return Response("nya")

def parse(xml):
  [titles] = xml.getElementsByTagName("animetitles")
  for anime in titles.childNodes:
    if anime.nodeName != 'anime':
      continue

    anidb_id = int(anime.getAttributeNode("aid").value)
    yield anidb_id

    for name in anime.childNodes:
      if name.nodeName != 'title':
        continue

      typ = name.getAttributeNode("type").value
      lang = name.getAttributeNode("xml:lang").value
      [data] = name.childNodes

      yield [typ,lang],data.nodeValue

  yield 0

def renamed(aid, names):
  put = []
  key_name = None
  for (typ,lang), name in names:
    if 'main' == typ:
      key_name = name

  if not key_name:
    return

  for typs, name in names:
    put.append(Rename(key_name=key_name, typs=typs,name=name) )

  db.put(put)


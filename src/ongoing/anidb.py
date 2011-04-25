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

    deferred.defer(load)

    return Response("nya")

def load():
  remote = urllib.urlopen(TITLES)

  head = remote.readline()
  head += remote.readline()

  logging.info("fetched head")

  while True:
    data = head

    while '</anime>' not in data:
      c = remote.readline()
      if not c:
        return

      data += c

    data += "</animetitles>"

    try:
      dom = minidom.parseString(data)
    except:
      logging.error("fuckup : %r" % data)

    ac = list(parse(dom))

    aid = ac.pop(0)
    deferred.defer(renamed, aid, ac)


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

def renamed(aid, names):
  put = []
  main = None
  for (typ,lang), name in names:
    if 'main' == typ:
      main = name

  if not main:
    return

  put.append(Rename(key_name = "anidb%d" % aid, name=main, typs=["anidb"]))
  for typs, name in names:
    put.append(Rename(key_name=name, typs=typs,name=main) )

  db.put(put)


import feedparser
import logging
import re

QUALITY = [
      "BD",
      "Blu-Ray",
      "360p",
      "480p",
      "720p",
      "1080p",
      "h264",
      "h.264",
      "H264",
      "Vorbis",
      "x264",
      "OGG",
      "DVD",
      "XVID",
      "MP3",
      "FLAC",
      "AAC",
      "[0-9]{3,4}x[0-9]{3,4}",
      "SD",
      "HD",
      "AC3",
      "Bluray",
]

def title_parse(title):
  title = title.replace(" ", "_")
  title = re.sub("\]_*\[", "][", title)
  title = re.sub("\.[a-zA-Z0-9]{3}$", "", title)

  # remove crc
  title = re.sub("\[[a-fA-F0-9]{8}\]", "", title)

  for q in QUALITY:
    qr = re.search("(%s)" % q, title, re.I)

    if qr:
      #logging.info("qr: %r" % qr.groups())

      qulity = qr.groups()[0]

      title = title.replace(qulity, "")

  title = re.sub("\[[,_-]*\]", "", title)
  title = re.sub("\([,_-]*\)", "", title)

  sb = re.match("^\[([^\[]*)\]", title)

  if not sb:
    sb = re.match("^.*\[([^\[]*)\]$", title)

  if not sb:
    sb = re.match("^.*\(([^\[]*)\)$", title)

  if sb:
    sb = sb.groups()[0]
    title = title.replace(sb, "")
    title = re.sub("\[[_-]*\]", "", title)
  else:
    sb = None


  ep = re.search("([0-9]{1,3}-[0-9]{1,3})", title)

  if not ep:
    ep = re.search("[_-]([0-9]{2,3})", title)

  if not ep:
    ep = re.search("(EP|Ep\.|E|SP|OVA)([0-9]{1,3})", title)

  if ep:
    ep_n = ep.groups()[-1]
    ep_n = int(ep_n.split("-")[0]) # XXX 

    title = re.sub(ep.group()+"(v[0-9])?", "", title)

  else:
    ep_n = None

  #logging.info("t: %r, ep: %r" % (entry.title, ep_n))

  #logging.info("t: %r, sb: %r" % (entry.title, sb))

  title = re.sub("\[[^\]]*\]", "", title)
  title = re.sub("\([^\)]*\)", "", title)



  while title[0] in ["_", "-"]:
    title = title[1:]

  while title[-1] in ["_", "-"]:
    title = title[:-1]

  title = title.replace("_", " ")

  logging.info("t: %r" % title)

  return {
      "subber" : sb,
      "title" : title,
      "number" : ep_n,
  }


class TokyoTosho(object):
  URL = 'http://tokyotosho.info/rss.php?filter=1&zwnj=0'
  

  @classmethod
  def load(cls):
    feed = feedparser.parse(cls.URL)

    for entry in feed.entries:
      parsed = cls.parse(entry)
      if parsed:
        yield parsed

  @classmethod
  def parse(cls, entry):
    ret = title_parse(entry.title)

    ret['link'] = entry.link

    return ret

      
enabled = [TokyoTosho]

def get_titles():
  ret = []
  for up in enabled:
    ret.extend(up.load())

  return ret

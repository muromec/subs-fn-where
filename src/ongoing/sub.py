import time
import logging

import  google.appengine.api.prospective_search as matcher
from google.appengine.api.users import get_current_user
from google.appengine.api import mail
from google.appengine.ext import db

from tipfy import RequestHandler, Response, redirect_to

from models import Ep, Drop

class Refresh(RequestHandler):
  def get(self):
    when = int(time.time() + (3600 * 2))

    sub_list = matcher.list_subscriptions(Ep, expires_before=when)

    for sub_id, query, expiration_time, state, error in sub_list:
      matcher.subscribe(Ep, query, sub_id)


    return Response("ok")

class Add(RequestHandler):
  def get(self, title):
    user = get_current_user()
    sub_id = "%s/%s" % (user.email(), title)
    matcher.subscribe(Ep, "title:"+title, sub_id)

    return redirect_to("title", title=title)


class Result(RequestHandler):
  def post(self):
    key = self.request.form.get('key')

    ep = db.get(db.Key(key))

    for sub_id in self.request.form.getlist("id"):
      sub_ids = sub_id.split('/')
      db.run_in_transaction(dispatch, sub_ids, ep)

    return Response("ok")


def dispatch((email,title), ep):
  drop = Drop.load(email)
  if ep.key() in drop.data:
    logging.info("ingore %r" % ep.key())
    return

  drop.data.append(ep.key())
  drop.put()

  logging.info("puted %r" % drop.data)


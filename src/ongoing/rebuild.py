import models

from google.appengine.ext import deferred


def rebuild_starts(cursor=None):

    rebuildq = models.Title.all(keys_only=True)
    rebuildq.with_cursor(cursor)

    title = rebuildq.get()

    if not title:
       return

    deferred.defer(rebuild, title.name())
    

    deferred.defer(rebuild_starts, rebuildq.cursor())


def rebuild(title):

    hint = models.TitleHint(name=title)
    hint.put()

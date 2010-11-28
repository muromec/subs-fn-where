from tipfy import Rule
from werkzeug.routing import Submount
import ongoing.urls

def get_rules():
  ret = [
    Rule(
      '/_ah/queue/deferred',
      endpoint = 'tasks/deferred',
      handler = 'tipfy.ext.taskqueue:DeferredHandler'
    )
  ]

  ret.extend(ongoing.urls.get_rules())

  return ret

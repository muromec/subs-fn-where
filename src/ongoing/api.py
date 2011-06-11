
from django.utils.simplejson import dumps

from tipfy import RequestHandler, Response

import models


class TitleHint(RequestHandler):
    def get(self):
        start = self.request.args.get("start")
        start = start.lower()
        
        hintq = models.TitleHint.all(keys_only=True)
        hintq.filter("start", start)

        names = [
            hint.name()
            for hint in hintq
        ]

        return Response(dumps({
            "status": "ok",
            "names": names,
        }))



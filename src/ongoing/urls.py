from tipfy import Rule

def get_rules():
  return [
      Rule(
        "/",
        handler="ongoing.handlers.Index",
      ),
      Rule(
        "/next/<string:start_from>",
        handler="ongoing.handlers.Index",
      ),
      Rule(
        "/adm/import",
        handler="ongoing.handlers.Import",
      ),
      Rule(
        "/adm/import/calendar",
        handler="ongoing.animecalendar.Import",
      ),
      Rule(
        "/adm/import/anidb",
        handler="ongoing.anidb.Import",
      ),
      Rule(
        "/adm/fix",
        handler="ongoing.fixer.Fix",
      ),

      Rule(
        "/t/<path:title>",
        endpoint="title",
        handler="ongoing.handlers.Title",
      ),
      Rule(
        "/u/sub/add/<path:title>",
        endpoint="sub:add",
        handler="ongoing.sub.Add",
      ),
      Rule(
        "/adm/sub/refresh",
        handler="ongoing.sub.Refresh",
      ),
      Rule(
        "/_ah/prospective_search",
        handler="ongoing.sub.Result",
      ),
  ]

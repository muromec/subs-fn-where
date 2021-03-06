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
        "/u/sub/add/<path:title>/subber/<path:subber>",
        endpoint="sub:add",
        handler="ongoing.sub.Add",
      ),
      Rule(
        "/u/drop",
        handler="ongoing.handlers.ShowDrop",
      ),
      Rule(
        "/r/drop/<token>",
        handler="ongoing.handlers.ShowDrop",
      ),
      Rule(
        "/u/ydrop",
        handler="ongoing.handlers.YShowDrop",
      ),
      Rule(
        "/r/ydrop/<token>",
        handler="ongoing.handlers.YShowDrop",
      ),

      Rule(
        "/u/token",
        handler="ongoing.handlers.GenToken",
      ),
      Rule(
        "/adm/sub/refresh",
        handler="ongoing.sub.Refresh",
      ),
      Rule(
        "/_ah/prospective_search",
        handler="ongoing.sub.Result",
      ),

      Rule(
        "/api/title_hint",
         handler="ongoing.api.TitleHint",
      ),

      Rule(
        "/adm/regen_hint",
        handler="ongoing.handlers.RebuildNames",
      ),

  ]

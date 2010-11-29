from tipfy import Rule

def get_rules():
  return [
      Rule(
        "/",
        handler="ongoing.handlers.Index",
      ),
      Rule(
        "/next<string:start_from>",
        handler="ongoing.handlers.Index",
      ),
      Rule(
        "/adm/import",
        handler="ongoing.handlers.Import",
      ),
      Rule(
        "/t/<path:title>",
        handler="ongoing.handlers.Title",
      ),
  ]

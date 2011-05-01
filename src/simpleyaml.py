import StringIO

x = [ {"x":u"err", "y":1l,}, {"x":u"arr", "d":2}]


def dumper(x, out=None, lvl=0):
  out = out or StringIO.StringIO()

  f = dumpers.get(type(x), dump_str)

  f(x, out, lvl)

  return out

def dump_list(x, out,lvl):
  for el in x:
    out.write("- ")
    dumper(el, out,lvl+2)

    for x in range(lvl):
      out.write(" ")

  out.write("\n")


def dump_str(x, out, lvl):
  out.write(x)
  out.write("\n")

def dump_dict(x, out, lvl):
  for k,v in x.items():
    out.write(k)
    out.write(": ")
    dumper(v, out,lvl+2)

    for x in range(lvl):
      out.write(" ")

  out.write("\n")

dumpers = {
    list : dump_list,
    dict : dump_dict,
    str : dump_str,
}

def dumps(x):
  out = dumper(x)

  out.seek(0)
  return out.read()

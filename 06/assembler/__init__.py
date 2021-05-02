m = __import__ ("06/assembler")

try:
    attrlist = m.__all__
    print(attrlist)
except AttributeError:
    attrlist = dir (m)
for attr in attrlist:
    globals()[attr] = getattr (m, attr)
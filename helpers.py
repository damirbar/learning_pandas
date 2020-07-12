
def hdr(s):
    s += ":"
    fmt = "{0:=^"
    fmt += str(len(s))
    fmt += "}"
    print(fmt.format(""))
    print(s)
    print(fmt.format(""))

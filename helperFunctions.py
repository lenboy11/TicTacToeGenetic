## helperFunctions
def list_to_str(l):
    enumeration = l.pop(0)
    if len(l) > 0:
        last = l.pop(0)
        for el in l:
            enumeration += ", " + str(el)
        enumeration += " or " + last
    return enumeration
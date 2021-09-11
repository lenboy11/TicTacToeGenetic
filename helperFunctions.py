## helperFunctions
def list_to_str(l):
    lcopy = l.copy()
    enumeration = lcopy.pop(0)
    if len(lcopy) > 0:
        last = lcopy.pop(0)
        for el in lcopy:
            enumeration += ", " + str(el)
        enumeration += " or " + last
    return enumeration
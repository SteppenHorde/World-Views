def isfloat(string):
    try:
        float(string)
    except ValueError:
        return False
    else:
        if string.count('.') == 1:
            return True
        else:
            return False

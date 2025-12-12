def calc_net_weight(firstW, lastW):
    try :
        f = float(firstW)
        l = float(lastW)
        if f > l:
            return f - l
        else:
            return l - f
    except :
        pass
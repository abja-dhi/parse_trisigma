def check_trips(tr, sdr, fdr, sdu, fdu):
    if tr != '' and sdu != '' and fdu != '':
        return True
    elif tr != '' and sdr != '' and fdr != '':
        return True
    else:
        return False
def DMS2DD(DMS):
    angle = float(DMS.split("°")[0])
    tmp = DMS.split("°")[1]
    minute = float(tmp.split("'")[0])
    tmp = tmp.split("'")[1]
    second = float(tmp.split('"')[0].replace(",", "."))
    angle = angle + minute / 60 + second / 3600
    if tmp.split('"')[1] == "S" or tmp.split('"')[1] == "W":
        angle = angle * (-1)
    return angle
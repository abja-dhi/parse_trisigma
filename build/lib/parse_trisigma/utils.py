from datetime import datetime
import numpy as np

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

def str2latlon(str):
    try:
        lat = DMS2DD(str.split("\n")[0].strip().replace("'`", "'").replace('`', "'"))
        lon = DMS2DD(str.split("\n")[1].strip().replace("'`", "'").replace('`', "'"))
        return [np.round(lat, 3), np.round(lon, 3)]
    except:
        return [np.nan, np.nan]
    
def get_number(x):
    try:
        return x.replace(" mtr", "").replace(",", ".").replace(" m", "").replace("mtr", "")
    except:
        return np.nan
def set_date(x, ref_date):
    try:
        ref_date = datetime.strptime(ref_date, "%Y-%m-%d")
        x = datetime.strptime(x, "%H:%M").time()
        return ref_date.combine(ref_date, x)
    except:
        return np.nan
    
def m3(x):
    try:
        x = x.replace(".", "")
    except:
        pass
    try:
        x = x.replace(",", "")
    except:
        pass
    try:
        return float(x)
    except:
        return np.nan
    
def get_lat(x):
    try:
        return [float(x) for x in str(x).replace("[", "").replace("]", "").split(", ")][0]
    except:
        return np.nan
    
def get_lon(x):
    try:
        return [float(x) for x in str(x).replace("[", "").replace("]", "").split(", ")][1]
    except:
        return np.nan
    
def find_area(lon, lat):
    if lon < 136.8:
        return "Area A"
    elif lon < 136.84:
        return "Area C"
    elif lat > -4.8325:
        return "Area D"
    else:
        return "Area F"
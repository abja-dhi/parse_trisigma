from .DMS2DD import DMS2DD

def str2latlon(str):
    lat = DMS2DD(str.split("\n")[0].strip().replace('`', ''))
    lon = DMS2DD(str.split("\n")[1].strip().replace('`', ''))
    return lat, lon
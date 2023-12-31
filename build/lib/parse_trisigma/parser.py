import os
import camelot
import pandas as pd
import locale
locale.setlocale(locale.LC_ALL, "nl_NL")
import datetime
import time
from string import ascii_uppercase as apc
import geopandas as gpd
import numpy as np
from shapely.geometry import Point
import matplotlib.pyplot as plt
from .utils import DMS2DD, str2latlon, get_number, set_date, m3, get_lat, get_lon, find_area
from myUtils.mkch import mkch

class Parser:
    def __init__(self, out_path, reports_path) -> None:
        self.out_path = out_path
        self.reports_path = reports_path
        mkch(out_path)


    
    def parse(self):
        # Walk through all the folders and grab the file paths
        self.fnames = []
        self.dates = []
        for root, dirs, files in os.walk(self.reports_path):
            for f in files:
                if ".pdf" in f:
                    self.fnames.append(os.path.join(root, f))
                    self.dates.append(f)
        
        # Grab the date information from the filenames
        self.datetimes = []
        for d in self.dates:
            d = d.replace("Daily production Report - ", "").replace("DPR", "").replace(".pdf", "").replace("KA3", "").replace(" ", "").capitalize().replace("desember", "december")
            self.datetimes.append(datetime.datetime.strptime(d, "%d%B%Y").strftime("%Y-%m-%d"))

        self.df_tot = pd.DataFrame()
        for i in range(len(self.fnames)):
            f = self.fnames[i]
            ref_date = self.datetimes[i]
            print(ref_date)
            df = self._parse_pdf(f, ref_date)
            self.df_tot = pd.concat([self.df_tot, df])

        self._update_df()

        return self.df_tot


    def _update_df(self):
        self.df_tot = self.df_tot[["Trip", "Start Dredging", "Finish Dredging", "Dredging Lon", "Dredging Lat", "Area", "Loaded Draft", "Hopper", "% Sediment", "Volume", "Start Travelling", "Finish Travelling", "Start Dumping", "Finish Dumping", "Dumping Lon", "Dumping Lat", "Empty Draft"]]


    def _parse_pdf(self, fname, ref_date):
        """
        Parse the data from the PDF file
        """
        df = camelot.read_pdf(fname)._tables[0].df
        df = self.clean_df(df, ref_date)
        return df
    
        
    def clean_df(self, df, ref_date):
        df = df[[0, 2, 3, 5, 6, 7, 8, 10, 11, 13, 21, 23, 24, 25]]
        df.drop([0, 1, 2], axis=0, inplace=True)
        df.drop(range(15, len(df)+3), axis=0, inplace=True)
        df.reset_index(inplace=True)
        df.columns = ["Row", "Trip", "Start Dredging", "Finish Dredging", "Loaded Draft", "Dredging Coord", "Start Travelling", "Finish Travelling", "Start Dumping", "Finish Dumping", "Empty Draft", "Dumping Coord", "Hopper", "% Sediment", "Volume"]
        df.set_index("Row", inplace=True)
        df.replace("", np.nan, inplace=True)
        df.dropna(axis=0, how='all', inplace=True)
        df["Start Dredging"] = df["Start Dredging"].apply(set_date, args=[ref_date])
        df["Finish Dredging"] = df["Finish Dredging"].apply(set_date, args=[ref_date])
        df["Loaded Draft"] = df["Loaded Draft"].apply(get_number)
        df["Dredging Coord"] = df["Dredging Coord"].apply(str2latlon)
        df["Dredging Lat"] = df["Dredging Coord"].apply(get_lat)
        df["Dredging Lon"] = df["Dredging Coord"].apply(get_lon)
        df["Start Travelling"] = df["Start Travelling"].apply(set_date, args=[ref_date])
        df["Finish Travelling"] = df["Finish Travelling"].apply(set_date, args=[ref_date])
        df["Start Dumping"] = df["Start Dumping"].apply(set_date, args=[ref_date])
        df["Finish Dumping"] = df["Finish Dumping"].apply(set_date, args=[ref_date])
        df["Empty Draft"] = df["Empty Draft"].apply(get_number)
        df["Dumping Coord"] = df["Dumping Coord"].apply(str2latlon)
        df["Dumping Lat"] = df["Dumping Coord"].apply(get_lat)
        df["Dumping Lon"] = df["Dumping Coord"].apply(get_lon)
        df.drop(["Dredging Coord", "Dumping Coord"], axis=1, inplace=True)
        df["Hopper"] = df["Hopper"].apply(m3)
        df["Volume"] = df["Volume"].apply(m3)
        df["Area"] = df.apply(lambda x: find_area(x["Dredging Lon"], x["Dredging Lat"]), axis=1)
        return df
    
    #def fill_missings(self):

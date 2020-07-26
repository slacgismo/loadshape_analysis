"""Loadshape analysis tool

The loadshape analysis module computes loadshapes for arbitary CSV load data sets.

Loadshapes are computed in one or more 24-hour series.  If more than one loadshape is computed, they are usually grouped by daytype, e.g., `weekday`, `weekend`.

To perform a customer grouping, a `get` function must be defined. By default
there are only two grouping functions, `get_daytype` and `get_hour`. 
Additional grouping functions may be added by specifying the `groupby`
parameter.

Example:

    from loadshape import *
    ls = Loadshape('testdata.csv',converters={'datetime':lambda x:dt.datetime.strptime(x,"%Y-%m-%d %H:%M:%S")})
    print(ls.loadshape())
    ls.groupby = {"hour":[ls.datecol,get_hour,ls.dstrules]}
    print(ls.loadshape())

"""
import sys
if sys.version_info[0] < 3:
    raise Exception("python version must be 3.0 or higher")

import os
import datetime as dt
import numpy as np
import pandas as pd
import sys

def get_daytype(x, daytypes):
    """Get the daytype for a datetime value"""
    for daytype, weekdays in daytypes.items():
        if x.weekday() in weekdays:
            return daytype
    return None

def get_hour(x, dstrules ):
    """Get the hour of day for a datetime value"""
    if x.year in dstrules:
        rule = dstrules[x.year]
        if x > rule[0] and x <= rule[1]:
            return x.hour+1
    return x.hour

class Loadshape:
    """Loadshape implementation"""

    def __init__(self, csvfile=None, **kwargs):
        """Initialize Loadshape object"""
        if csvfile:
            self.data = pd.read_csv(csvfile,**kwargs)
        else:
            self.data = pd.DataFrame(kwargs)
        self.datecol = self.data.columns[0]
        self.daytypes = {
            "weekday" : [0,1,2,3,4],
            "weekend" : [5,6],
            "holiday" : [7],
            }
        self.dstrules = {}
        self.groupby = {
            "daytype":[self.datecol,get_daytype,self.daytypes],
            "hour":[self.datecol,get_hour,self.dstrules]
            }
        self.columns = self.data.columns[1:]
        self.add_groups()

    def add_groups(self):
        """Add one or more groups to a Pandas DataFrame"""
        for name, group in self.groupby.items():
            self.data[name] = list(map(lambda x: group[1](x,group[2]),self.data[group[0]]))

    def normalize(self, value=None, inplace=False):
        """Normalize a Numpy series or DataFrame column"""
        if not value:
            result = self.data
        elif value == 'max':
            result = self.data / self.data.max()
        elif value == 'min':
            result = self.data / self.data.min()
        elif value == 'range':
            result = self.data / (self.data.max()-self.data.min())
        else:
            result = self.data / value
        if inplace:
            self.data = result
        else:
            return result

    def loadshape(self, normalization='max'):
        """Load an enduse loadshape into a DataFrame"""
        self.data = self.data.groupby(list(self.groupby.keys()))
        self.data = self.data[self.columns].sum()
        self.normalize(normalization,inplace=True)
        return pd.DataFrame(self.data,columns=self.columns)

if __name__ == '__main__':

    import unittest

    class TestLoadshapeDaytype(unittest.TestCase):
        """Unit testing class"""

        ls = Loadshape('testdata.csv',converters={'datetime':lambda x:dt.datetime.strptime(x,"%Y-%m-%d %H:%M:%S")})
        result = ls.loadshape()
        assert(result.shape==(48,1))
        assert(result.max()['load']==1.0)

    class TestLoadshapeHour(unittest.TestCase):
        """Unit testing class"""

        ls = Loadshape('testdata.csv',converters={'datetime':lambda x:dt.datetime.strptime(x,"%Y-%m-%d %H:%M:%S")})
        ls.groupby = {"hour":[ls.datecol,get_hour,ls.dstrules]}
        result = ls.loadshape()
        assert(result.shape==(24,1))
        assert(result.max()['load']==1.0)

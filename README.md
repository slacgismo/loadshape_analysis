The loadshape analysis module computes loadshapes for arbitary CSV load data sets.

Loadshapes are computed in one or more 24-hour series.  If more than one loadshape is computed, they are usually grouped by daytype, e.g., `weekday`, `weekend`.

To perform a customer grouping, a `get` function must be defined. By default there are only two grouping functions, `get_daytype` and `get_hour`.  Additional grouping functions may be added by specifying the `groupby` parameter.

Example:

~~~
>>> from loadshape import *
>>> ls = Loadshape('testdata.csv',converters={'datetime':lambda x:dt.datetime.strptime(x,"%Y-%m-%d %H:%M:%S")})
>>> ls.loadshape()
                  load
daytype hour          
weekday 0     0.447995
        1     0.437313
        2     0.441207
        3     0.461819
        4     0.575674
        5     0.775771
        6     0.982281
        7     1.000000
        8     0.908188
        9     0.837535
        10    0.800837
        11    0.739926
        12    0.696098
        13    0.675561
        14    0.684019
        15    0.745459
        16    0.857878
        17    0.965315
        18    0.968541
        19    0.967299
        20    0.944210
        21    0.803619
        22    0.636910
        23    0.516616
weekend 0     0.190945
        1     0.180763
        2     0.180531
        3     0.187351
        4     0.202301
        5     0.239496
        6     0.305467
        7     0.369949
        8     0.409606
        9     0.399953
        10    0.375344
        11    0.353045
        12    0.339295
        13    0.316050
        14    0.310711
        15    0.318433
        16    0.333318
        17    0.352356
        18    0.358716
        19    0.367455
        20    0.362257
        21    0.315463
        22    0.255831
        23    0.206006
>>> ls.groupby = {"hour":[ls.datecol,get_hour,ls.dstrules]}
>>> ls.loadshape()
          load
hour          
0     0.466397
1     0.451167
2     0.453840
3     0.473864
4     0.567886
5     0.741098
6     0.939997
7     1.000000
8     0.961929
9     0.903310
10    0.858558
11    0.797819
12    0.755789
13    0.723830
14    0.726108
15    0.776592
16    0.869518
17    0.961839
18    0.968837
19    0.974309
20    0.953661
21    0.816878
22    0.651660
23    0.527481
~~~
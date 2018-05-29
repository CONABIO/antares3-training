import pandas
import geopandas
import os
import numpy

shape = geopandas.read_file('mx_man15gw.shp')
class_index={'MANGLAR': 9}
shape = shape.to_crs({'init': 'epsg:4326'})
shape['madmex'] = shape['Descrip'].str.upper().map(class_index).fillna(0).astype(numpy.int16)
shape.to_file('mangroves.shp')

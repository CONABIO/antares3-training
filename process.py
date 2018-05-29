import pandas
import geopandas
import os
import numpy

DROP = [45091, 30754, 45090, 31799, 26528, 31719]

def check_names(filename, code, mapping):
    print(filename)
    basename = os.path.basename(filename)
    print(basename)
    outputname = os.path.join('output', basename)
    print(outputname)
    shape = geopandas.read_file(filename)

    '''
    for value in list(shape[code].unique()):
        if not mapping.get(value.upper(), None):
            print(value)
    '''
    #print(shape.crs)
    #shape = shape.to_crs({'init': 'epsg:4326'})

    if 'usv250s6' in filename:
        shape = shape[~shape['OBJECTID'].isin(DROP)]

    shape['madmex'] = shape[code].str.upper().map(mapping).fillna(0).astype(numpy.int16)
    shape.to_file(outputname)



excel = pandas.read_excel('Tabla_INEGI_MADMex.xlsx')

class_index={'IAPF': 29}

for row in range(len(excel)):
    class_index[excel['clave'][row].upper()] = excel['MAD-MEX 32 Clases'][row]

class_index_fot={'VSA/MKX': 14,
                 'VSA/VPN': 8,
                 'VP': 8,
                 'VSA/MKE': 5,
                 'VSA/VHH': 26,
                 'VSA/PT': 9,
                 'VSA/SBQP': 8}

for row in range(len(excel)):
    class_index_fot[excel['clave_fot'][row].upper()] = excel['MAD-MEX 32 Clases'][row]


check_names('USV_2/usv250ks2cw.shp',
            'CLAVE',
            class_index)
check_names('USV_3/usv250ks3cw.shp',
            'CLAVE_V',
            class_index)
check_names('USV_4/usv250ks4cw.shp',
            'CLAVE',
            class_index)
check_names('USV_5/usv250ks5cw.shp',
            'CLAVE',
            class_index_fot)
check_names('USV_6-20180427T211638Z-001/conjunto_de_datos/usv250s6_union.shp',
            'CVE_UNION',
            class_index)
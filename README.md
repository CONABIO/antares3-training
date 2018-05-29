# Antares 3 Initial Training Set

## INEGI Series

We expecto to have all the INEGI series (in this case we are talking about series 2-6), extracted in a single folder. Additionally, we need the excel file with the mappings between INEGI and MAD-Mex classes. In that very same folder we need to have the file *process.py*. Finally a clean directory where the output will be written (output should be the name of the directory). The layout should be as follows:

```
Tabla_INEGI_MADMex.xlsx
USV_1
USV_2
USV_3
USV_4
USV_5
USV_6-20180427T211638Z-001
output
process.py
```

Then we type:

```
python process.py
```

This process will armonize the INEGI series creating a new column named *madmex* in which the landcover classes will be coded using the MADMex scheme. The files will be written in the *output* directory.

Once we have the clean shape files, we can rasterize them to use raster algebra to get the persistent polygons. While series 2-5 have the same extent, series 6 has a different one. To armonize this as well we rasterize using the option to fix the extent window. As this was done in the cluster (nodo5), the paths are absolute, so this commands can be executed anywhere:

```
gdal_rasterize -co COMPRESS=LZW -ot Byte -a madmex -tr 30.0 30.0 -te  907836.035 319429.201 4083036.035 2349619.201 -l usv250ks2cw /LUSTRE/MADMEX/tasks/2018_tasks/series_inegi_madmex/usv250ks2cw.shp /LUSTRE/MADMEX/tasks/2018_tasks/series_inegi_madmex_raster/usv250ks2cw.tif
gdal_rasterize -co COMPRESS=LZW -ot Byte -a madmex -tr 30.0 30.0 -te  907836.035 319429.201 4083036.035 2349619.201 -l usv250ks3cw /LUSTRE/MADMEX/tasks/2018_tasks/series_inegi_madmex/usv250ks3cw.shp /LUSTRE/MADMEX/tasks/2018_tasks/series_inegi_madmex_raster/usv250ks3cw.tif
gdal_rasterize -co COMPRESS=LZW -ot Byte -a madmex -tr 30.0 30.0 -te  907836.035 319429.201 4083036.035 2349619.201 -l usv250ks4cw /LUSTRE/MADMEX/tasks/2018_tasks/series_inegi_madmex/usv250ks4cw.shp /LUSTRE/MADMEX/tasks/2018_tasks/series_inegi_madmex_raster/usv250ks4cw.tif
gdal_rasterize -co COMPRESS=LZW -ot Byte -a madmex -tr 30.0 30.0 -te  907836.035 319429.201 4083036.035 2349619.201 -l usv250ks5cw /LUSTRE/MADMEX/tasks/2018_tasks/series_inegi_madmex/usv250ks5cw.shp /LUSTRE/MADMEX/tasks/2018_tasks/series_inegi_madmex_raster/usv250ks5cw.tif
gdal_rasterize -co COMPRESS=LZW -ot Byte -a madmex -tr 30.0 30.0 -te  907836.035 319429.201 4083036.035 2349619.201 -l usv250s6_union /LUSTRE/MADMEX/tasks/2018_tasks/series_inegi_madmex/usv250s6_union.shp /LUSTRE/MADMEX/tasks/2018_tasks/series_inegi_madmex_raster/usv250s6_union.tif
```


## BITS Reference Map

To rasterize all of bits shape files into a directory.

```
find $(pwd) -name *.shp -exec sh -c 'gdal_rasterize -ot Byte -co "COMPRESS=LZW" -a interpreta -where 'interpreta=predicted' -tr 30.0 30.0 $0 /LUSTRE/MADMEX/mapa_referencia_2015/30_meters/$(basename $0 .shp)-$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w ${1:-3} | head -n 1).tif' {} \;
```


To translate into the same window as the INEGI series:

```
gdal_translate -ot Byte -co COMPRESS=LZW -projwin 907836.035 2349619.201 4083036.035 319429.201  mexico.vrt mexico.tif
```

## Mangroves

The file *mx_man15gw.shp* was downloaded from CONABIO portal. A process similar to the one with the INEGI series was performed on the file with the python script named *transform_mangroves.py*. The resulting shape with the madmex column can be found at:

```
/LUSTRE/MADMEX/tasks/2018_tasks/mangroves/mangroves.shp
```

However, the resulting file is not projected so we need to project it into Lambert Comformal Conic (This Proj4 string was taken from [http://spatialreference.org/ref/sr-org/6700/](http://spatialreference.org/ref/sr-org/6700/)):

```
ogr2ogr -f "ESRI Shapefile" mangroves_inegi.shp mangroves.shp -t_srs "+proj=lcc +lat_1=17.5 +lat_2=29.5 +lat_0=12 +lon_0=-102 +x_0=2500000 +y_0=0 +datum=WGS84 +units=m +no_defs"
```

Then we can use this command to rasterize it:

```
gdal_rasterize -ot Byte -co COMPRESS=LZW -a madmex -tr 30.0 30.0 -te 907836.035 319429.201 4083036.035 2349619.201 mangroves_inegi.shp final_mangroves.tif
```


## Global Surface Water

We already downloaded and preprocess the tiles for the global surface water product. The pixels with >80 ocurrence of water where filtered and a shape file was created. Those polygons are available in the *antares* database. Dumping those objects into a shape file resulted into the file:

```
/LUSTRE/MADMEX/tasks/2018_tasks/global_surface_water/global_surface_water.shp
```

We need to apply the same process as with the mangroves file:

```
ogr2ogr -f "ESRI Shapefile" global_surface_water_inegi.shp global_surface_water.shp -t_srs "+proj=lcc +lat_1=17.5 +lat_2=29.5 +lat_0=12 +lon_0=-102 +x_0=2500000 +y_0=0 +datum=WGS84 +units=m +no_defs"
```


Later with this command we transformed that shape file into a raster:

```
gdal_rasterize -ot Byte -co COMPRESS=LZW -a madmex -tr 30.0 30.0 -te 907836.035 319429.201 4083036.035 2349619.201 global_surface_water_inegi.shp final_global_surface_water.tif
```

## INEGI + BITS + Mangroves + Global Surface Water

Finally we want to summarize the information of all series (2-6) in a single raster. To this end, we use rasterio and numpy to perform a raster algebra operation on the rasters, we will filter all the pixels whose class didn't change. Given that the rasters are quite big to fit in memory at the same time, we process them by block and write the output in the same way. Rasters with mangrove and water information will be overwritten on the final raster. In a folder that includes all the products that we just generated we execute:

```
python block.py
```

We have a raster file named *final.tif*. The current file can be found at:

```
/LUSTRE/MADMEX/tasks/2018_tasks/convergence_of_evidence
```

## Clumpling

To get rid of some pixels product of noise innherent to the BITS process we experimented with the SieveFilter function that comes with gdal:

```
python clump.py
```

The clumped file is in:

```
/LUSTRE/MADMEX/tasks/2018_tasks/convergence_of_evidence
```



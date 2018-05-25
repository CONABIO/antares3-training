# antares3_training
Some code snippets used to get a clean training dataset.

To rasterize all of bits shape files into a directory.

```
find $(pwd) -name *.shp -exec sh -c 'gdal_rasterize -ot Byte -co "COMPRESS=LZW" -a interpreta -where 'interpreta=predicted' -tr 30.0 30.0 $0 /LUSTRE/MADMEX/mapa_referencia_2015/30_meters/$(basename $0 .shp)-$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w ${1:-3} | head -n 1).tif' {} \;
```


To translate into the same window as the INEGI series:

```
gdal_translate -ot Byte -co "COMPRESS=LZW" -projwin 907836.035 2349619.201 4083036.035 319429.201  mexico.vrt mexico.tif
```
import gdal
filename = 'final.tif'
output = 'final_clumped.tif'
gdal.AllRegister()
threshold = 1
connectedness = 8
src_ds = gdal.Open(filename, gdal.GA_ReadOnly)
srcband = src_ds.GetRasterBand(1)
maskband = srcband.GetMaskBand()
drv = gdal.GetDriverByName(str('GTiff'))
dst_ds = drv.Create(output, src_ds.RasterXSize, src_ds.RasterYSize, 1,
                     srcband.DataType )
wkt = src_ds.GetProjection()
if wkt != '':
    dst_ds.SetProjection( wkt )
dst_ds.SetGeoTransform( src_ds.GetGeoTransform() )
dstband = dst_ds.GetRasterBand(1)
prog_func = gdal.TermProgress
result = gdal.SieveFilter(srcband, 
                          maskband, 
                          dstband,
                          threshold, 
                          connectedness,
                          callback = prog_func )
src_ds = None
dst_ds = None
mask_ds = None
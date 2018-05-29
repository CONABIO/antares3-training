import rasterio
import numpy
file_template = 'usv250ks%scw.tif'
file_6 = 'usv250s6_union.tif'
file_bits = 'mexico_bits.tif'
src_1 = rasterio.open(file_template % 2)
src_2 = rasterio.open(file_template % 3)
src_3 = rasterio.open(file_template % 4)
src_4 = rasterio.open(file_template % 5)
src_5 = rasterio.open(file_6)
src_6 = rasterio.open(file_bits)
water = rasterio.open('final_global_surface_water.tif')
mangroves = rasterio.open('final_mangroves.tif')


profile = src_1.profile
profile.update(
    dtype=rasterio.uint8,
    count=1,
    compress='lzw')
output = rasterio.open(
            'final.tif', 'w', **profile)
for ji, window in src_1.block_windows(1):
    print((ji, window))
    block_1 = src_1.read(window=window)
    block_2 = src_2.read(window=window)
    block_3 = src_3.read(window=window)
    block_4 = src_4.read(window=window)
    block_5 = src_5.read(window=window)
    block_6 = src_6.read(window=window)
    block_water = water.read(window=window)
    block_mangroves = mangroves.read(window=window)
    stack = numpy.vstack((block_1,
                          block_2,
                          block_3,
                          block_4,
                          block_5,
                          block_6))
    mask = numpy.logical_and(numpy.bitwise_and.reduce(stack) == stack[0],
                             numpy.bitwise_or.reduce(stack) == stack[0])

    mask_water = block_water == 32 # 32 is the class for water
    mask_mangroves = block_mangroves == 9 # 32 is the class for mangrove

    print(mask_water.shape)

    to_write = numpy.full(block_1.shape, 0).astype(rasterio.uint8)
    to_write[:,mask] = block_1[:,mask]
    to_write[mask_mangroves] = 9
    to_write[mask_water] = 32
    output.write(to_write, window=window)

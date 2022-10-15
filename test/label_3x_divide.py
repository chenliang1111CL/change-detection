from osgeo import gdal,ogr,osr
import os
from PIL import Image
def caijian(image_one,path,image_file):
    img = Image.open(image_one)
    f=image_file.split('.')
    w,h = img.size
    num = 1
    for r in range((h//256)-1):
        for c in range((w//256)-1):
            box = (c*256,r*256,c*256+512,r*256+512)
            file = os.path.join(path,f[0]+'_'+str(num)+'.tif')
            num = num+1
            rol = img.crop(box)
            rol.save(file)

def vector2raster(inputfilePath, outputfile, templatefile,bands=[1],burn_values=[0],field="",all_touch="False"):
    inputfilePath = inputfilePath
    outputfile = outputfile
    templatefile = templatefile
    # 打开栅格模板文件
    data = gdal.Open(templatefile, gdal.gdalconst.GA_ReadOnly)
    # 确定栅格大小
    x_res = 3072
    y_res = 3072

    # 打开矢量文件
    vector = ogr.Open(inputfilePath)
    # 获取矢量图层
    layer = vector.GetLayer()
    # geo_featrues = layer.GetGeomType()
    # print(geo_featrues)
    print(inputfilePath)


    # 创建输出的TIFF栅格文件
    targetDataset = gdal.GetDriverByName('GTiff').Create(outputfile, x_res, y_res, 1, gdal.GDT_Byte)
    # 设置栅格坐标系与投影
    targetDataset.SetGeoTransform(data.GetGeoTransform())
    targetDataset.SetProjection(data.GetProjection())
    # 目标band 1
    band = targetDataset.GetRasterBand(1)
    # 白色背景
    #NoData_value = -999
    NoData_value = 0
    band.SetNoDataValue(NoData_value)
    band.FlushCache()
    if field:
        # 调用栅格化函数。RasterizeLayer函数有四个参数，分别有栅格对象，波段，矢量对象，options
        # options可以有多个属性，其中ATTRIBUTE属性将矢量图层的某字段属性值作为转换后的栅格值
        gdal.RasterizeLayer(targetDataset, bands, layer, burn_values=burn_values,options=["ALL_TOUCHED="+all_touch,"ATTRIBUTE="+field])
    else:
        gdal.RasterizeLayer(targetDataset, bands, layer, burn_values=burn_values,options=["ALL_TOUCHED="+all_touch])


def data_migration_value(filename):

    # from layer
    vector = ogr.Open(filename)
    layer = vector.GetLayer()
    spatialRef = layer.GetSpatialRef()
    # from feature
    feature = layer.GetNextFeature()
    if feature==None:
        pass

    geom = feature.GetGeometryRef()
    # spatialRef = geom.GetSpatialReference()

    # coordinate migraion
    coor = []
    coornum = []
    while feature:
        try:
            # # change field value
            # x = feature.GetFieldAsDouble('x')
            # y = feature.GetFieldAsDouble('y')
            # x += 10
            # y += 10
            # feature.SetField('x',x)
            # feature.SetField('y',y)
            # layer.SetFeature(feature)
            # feature.transform()

            geom = feature.GetGeometryRef()
            polygon = geom.GetGeometryRef(0)
            num = polygon.GetPointCount()
            coornum.append(num)
            for j in range(num):
                # point data
                point = polygon.GetPoint(j)

                x = point[0]
                y = point[1]
                x = x*3
                y = y*3
                # x += 10
                # y += 10
                coor.append([x, y])
        except:
            print('done!')
        feature = layer.GetNextFeature()
    layer.ResetReading()
    return coor, coornum, spatialRef

    # copy filename feature
def data_migration_value2(x1,x2,filename):

    # from layer
    vector = ogr.Open(filename)
    layer = vector.GetLayer()
    spatialRef = layer.GetSpatialRef()
    # from feature
    feature = layer.GetNextFeature()

    geom = feature.GetGeometryRef()
    # spatialRef = geom.GetSpatialReference()

    # coordinate migraion
    coor = []
    coornum = []
    while feature:
        try:
            # # change field value
            # x = feature.GetFieldAsDouble('x')
            # y = feature.GetFieldAsDouble('y')
            # x += 10
            # y += 10
            # feature.SetField('x',x)
            # feature.SetField('y',y)
            # layer.SetFeature(feature)
            # feature.transform()

            geom = feature.GetGeometryRef()
            polygon = geom.GetGeometryRef(0)
            num = polygon.GetPointCount()
            coornum.append(num)
            for j in range(num):
                # point data
                point = polygon.GetPoint(j)

                x = point[0]
                y = point[1]
                x = x+x1
                y = y+x2
                # x += 10
                # y += 10
                coor.append([x, y])
        except:
            print('done!')
        feature = layer.GetNextFeature()
    layer.ResetReading()
    return coor, coornum, spatialRef

def osm_offset_outshp(coor, coornum, spatialRef, fp):
    #     定义写入路径
    #     fp=r'D:\G_project\real_data\London_data_output\osm_offset.shp'
    # 注册驱动
    ogr.RegisterAll()
    strDriverName = "geojson"  # 创建数据，这里创建ESRI的shp文件
    oDriver = ogr.GetDriverByName(strDriverName)
    if oDriver == None:
        print("%s 驱动不可用！\n", strDriverName)

    oDS = oDriver.CreateDataSource(fp)  # 创建数据源
    if oDS == None:
        print("创建文件【%s】失败！", fp)
    # 创建空间参考
    srs = osr.SpatialReference()
    srs = spatialRef
    papszLCO = []
    # 创建图层，创建一个多边形图层,"TestPolygon"->属性表名
    oLayer = oDS.CreateLayer("osm_offset", srs, ogr.wkbPolygon, papszLCO)
    if oLayer == None:
        print("图层创建失败！\n")
    '''下面添加矢量数据，属性表数据、矢量数据坐标'''
    oFieldID = ogr.FieldDefn("FieldID", ogr.OFTInteger)  # 创建一个叫FieldID的整型属性
    oLayer.CreateField(oFieldID, 1)
    oFieldName = ogr.FieldDefn("FieldName", ogr.OFTString)  # 创建一个叫FieldName的字符型属性
    oFieldName.SetWidth(100)  # 定义字符长度为100
    oLayer.CreateField(oFieldName, 1)
    oDefn = oLayer.GetLayerDefn()  # 定义要素
    j = 0
    u = 0
    n = 0
    k = len(coornum)
    # print(len(coor))
    # 创建了组成不同线的点集合
    newcoorPoint = [{} for _ in range(k)]
    ring = [{} for _ in range(k)]
    yard = [{} for _ in range(k)]
    for i in coornum:
        # point data:
        u = u + i
        # 点集合切片操作
        newcoorPoint[n] = coor[j:u]
        j = u
        # 构建集合类型：线
        ring[n] = ogr.Geometry(ogr.wkbLinearRing)
        for q in range(len(newcoorPoint[n])):
            ring[n].AddPoint(newcoorPoint[n][q][0], newcoorPoint[n][q][1])  # 添加点
        # 构建集合类型：面
        yard[n] = ogr.Geometry(ogr.wkbPolygon)
        yard[n].AddGeometry(ring[n])
        yard[n].CloseRings()
        n += 1

    oFeatureTriangle = ogr.Feature(oDefn)

    for q in range(len(ring)):
        geomTriangle = ogr.CreateGeometryFromWkt(str(yard[q]))  # 将封闭后的多边形集添加到属性表
        oFeatureTriangle.SetGeometry(geomTriangle)
        oLayer.CreateFeature(oFeatureTriangle)

    oDS.Destroy()
    # print("数据集创建完成！\n")

root = r'D:\spacenet\train'
aois = [os.path.join(root, x) for x in os.listdir(root)]
for aoi in aois:
    if not os.path.isdir(os.path.join(root, aoi)):
        continue
    print(aoi)

    labels_match = os.path.join(aoi, "labels_match")
    img_files = [x for x in os.listdir(labels_match)]
    labels_match_3x = os.path.join(aoi, "labels_3x")
    if not os.path.exists(labels_match_3x):
        os.makedirs(labels_match_3x)
    labels_match_3x_tmp = os.path.join(aoi, "labels_3x_tmp")
    if not os.path.exists(labels_match_3x_tmp):
        os.makedirs(labels_match_3x_tmp)
    masks_3x = os.path.join(aoi, "masks_3x")
    masks_3x_divide = os.path.join(aoi, "masks_3x_divide")
    if not os.path.exists(masks_3x):
        os.makedirs(masks_3x)
    if not os.path.exists(masks_3x):
        os.makedirs(masks_3x)
    if not os.path.exists(masks_3x_divide):
        os.makedirs(masks_3x_divide)
    for img_file in img_files:

        fppath = os.path.join(labels_match,img_file)
        fp = os.path.join(labels_match_3x_tmp,img_file)
        fp2 = os.path.join(labels_match_3x,img_file)

        coor, coornum, spatialRef=data_migration_value(fppath)
        osm_offset_outshp(coor, coornum, spatialRef, fp)

        vector1 = ogr.Open(fppath)
        layer1 = vector1.GetLayer()
        h1 = layer1.GetExtent()
        vector2 = ogr.Open(fp)
        layer2 = vector2.GetLayer()
        h2 = layer2.GetExtent()
        x1 = h1[0]-h2[0]
        y1 = h1[3]-h2[3]
        coor2, coornum2, spatialRef2= data_migration_value2(x1,y1,fp)
        osm_offset_outshp(coor2, coornum2, spatialRef2, fp2)

        inputfilePath2 = fp2  # 输入矢量文件
        outputfile2 = os.path.join(masks_3x,img_file.replace('_Buildings.geojson','.tif'))
        templatefile2 = os.path.join(aoi,'images_masked',img_file.replace('_Buildings.geojson','.tif'))  # 栅格模板文件，确定输出栅格的元数据（坐标系等，栅格大小，范围等）
        vector2raster(inputfilePath2, outputfile2, templatefile2, bands=[1], burn_values=[255], field="",all_touch="False")
        image_path = masks_3x
        out_path = masks_3x_divide
        for image_file in os.listdir(image_path):
            image_one = os.path.join(image_path,image_file)
            caijian(image_one,out_path,image_file)



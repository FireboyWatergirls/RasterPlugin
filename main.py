# -*- coding: utf-8 -*-

#import
import os, sys,struct
import os, sys,struct
from qgis.core import *
from qgis.gui import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QFileDialog,QMessageBox
from ui.mapView import Ui_MainWindow
from ui.resultView2 import Ui_MainWindow as resultView
#from ui.resultView import Ui_Dialog
from osgeo import gdal
from RasterAnalysis_DEM_Information import *
from RasterAnalysis_webLayer import *
from RasterAnalysis_showNDVI import *
from RasterAnalysis_DEM_Information import *
from RasterAnalysis_correlation import *
from RasterAnalysis_RasterData import *

import os, sys,struct
import numpy as np
from osgeo import gdal, gdal_array
from sklearn.cluster import KMeans
from sklearn.cluster import MiniBatchKMeans
import matplotlib.image as mpimg
import cv2
from RasterAnalysis_DEM_Information import DEMInformation
from RasterAnalysis_webLayer import *
from RasterAnalysis_showNDVI import *
from RasterAnalysis_correlation import *
from RasterAnalysis_RasterData import *
from ui.mapView import Ui_MainWindow
from ui.resultView2 import Ui_MainWindow as resultView
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QFileDialog,QMessageBox
from PyQt5.QtGui import QColor
from PyQt5.QtCore import *
from qgis.gui import *
from qgis.core import *
import matplotlib
matplotlib.use("Qt5Agg")  # 声明使用QT5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy

#w问题：如果有多个图层，是只显示选项框里的图层还是全部显示？
##扩展部分
##1 栅格运算：添加计算器
##2 弹出窗口显示结果

# 主题的类
class StyleFile:
    def __init__(self):
        pass

    # @staticmethod
    def readQSS(style):
        with open(style, 'r') as f:
            return f.read()

class MapExplorer(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(MapExplorer, self).__init__()
        self.setupUi(self)
        self.init_mapcanvas()
        self.init_rasterType()
        self.slot_connect()


    #信号和槽的连接
    def slot_connect(self):
        self.actionopen_file.triggered.connect(self.action_open_triggered)
        self.actionzoom_in.triggered.connect(self.action_zoomin_triggered)
        self.actionzoom_out.triggered.connect(self.action_zoomout_triggered)
        self.actionpan.triggered.connect(self.action_pan_triggered)
        self.actionfull_extent.triggered.connect(self.action_fullextent_triggered)
        self.actiondisplay_layers.triggered.connect(self.action_display_layers)
        self.actionsave.triggered.connect(self.action_save_triggered)
        self.action_countndvi.clicked.connect(self.action_count_ndvi_triggered)
        self.input_vector_layer.activated.connect(lambda :self.action_change_layer(1))
        self.input_raster_layer.activated.connect(lambda :self.action_change_layer(0))
        self.WFS.clicked.connect(self.open_WFS_dialog)
        self.WMS.clicked.connect(self.open_WMS_dialog)
        self.ImageData.clicked.connect(self.RasterData)
        self.k_means.clicked.connect(self.build_kmeans)
        self.pushButtonInfor.clicked.connect(self.action_show_information)
        self.pushButtonHis.clicked.connect(self.action_show_histogram)
        self.demRenderType.currentIndexChanged.connect(self.action_change_render_type)
        self.pushButtonRender.clicked.connect(self.action_render_dem)
        self.openXcsv.clicked.connect(self.open_gdp)
        self.openYcsv.clicked.connect(self.open_light)
        self.correlation.clicked.connect(self.linear_regression)
        self.actionAMOLED.triggered.connect(self.action_change_style_amoled)
        self.actionAqua.triggered.connect(self.action_change_style_aqua)
        self.actionConsoleStyle.triggered.connect(self.action_change_style_console)
        self.actionElegantDark.triggered.connect(self.action_change_style_elegant)
        self.actionManjaroMix.triggered.connect(self.action_change_style_mix)
        self.actionMaterialDark.triggered.connect(self.action_change_style_dark)
        self.actionUbuntu.triggered.connect(self.action_change_style_ubuntu)


    def init_rasterType(self):
        self.demRenderType.addItems(["请选择渲染方法", "Singleband gray", "Singleband pseudocolor", "Hillshade"])


    def onCountChanged(self, value):
        self.progressBar.setValue(value)


    def createOutputImage(self, outFilename, inDataset):
        # Define the image driver to be used
        # This defines the output file format (e.g., GeoTiff)
        driver = gdal.GetDriverByName("GTiff")
        # Check that this driver can create a new file.
        metadata = driver.GetMetadata()

        # Get the spatial information from the input file
        geoTransform = inDataset.GetGeoTransform()
        geoProjection = inDataset.GetProjection()
        # Create an output file of the same size as the inputted
        # image, but with only 1 output image band.
        newDataset = driver.Create(outFilename, inDataset.RasterXSize, inDataset.RasterYSize, 1, gdal.GDT_Float32)
        # Define the spatial information for the new image.
        newDataset.SetGeoTransform(geoTransform)
        newDataset.SetProjection(geoProjection)
        return newDataset


    def action_count_ndvi_triggered(self):
        #the function runs a counter thread ( a separate thread)
        print("ndvi")
        self.progressBar.setValue(0)
        #countChanged = pyqtSignal(int)
        #countChanged.connect(self.onCountChanged)
        #combox_R
        #combox_NIR
        print("action_ndvi triggered")
        if self.input_raster_layer.count() == 0:
            print("input_raster = 0")
            msg = QMessageBox()
            print("set msgbox")
            #msg.setIcon(QMessageBox.critical)
            msg.setText("cannot calculate NDVI")
           # msg.setInformativeText("This is additional information")
            msg.setWindowTitle("Error")
            msg.setDetailedText("Please import at least one raster layer")
            msg.setStandardButtons(QMessageBox.Ok)
            returnValue = msg.exec()
            if returnValue == QMessageBox.Ok:
                print('OK clicked')
            return


        outFilePath="./ndvi.tif"
        #可以改的一个地方
        #curLayer= self.input_raster_layer.currentText()
        #layer= QgsProject.instance().mapLayersByName(curLayer)[0]
        #dataset = gdal.Open(layer.dataProvider().dataSourceUri()) 
        #添加可选择波段
        #for i in range(self.rasterDataset.RasterCount):
        #   self.comboBox_R.addItem(str(i))
        #   self.comboBox_NIR.addItem(str(i))
        #self.comboBox_R.addItems(["1","2","3","4"])
        #self.comboBox_NIR.addItems(["1","2","3","4"])

        if self.rasterDataset is None:
            print("The dataset could not opened")
            sys.exit(-1)

            # Create the output dataset
        outDataset = self.createOutputImage(outFilePath, self.rasterDataset)
        # Check the datasets was successfully created.
        if outDataset is None:
            print('Could not create output image')
            sys.exit(-1)

        # Get hold of the RED and NIR image bands from the image
        # Note that the image bands have been hard coded
        # in this case for the Landsat sensor. RED = 3
        # and NIR = 4 this might need to be changed if
        # data from another sensor was used.

        red_band_ind = int(self.comboBox_R.currentText())
        nir_band_ind = int(self.comboBox_NIR.currentText())
        red_band = self.rasterDataset.GetRasterBand(red_band_ind )  # RED BAND
        nir_band = self.rasterDataset.GetRasterBand(nir_band_ind)  # NIR BAND
        # Retrieve the number of lines within the image
        numLines = red_band.YSize
        # Loop through each line in turn.

        self.progressBar.setMaximum(numLines)
        j=0
        for line in range(numLines):
            self.progressBar.setValue(j)
            # Define variable for output line.
            outputLine = bytearray()
            # outputLine=struct.pack('s',outputLines)
            # Read in data for the current line from the
            # image band representing the red wavelength
            red_scanline = red_band.ReadRaster(0, line, red_band.XSize, 1, \
                                               red_band.XSize, 1, gdal.GDT_Float32)
            # Unpack the line of data to be read as floating point data
            red_tuple = struct.unpack('f' * red_band.XSize, red_scanline)

            # Read in data for the current line from the
            # image band representing the NIR wavelength
            nir_scanline = nir_band.ReadRaster(0, line, nir_band.XSize, 1, \
                                               nir_band.XSize, 1, gdal.GDT_Float32)
            # Unpack the line of data to be read as floating point data
            nir_tuple = struct.unpack('f' * nir_band.XSize, nir_scanline)

            # Loop through the columns within the image
            #self.progressBar.setValue(0)

            for i in range(len(red_tuple)):
                # Calculate the NDVI for the current pixel.
                ndvi_lower = (nir_tuple[i] + red_tuple[i])
                ndvi_upper = (nir_tuple[i] - red_tuple[i])
                ndvi = 0
                # Be careful of zero divide
                if ndvi_lower == 0:
                    ndvi = 0
                else:
                    ndvi = ndvi_upper / ndvi_lower
                    # Add the current pixel to the output line
                # outputLine = outputLine + struct.pack('f', ndvi)
                outputLine.extend(struct.pack('f', ndvi))
                # Write the completed line to the output image
            outDataset.GetRasterBand(1).WriteRaster(0, line, red_band.XSize, 1, \
                                                    bytes(outputLine), buf_xsize=red_band.XSize,
                                                    buf_ysize=1, buf_type=gdal.GDT_Float32)
            j=j+1

            # Delete the output line following write
        del outputLine
        self.progressBar.setValue(j)
        print('NDVI Calculated and Outputted to File')
        del outDataset

        self.resultwindow = ResultWindow(outFilePath)
        #resultwindow.fullpath=outFilePath
        self.resultwindow.show()


        #t弹出新的窗口 显示图层！


    def init_mapcanvas(self):
        self.mapCanvas = QgsMapCanvas()
        self.mapCanvas.xyCoordinates.connect(self.show_lonlat)
        self.mapCanvas.setCanvasColor(Qt.white)
        # self.mapCanvas.show()
        layout = QVBoxLayout(self.mapWidget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.mapCanvas)


    def loadMap(self, fullpath):
        self.progressBar.setValue(0)
        self.progressBar.setMaximum(20)
        print(fullpath)
        info=QFileInfo(fullpath)
        basename=info.baseName()
        suffix=info.suffix()
        if suffix == 'shp':
            # 打开矢量图层
            self.layer = QgsVectorLayer(fullpath, basename, "ogr")
            if not self.layer:
                print("failed")
            # 添加下拉框
        else:
            #打开栅格图层
            self.layer = QgsRasterLayer(fullpath, basename,"gdal")
            if not self.layer:
                print("failed")
            # 添加下拉框
            self.fill_combo_box_band()
        # 注册图层
        QgsProject.instance().addMapLayer(self.layer)
        layers=QgsProject.instance().mapLayers()
        layerList=[]
        for i in range(1,20):
            self.progressBar.setValue(i)
        for layer in layers.values():
            layerList.append(layer)
        self.mapCanvas.setLayers(layerList)
        #设置图层范围
        self.mapCanvas.setExtent(self.layer.extent())
        self.mapCanvas.refresh()
        self.fill_combo_box_with_layers(self.input_vector_layer,self.input_raster_layer)
        for i in range(11,21):
            self.progressBar.setValue(i)
        #curLayer = self.input_raster_layer.currentText()
        #layer = QgsProject.instance().mapLayersByName(curLayer)[0]


    def action_open_triggered(self):
        fullpath, format = QFileDialog.getOpenFileName(self, '打开数据', '', '*.shp;;remote sensing image(*.tif *.tiff);;image(*.jpg *.jpeg *.png *.bmp)')
        if os.path.exists(fullpath):
            self.loadMap(fullpath)


    def action_save_triggered(self):
        fullpath,format = QFileDialog.getSaveFileName(self,'保存数据','','*.tif')
        self.mapCanvas.saveAsImage(fullpath)


    def action_zoomin_triggered(self):
        self.maptool = QgsMapToolZoom(self.mapCanvas, False)
        self.mapCanvas.setMapTool(self.maptool)


    def action_zoomout_triggered(self):
        self.maptool = QgsMapToolZoom(self.mapCanvas, True)
        self.mapCanvas.setMapTool(self.maptool)


    def action_pan_triggered(self):
        self.maptool = QgsMapToolPan(self.mapCanvas)
        self.mapCanvas.setMapTool(self.maptool)


    def action_fullextent_triggered(self):
        self.mapCanvas.setExtent(self.layer.extent())
        self.mapCanvas.refresh()


    def action_display_layers(self):
        layers = QgsProject.instance().mapLayers()
        layerList = []
        for layer in layers.values():
            layerList.append(layer)
        self.mapCanvas.setLayers(layerList)
        # 设置图层范围
        self.mapCanvas.setExtent(self.layer.extent())
        self.mapCanvas.refresh()


    #显示鼠标点的经纬度信息
    def show_lonlat(self, point):
        x = point.x()
        y = point.y()
        self.statusbar.showMessage(f'经度:{x},纬度:{y}')


    def fill_combo_box_with_layers(self,combo_box_vector, combo_box_raster):
        # Add layers not in the combo box
        for layer in self.mapCanvas.layers():
            if layer.type() == QgsMapLayer.VectorLayer:
                if combo_box_vector.findText(layer.name()) < 0:
                    combo_box_vector.addItem(layer.name())
                    #if layer in QgsLayerTreeView().selectedLayers():
                        #combo_box.setCurrentIndex(combo_box.count() - 1)

        # Remove layers no longer on the map
        removed = []
        for index in range(combo_box_vector.count()):
            found = False
            for layer in self.mapCanvas.layers():
                if layer.name() == combo_box_vector.itemText(index):
                    found = True

                    break
            if not found:
                removed.append(index)

        removed.reverse()
        for index in removed:
            combo_box_vector.removeItem(index)

        # Add layers not in the combo box
        for layer in self.mapCanvas.layers():
            if layer.type() == QgsMapLayer.RasterLayer:
                if combo_box_raster.findText(layer.name()) < 0:
                    combo_box_raster.addItem(layer.name())
                    # if layer in QgsLayerTreeView().selectedLayers():
                    # combo_box.setCurrentIndex(combo_box.count() - 1)

        # Remove layers no longer on the map
        removed = []
        for index in range(combo_box_raster.count()):
            found = False
            for layer in self.mapCanvas.layers():
                if layer.name() == combo_box_raster.itemText(index):
                    found = True
                    break
            if not found:
                removed.append(index)

        removed.reverse()
        for index in removed:
            combo_box_raster.removeItem(index)

        if self.layer.type() == QgsMapLayer.RasterLayer:
            combo_box_raster.setCurrentText(self.layer.name())
        else:
            combo_box_vector.setCurrentText(self.layer.name())


    def build_kmeans(self):
        # 没有什么循环，所以做了个假的进度条
        print("当前值为：", self.clusterNumber.value())
        if self.input_raster_layer.count() == 0:
            print("无矢量图层数据")
            sys.exit(-1)
        self.img = gdal.Open(self.layer.dataProvider().dataSourceUri())
        if self.img is None:
            print("数据加载失败")
            sys.exit(-1)
        self.progressBar.setValue(0)
        print(self.img.RasterYSize)
        self.progressBar.setMaximum(100)

        print(self.selectClusterBand.currentText())
        if self.selectClusterBand.currentText() == "全波段":
            self.tmpimg = np.zeros((self.img.RasterYSize, self.img.RasterXSize, self.img.RasterCount),
                                   gdal_array.GDALTypeCodeToNumericTypeCode(self.img.GetRasterBand(1).DataType))
            j = 0
            for b in range(self.tmpimg.shape[2]):
                self.tmpimg[:, :, b] = self.img.GetRasterBand(b+1).ReadAsArray()
                self.progressBar.setValue(b)
                j = b
            self.new_shape = (self.tmpimg.shape[0] * self.tmpimg.shape[1], self.tmpimg.shape[2])
            x = self.tmpimg[:, :, :13].reshape(self.new_shape)
            print("1")
            if self.clusterNumber.value() == 0:
                print("聚类数不可为0")
                sys.exit(-1)
            k_means = KMeans(n_clusters=self.clusterNumber.value())
            k_means.fit(x)
            self.progressBar.setValue(99)
            # for j in range(30, 78):
            #     self.progressBar.setValue(j)
            #     j = j + 1
            x_cluster = k_means.labels_
            x_cluster = x_cluster.reshape(self.tmpimg[:, :, 0].shape)
        elif self.selectClusterBand.currentText() == "波段1":
            band = self.img.GetRasterBand(1)
            self.tmpimg = band.ReadAsArray()
            x = self.tmpimg.reshape((-1, 1))
            if self.clusterNumber.value() == 0:
                print("聚类数不可为0")
                sys.exit(-1)
            self.progressBar.setValue(84)
            k_means = KMeans(n_clusters=self.spinBox.value())
            k_means.fit(x)
            # for j in range(30, 78):
            #     self.progressBar.setValue(j)
            #     j = j + 1
            x_cluster = k_means.labels_
            self.progressBar.setValue(96)
            x_cluster = x_cluster.reshape(self.tmpimg.shape)
        elif self.selectClusterBand.currentText() == "波段2":
            band = self.img.GetRasterBand(2)
            self.tmpimg = band.ReadAsArray()
            self.progressBar.setValue(77)
            x = self.tmpimg.reshape((-1, 1))
            if self.clusterNumber.value() == 0:
                print("聚类数不可为0")
                sys.exit(-1)
            k_means = KMeans(n_clusters=self.spinBox.value())
            k_means.fit(x)
            # for j in range(30, 78):
            #     self.progressBar.setValue(j)
            #     j = j + 1
            x_cluster = k_means.labels_
            self.progressBar.setValue(93)
            x_cluster = x_cluster.reshape(self.tmpimg.shape)
        else:
            band = self.img.GetRasterBand(3)
            self.tmpimg = band.ReadAsArray()
            x = self.tmpimg.reshape((-1, 1))
            if self.clusterNumber.value() == 0:
                print("聚类数不可为0")
                sys.exit(-1)
            k_means = KMeans(n_clusters=self.clusterNumber.value())
            k_means.fit(x)
            # for j in range(30, 78):
            #     self.progressBar.setValue(j)
            #     j = j + 1
            x_cluster = k_means.labels_
            x_cluster = x_cluster.reshape(self.tmpimg.shape)

        print("保存")
        cv2.imwrite('generated.tif', x_cluster)
        # self.progressBar.setValue(99)
        self.resultwindow = ResultWindow('generated.tif')
        self.progressBar.setValue(100)
        # resultwindow.fullpath=outFilePath
        self.resultwindow.show()


    def action_change_layer(self,flag):
        vector_layer=self.find_layer(self.input_vector_layer.currentText())
        raster_layer = self.find_layer(self.input_raster_layer.currentText())
        if flag == 1:
            self.layer=vector_layer
        else:
            self.layer=raster_layer
            #更新NDVI下拉框
            self.fill_combo_box_band()
        self.mapCanvas.setLayers([vector_layer,raster_layer])
        self.mapCanvas.setExtent(self.layer.extent())
        self.mapCanvas.refresh()


    def find_layer(self, layer_name):
        if not layer_name:
            return None

        layers = QgsProject.instance().mapLayersByName(layer_name)
        print(layers)
        if (len(layers) >= 1):
            return layers[0]

        return None


    def fill_combo_box_band(self):
        if self.layer.name() != 'wms layer':
            self.rasterDataset = gdal.Open(self.layer.dataProvider().dataSourceUri())
            # 添加可选择波段
            self.comboBox_R.clear()
            self.comboBox_NIR.clear()
            for i in range(self.rasterDataset.RasterCount):
                self.comboBox_R.addItem(str(i + 1))
                self.comboBox_NIR.addItem(str(i + 1))


    def open_WFS_dialog(self):
        self.WFSdialog = wfsLayer()
        self.WFSdialog.show()
        self.WFSdialog.wfsLayerSignal.connect(self.add_WFS_layer)


    def add_WFS_layer(self,wfsLayer):
        self.progressBar.setValue(0)
        self.progressBar.setMaximum(100)
        self.layer=wfsLayer
        QgsProject.instance().addMapLayer(self.layer)
        layers = QgsProject.instance().mapLayers()
        layerList = []
        for i in range(1, 60):
            self.progressBar.setValue(i)
        for layer in layers.values():
            layerList.append(layer)
        self.mapCanvas.setLayers(layerList)
        # 设置图层范围
        for i in range(61, 80):
            self.progressBar.setValue(i)
        self.mapCanvas.setExtent(self.layer.extent())
        self.mapCanvas.refresh()
        self.fill_combo_box_with_layers(self.input_vector_layer, self.input_raster_layer)
        for i in range(81, 101):
            self.progressBar.setValue(i)


    def open_WMS_dialog(self):
        self.WMSdialog = xyzTileLayer()
        self.WMSdialog.show()
        self.WMSdialog.xyzLayerSignal.connect(self.add_WMS_layer)


    def add_WMS_layer(self,wmsLayer):
        self.progressBar.setValue(0)
        self.progressBar.setMaximum(100)
        self.layer=wmsLayer
        QgsProject.instance().addMapLayer(self.layer)
        layers = QgsProject.instance().mapLayers()
        layerList = []
        for i in range(1, 20):
            self.progressBar.setValue(i)
        for layer in layers.values():
            layerList.append(layer)
        self.mapCanvas.setLayers(layerList)
        for i in range(21, 60):
                self.progressBar.setValue(i)
        # 设置图层范围
        self.mapCanvas.setExtent(self.layer.extent())
        self.mapCanvas.refresh()
        self.fill_combo_box_with_layers(self.input_vector_layer, self.input_raster_layer)
        for i in range(61, 101):
            self.progressBar.setValue(i)


    def RasterData(self):
        self.progressBar.setValue(0)
        self.progressBar.setMaximum(100)
        layer = self.find_layer(self.input_raster_layer.currentText())
        wave=int(self.comboBox_R.currentText())
        out = raster_stat_unique_count(layer,wave)
        print()
        value = []
        count = []
        for i in range(1, 20):
            self.progressBar.setValue(i)
        for k in sorted(out.keys()):
            # print("value = ", k, '\t, count = ', out[k])
            if (k<1000):
                value.append(k)
                count.append(out[k])
        for i in range(21, 60):
            self.progressBar.setValue(i)
        histogram_draw(value, count)
        for i in range(61,101):
            self.progressBar.setValue(i)


    def action_show_information(self):
        self.progressBar.setValue(0)
        self.progressBar.setMaximum(1)
        p = self.layer.dataProvider()
        p.initHistogram(QgsRasterHistogram(), 1, 100)
        h = p.histogram(1)

        # 获取栅格类型
        def switch_case(value):
            switcher = {
                0: "灰度值（单波段）",
                1: "调色板（单波段）",
                2: "多波段",
                3: "网格"
            }
            return switcher.get(value, 'wrong value')
        rasterType = switch_case(self.layer.rasterType())
        basename = self.layer.name()

        # 传值给基本信息窗口
        self.dem_dialog = DEMInformation()
        self.dem_dialog.textName.setText(basename)
        self.dem_dialog.textWidth.setText(str(self.layer.width()))
        self.dem_dialog.textHeight.setText(str(self.layer.height()))
        self.dem_dialog.textExtent.setText(self.layer.extent().toString())
        self.dem_dialog.textMax.setText(str(h.maximum))
        self.dem_dialog.textMin.setText(str(h.minimum))
        self.dem_dialog.textBandNum.setText(str(self.layer.bandCount()))
        self.dem_dialog.textType.setText(rasterType)
        self.dem_dialog.show()
        self.progressBar.setValue(1)


    def action_show_histogram(self):
        self.progressBar.setValue(0)
        self.progressBar.setMaximum(2)
        # 绘制高程直方图
        p = self.layer.dataProvider()
        p.initHistogram(QgsRasterHistogram(), 1, 100)
        h = p.histogram(1)
        array = h.histogramVector
        index = numpy.arange(h.minimum, h.maximum + 1, 1)
        self.progressBar.setValue(1)
        plt.bar(index, array)
        plt.title('Histogram')
        plt.show()
        self.progressBar.setValue(2)


    def action_change_render_type(self, index):
        self.progressBar.setValue(0)
        currentIndex = self.demRenderType.currentIndex()
        self.single_band_gray_renderer_widget = QgsSingleBandGrayRendererWidget(self.layer)
        self.single_band_pseudo_color_renderer_widget = QgsSingleBandPseudoColorRendererWidget(self.layer)
        self.hillshade_renderer_widget = QgsHillshadeRendererWidget(self.layer)
        if currentIndex == 1:
            self.single_band_gray_renderer_widget.setVisible(True)
            self.single_band_pseudo_color_renderer_widget.setVisible(False)
            self.hillshade_renderer_widget.setVisible(False)
        elif currentIndex == 2:
            self.single_band_gray_renderer_widget.setVisible(False)
            self.single_band_pseudo_color_renderer_widget.setVisible(True)
            self.hillshade_renderer_widget.setVisible(False)
        elif currentIndex == 3:
            self.single_band_gray_renderer_widget.setVisible(False)
            self.single_band_pseudo_color_renderer_widget.setVisible(False)
            self.hillshade_renderer_widget.setVisible(True)


    def action_render_dem(self):
        self.progressBar.setValue(0)
        self.progressBar.setMaximum(1)
        currentIndex = self.demRenderType.currentIndex()
        if currentIndex == 1:
            self.render = self.single_band_gray_renderer_widget.renderer()
            self.layer.setRenderer(self.render)
            self.layer.triggerRepaint()
            self.progressBar.setValue(1)
        elif currentIndex == 2:
            self.render = self.single_band_pseudo_color_renderer_widget.renderer()
            self.layer.setRenderer(self.render)
            self.layer.triggerRepaint()
            self.progressBar.setValue(1)
        elif currentIndex == 3:
            self.render = self.hillshade_renderer_widget.renderer()
            self.layer.setRenderer(self.render)
            self.layer.triggerRepaint()
            self.progressBar.setValue(1)
        else:
            print('请选择渲染方式')


    def open_gdp(self):
        fullpath, format = QFileDialog.getOpenFileNames(self, '打开数据', '', '*.csv')
        gdp_data_temp = pd.read_csv(fullpath[0], encoding='gbk').iloc[:, :2].dropna(axis=0, how='any')
        gdp_data_temp = gdp_data_temp.to_dict(orient='index')
        years = None
        for i in gdp_data_temp[0].keys():
            if i != '地区' and 'Unnamed' not in i:
                years = i
                break
        if years is None:
            print('数据有问题！')
        else:
            self.gdp_dict = {}
            for i in range(len(gdp_data_temp)):
                self.gdp_dict[gdp_data_temp[i]['地区']] = gdp_data_temp[i][years]
        self.lineEditX.setText(fullpath[0])


    def open_light(self):
        fullpath, format = QFileDialog.getOpenFileNames(self, '打开数据', '', '*.csv')
        light_data_temp = pd.read_csv(fullpath[0], encoding='gbk').iloc[:, :2].dropna(axis=0, how='any')
        light_data_temp = light_data_temp.to_dict(orient='index')
        self.light_dict = {}
        for i in range(len(light_data_temp)):
            self.light_dict[light_data_temp[i]['地区']] = light_data_temp[i]['亮度']
        self.lineEditY.setText(fullpath[0])


    def linear_regression(self):
        # self.light_dict和self.gdp_dict都是{城市名:值}
        data = []
        for k, v in self.gdp_dict.items():
            data.append([v, self.light_dict[k]])
        # data.sort()
        x = []
        y = []
        for i in data:
            x.append([i[0]])
            y.append([i[1]])
        reg = LinearRegression()
        reg.fit(x, y)
        X = list(range(int(min([i[0] for i in x])), int(max([i[0] for i in x]))))
        Y = reg.predict(np.reshape(X, (-1, 1)))
        self.plot_widget = PlotLinear()
        self.plot_widget.plot(x, y, X, Y)


    def action_change_style_amoled(self):
        style_file = 'qss/AMOLED.qss'
        self.style = StyleFile.readQSS(style_file)
        self.setStyleSheet(self.style)

    def action_change_style_aqua(self):
        style_file = 'qss/Aqua.qss'
        self.style = StyleFile.readQSS(style_file)
        self.setStyleSheet(self.style)

    def action_change_style_console(self):
        style_file = 'qss/ConsoleStyle.qss'
        self.style = StyleFile.readQSS(style_file)
        self.setStyleSheet(self.style)

    def action_change_style_elegant(self):
        style_file = 'qss/ElegantDark.qss'
        self.style = StyleFile.readQSS(style_file)
        self.setStyleSheet(self.style)

    def action_change_style_mix(self):
        style_file = 'qss/ManjaroMix.qss'
        self.style = StyleFile.readQSS(style_file)
        self.setStyleSheet(self.style)

    def action_change_style_dark(self):
        style_file = 'qss/MaterialDark.qss'
        self.style = StyleFile.readQSS(style_file)
        self.setStyleSheet(self.style)

    def action_change_style_ubuntu(self):
        style_file = 'qss/Ubuntu.qss'
        self.style = StyleFile.readQSS(style_file)
        self.setStyleSheet(self.style)


def main():
    qgs = QgsApplication([], True)
    qgs.setPrefixPath('qgis', True)
    #启动QGIS
    qgs.initQgis()

    window = MapExplorer()
    window.show()

    exit_code = qgs.exec_()
    #退出QGIS
    qgs.exitQgis()
    sys.exit(exit_code)


if __name__ == '__main__':
    main()








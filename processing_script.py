# -*- coding: utf-8 -*-
"""
Created on Wed May  4 13:38:13 2022

@author: au526889
"""

import os

from qgis import processing

from qgis.core import (
  QgsApplication,
  QgsDataSourceUri,
  QgsCategorizedSymbolRenderer,
  QgsClassificationRange,
  QgsPointXY,
  QgsProject,
  QgsExpression,
  QgsField,
  QgsFields,
  QgsFeature,
  QgsFeatureRequest,
  QgsFeatureRenderer,
  QgsGeometry,
  QgsGraduatedSymbolRenderer,
  QgsMarkerSymbol,
  QgsMessageLog,
  QgsRectangle,
  QgsRendererCategory,
  QgsRendererRange,
  QgsSymbol,
  QgsVectorDataProvider,
  QgsVectorLayer,
  QgsVectorFileWriter,
  QgsWkbTypes,
  QgsSpatialIndex,
  QgsVectorLayerUtils
)


class InputPoints():
    
    def __init__(self,
                 pts,
                 temp_dir):
        
        self.pts = pt
        
        self.temp_dir = temp_dir
        
        
    
    def buff(self,
             buff_dist):
        
        p = processing.run('native:buffer',{'INPUT': self.points,
                                            'DISTANCE': buff_dist,
                                            'SEGMENTS':25,
                                            'DISSOLVE':True,
                                            'END_CAP_STYLE':0,
                                            'JOIN_STYLE':0,
                                            'MITER_LIMIT':10,
                                            'OUTPUT':os.path.join(self.temp_dir,'buffers.shp')
                                            })
        
        return p['OUTPUT']
    
    def centroids(self,
                  buffers):
        
        p = processing.run('native:centroids',{'INPUT':buffers,
                                               'ALL_PARTS':True,
                                               'OUTPUT':os.path.join(self.temp_dir,'centroids.shp')
                                               })
                                               
        return p['OUTPUT']
        
    
        
    def run(self,
            buff_dist=25000):
        
        buffers = self.buff(buff_dist)
        
        centroids = self.centroids(buffers)
        
        return centroids
        
    
class LCP():
    
    def __init__(self,
                 points,
                 elevation,
                 friction,
                 temp_dir,
                 output_dir):
        
        self.points = QgsVectorLayer(points, "points", "ogr")
        self.elevation = elevation
        self.friction = friction
        self.temp_dir = temp_dir
        self.output_dir = output_dir
        
    def walk(self,
             point):
        
        p = processing.run('grass7:r.walk.coords',{'elevation':self.elevation,
                                                   'friction':self.friction,
                                                   'start_coordinates':self.})
        
        
        
        pass
    
    def drain(self):
        pass
    
    def cleanup(self):
        pass
    
    def run(self,
            cleanup=False):
        
        features = self.pts.getFeatures()
        
        for f in features:
            geom = f.geometry()
            pt = geom.asPoint()
            
            
    


    



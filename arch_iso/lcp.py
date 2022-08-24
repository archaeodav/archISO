# -*- coding: utf-8 -*-
"""
Created on Mon May 23 12:57:24 2022

@author: au526889
"""


import os
print ('OK')
import json
print ('OK')
from qgis import processing
print ('OK')
from qgis.processing import alg
print ('OK')
from qgis.core import (QgsProject,
                       QgsVectorLayer)
print ('OK')

import shutil
print ('OK')
    
    
class leastCostPath:
    
    def __init__(self,
                points,
                dtm,
                friction,
                outdir):
        
        self.points = points
        
        self.dtm = dtm
        
        self.friction = friction
        
        self.outdir = outdir
        
        self.nodes = None
        
        self.buffers = {}   
        
        self.heirarch_buffers = {}
        
        #self.nodes = self.centroids(self.buffer()['OUTPUT'])
        
        if not os.path.exists(self.outdir):
            os.mkdir(self.outdir)
            
        self.tempdir = os.path.join(self.outdir,'temp')
        
        if not os.path.exists(self.tempdir):
            os.mkdir(self.tempdir)
            
    def buffer(self,
               pts = None,
                distance = 25000,
                segments = 25):
        
         if pts is None:
             pts  =self.points
        
         buffered = processing.run("native:buffer",{'INPUT':pts,
                                                    'DISTANCE':distance,
                                                    'SEGMENTS':segments,
                                                    'DISSOLVE':True})
         
         count = processing.run('native:countpointsinpolygon',{'POLYGONS':buffered['OUTPUT'],
                                                               'POINTS':self.points})
         
         return count
     
     
    def centroids(self,
                   polys,
                   outfile = None):
         
         centroids = processing.run("native:centroids",{'INPUT':polys})
         
         return centroids
     
     
    def iterative_buffer(self,
                         start_distance = 20000,
                         factor = 2):
        
        #get number of points so we know where to stop
        pts = QgsVectorLayer(self.points,'nodes','ogr')
        
        max_points = pts.featureCount()
        
        distance = start_distance
        
        num_polys = 100000
        
        while num_polys >1:
            b = self.buffer(self.points,
                     distance = distance)
            
            self.buffers[distance]=b
            
            b_polys = QgsVectorLayer(b['OUTPUT'],'buff','ogr')
            
            num_polys = b_polys.featureCount()
            
            distance = distance*factor   
            

    def heirarchy(self):
        
        keys_sorted = list(self.buffers.keys()).sort()
        
        #keys_sorted.reverse()
        
        n_levels = len(keys_sorted)
        
        '''for idx,key in emumerate(keys_sorted):
            if idx+1 < n_levels:
                this_layer = QgsVectorLayer(self.buffers[key],
                                            'this',
                                            'ogr')
                
                next_layer = QgsVectorLayer(self.buffers[keys_sorted[idx+1]],
                                            'next',
                                            'ogr')'''
                                                      
    def subset(self,
               in_raster,
               in_vector,
               oname):
                   
        in_raster = QgsRasterLayer(in_raster,'in_raster', 'gdal')
        
        print (in_raster, 
               in_raster.width(), 
               in_raster.height(),
               in_raster.extent())
        
        in_vector = QgsVectorLayer(in_vector,'in_vector', 'ogr')
        
        print (in_vector)
        
        output = os.path.join(self.tempdir,oname)
        
        #out_raster = QgsRasterLayer(output,'out_raster', 'gdal')
        
        subset = processing.run("gdal:cliprasterbyextent",{'INPUT':in_raster,
                                                           'PROJWIN':in_vector,
                                                           'OUTPUT':output})
        
        return subset['OUTPUT']
    
    
    def walk(self,
             dtm,
             friction,
             pt,
             cost_out,
             direction_out,
             walk_coeff='1.1,6.0,1.9998,-1.9998',
             l=1,
             slope_factor=-0.2125,
             null_cost=0.02,
             memory = 25000,
             k = True,
             n = False):  
                 
      '''dtm = QgsRasterLayer(dtm,'dtm', 'gdal')
      friction = QgsRasterLayer(friction,'friction', 'gdal')'''
      
    
      w = processing.run("grass7:r.walk.coords",{'elevation':dtm,
                                                 'friction':friction,
                                                 'start_coordinates':pt,
                                                 'output':cost_out,
                                                 'outdir':direction_out,
                                                 'walk_coeff':walk_coeff,
                                                 'lambda':l,
                                                 'slope_factor':slope_factor,
                                                 'null_cost':null_cost,
                                                 'memory':memory,
                                                 '-k':k,
                                                 '-n':n})
      
      #cost = w['output'],direction = w['outdir']
      
      return w
  
    
    def lcp(self,
          cost,
          direction,
          start_points,
          output,
          drain,
          c=False,
          a=True,
          n= False,
          d=True,
          ):
      
      d = processing.run("grass7:r.drain",{'input':cost,
                                           'direction':direction,
                                           'start_points':start_points,
                                           'output':output,
                                           'drain':drain,
                                           '-c':c,
                                           '-a':a,
                                           '-n':n,
                                           '-d':d})
      # 'output' = raster lcp 'drain' = vector lcp
      
      return d
  
    
    def tidy_up(self):
      shutil.rmtree(self.tempdir)
      
      
    def run_whole(self,
                  tidyup = True):
      print ('Subsetting DTM')
      print (self.dtm, self.points)
      dtm = self.subset(self.dtm, self.points,'dtm.tif')
      print (dtm)
      print ('Subsetting Friction')
      friction = self.subset(self.friction,self.points,'friction.tif')
      print (friction)
      
      print ('Loading Points')
      points = QgsVectorLayer(self.points,'nodes','ogr')
      
      features = points.getFeatures()
      
      print ('Iterating points')
      for feature in features:
          fid = feature.id()
          
          pt = feature.geometry()
          
          pt = pt.asPoint()
          
          pt_string = '%s,%s' %(pt.x(),pt.y())
          
          cost = os.path.join(self.tempdir,
                              'cost_%s.tif' %(fid))
          
          direction = os.path.join(self.tempdir,
                                   'direction_%s.tif' %(fid))
          
          walk = self.walk(dtm,
                           friction,
                           pt_string,
                           cost,
                           direction)
          
          lcp_rast = os.path.join(self.tempdir,
                                  'lcp_%s.tif' %(fid))
          
          lcp_vect = os.path.join(self.outdir,
                                  'lcp_%s.shp' %(fid))
          
          drain = self.lcp(walk['output'],
                           walk['outdir'],
                           self.points,
                           lcp_rast,
                           lcp_vect)
          
      if tidyup is True:
          self.tidyup()
      
      return drain
          
          
          
def test():
    l = leastCostPath(r'C:/Users/au526889/Dropbox/GIS female mobility/test_data/typ1.shp',
                      r'C:/Users/au526889/Dropbox/GIS female mobility/test_data/50m_dtm.tif',
                      r'C:/Users/au526889/Dropbox/GIS female mobility/test_data/friction.tif',
                      r'E:/EBA_MOB_TEST')
    
    l.run_whole(tidyup=False)
          
        
     
        
        
        
        
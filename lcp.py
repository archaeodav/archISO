# -*- coding: utf-8 -*-
"""
Created on Mon May 23 12:57:24 2022

@author: au526889
"""


import os
import json
from qgis import processing
from qgis.processing import alg
from qgis.core import (QgsProject,
                       QgsVectorLayer)


    
    
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
        
        
        self.nodes = self.centroids(self.buffer()['OUTPUT'])
        
        if not os.path.exists(self.outdir):
            os.mkdir(self.outdir)
            
        
        self.tempdir = os.path.join(self.outdir,'temp')
        
        if not os.path.exists(self.tempdir):
            os.mkdir(self.tempdir)
            
        
            

    def buffer(self,
               pts = None,
                distance = 25000,
                segments = 25):
        
         if pts is None;:
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
     
     
    def n_hood(self,
               distance=100000)
    
        
     
     
    
    def point_collector(self,
                       min_clust=3):
        pts = QgsVectorLayer(self.nodes,'nodes','ogr')
        
        features in pts.getFeatures()
        
        
        for f in features:
            pass
        
            # if f['NUMPOINTS']
                #run walk 
        
        
    def walk(self,
             pt,
             walk_coeff='1.1,6.0,1.9998,-1.9998',
             l=1,
             slope_factor,
             null_cost=0.02,
             memory = 25000,
             k = True,
             n = False):  
      w = processing.run("grass7:r.walk.points",{'elevation':self.dtm,
                                                 'friction':self.friction,
                                                 'start_points':pt,
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
          c=False,
          a=True,
          n= False
          d=True,
          ):
      
      d = processing.run("grass7:r.drain",{'input':cost,
                                           'direction':direction,
                                           'start_points':start_points,
                                           '-c':c,
                                           '-a':a,
                                           '-n':a,
                                           '-d':d})
      # 'output' = raster lcp 'drain' = vector lcp
      
      return d
      
      
     
      
     
        
        
        
        
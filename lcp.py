# -*- coding: utf-8 -*-
"""
Created on Mon May 23 12:57:24 2022

@author: au526889
"""


import os
import json
from qgis import processing
from qgis.processing import alg
from qgis.core import QgsProject


    
    
class leastCostPath:
    
    def __init__(self,
                points,
                dtm,
                cost_surface,
                outdir):
        
        self.points = points
        
        self.dtm = dtm
        
        self.cost_surface = cost_surface
        
        self.outdir = outdir
        
        self.nodes = None
        
        
        self.nodes = self.centroids(self.buffer()['OUTPUT'])
        
        if not os.path.exists(self.outdir):
            os.mkdir(self.outdir)
            
        
        self.tempdir = os.path.join(self.outdir,'temp')
        
        if not os.path.exists(self.tempdir):
            os.mkdir(self.tempdir)
            
        
            

    def buffer(self,
                distance = 25000,
                segments = 25):
         buffered = processing.run("native:buffer",{'INPUT':self.points,
                                                    'DISTANCE':distance,
                                                    'SEGMENTS':segments,
                                                    'DISSOLVE':True})
         
         return buffered
     
     
    def centroids(self,
                   polys,
                   outfile = None):
         
         centroids = processing.run("native:centroids",{'INPUT':polys})
         
         return centroids 
    
    def pointItereator(self):
        
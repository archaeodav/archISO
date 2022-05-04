# -*- coding: utf-8 -*-
"""
Created on Wed May  4 13:38:13 2022

@author: au526889
"""

import os

from qgis import processing


from qgis.core import (QgsProcessingAlgorithm,
       QgsProcessingParameterNumber,
       QgsProcessingParameterFeatureSource,
       QgsProcessingParameterFeatureSink)


class rWalk(QgsProcessingAlgorithm):
    
    def __init__(self):
        super().__init__()
        
    def name(self):
        return "rWalk"
    
    def displayName(self):
        return "rWalk Script"
    
    def createInstance(self):
        retrun type(self)()
        
    
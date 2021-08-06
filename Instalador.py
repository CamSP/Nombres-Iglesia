# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 21:15:01 2021

@author: Camilo
"""

import sys
import subprocess


subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
'Pillow'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
'tk'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
'aerender'])

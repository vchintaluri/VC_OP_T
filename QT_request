#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 19:37:44 2019

@author: bhaskarnamrata
"""



import pickle
from datetime import datetime
from qt_funcs import qt_analysis

obj = qt_analysis()
q = obj.qt_connect()
obj.get_account(q)
obj.get_positions(q)
obj.enrich_positions(q)
obj.summarize_positions()

pickle.dump(obj, open('{0}_{1}'.format('qt_obj', datetime.now().date()), "wb"))

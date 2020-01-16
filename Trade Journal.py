#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  7 15:16:27 2019

@author: bhaskarnamrata
"""

from New_Struct import portfolio
from datetime import datetime
from os import path
import pprint

def main():
    
    p = portfolio()
    underlying = input('Underlying:')
    expiry_date = datetime.strptime(input('Expiry Date(yyyymmdd):'), '%Y%m%d').date()
    
    if path.exists('{0}_{1}'.format(underlying, expiry_date)):
        p = p.load_object(underlying, expiry_date)
        
    else:
        p.save_object(p, underlying, expiry_date)
    
    while input('Add Trades(Y/N):') == 'Y':
        current_positions = len(p.Strategy['Legs_Detail'])
        p.initialize_legs()
        new_positions = len(p.Strategy['Legs_Detail'])
        print ('{0} positions added.'.format(new_positions - current_positions))
        p.save_object(p, underlying, expiry_date)
        

    
  
    while input('Update Position(Y/N):') == 'Y':
        p.update_mkt_val(input('Option Type:'))
        
    
    p.save_object(p, underlying, expiry_date)
    pprint.pprint(p.Strategy['Legs_Detail'])

 
    
if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 19:52:13 2019

@author: bhaskarnamrata
"""
from datetime import datetime
import pickle

class portfolio:
    def __init__(self):
       
        self.Strategy = {
                        "Legs" : 2,
                        "Entry Date" : "",
                        "Name" : "Veritical Spread",
                        "Max Profit" : 0.00,
                        "Max Loss" : 0.00,
                        "Spread" : 5.00,
                        "Bias" : "Bear",
                        "Instrument" : "SPY",
                        "Iteration" : 0,
                        "PnL" : 0.00,
                        "Legs_Detail" : {},
                        }
    
        self.Leg = {
                   "Status" : "Open",
                   "Last Update Date" : 19000000,
                   "Close Price": 0.00,
                   "Credit" : "Yes",
                   "Short Strike" : 0.0,
                   "Short Strike Price": 0.0,
                   "Long Strike Price":0.0,
                   "Long Strile" : 0.0,
                   "Option Type" : 'Call',
                   "Expiry Date" : 19000000,
                   "Entry Date" : 19000000,
                   "Instrument" : "SPY",
                   "Price Entry" : 0.00,
                   "Mkt Val" : 0.00,
                   "Short Strike Mkt Val" : 0.00,
                   "Long Strike Mkt Val" : 0.00,
                   "Spread" : 5.00,
                   "Max Profit": 0.00,
                   "Max Loss": 0.00,
                   "PnL": 0.00,
                   "DTE": 0,
                   "Iteration" : 0,
                   }
                
                
        
    def initialize_legs(self):
        self.Strategy['Legs'] = int(input('Number of Legs:'))
        for i in range(self.Strategy['Legs']):
            self.Leg['Entry Date'] = datetime.strptime(input('Input Date(yyyymmdd):'), '%Y%m%d').date()
            self.Leg['Option Type'] = input('Option Type:')
            self.Leg['Instrument'] = input('Instrument Name:')
            self.Leg['Credit'] = input('Credit (Y/N):')
            self.Leg['Short Strike'] = int(input('Short Strike Value:'))
            self.Leg['Short Strike Price'] = int(input('Short Strike Price:'))
            self.Leg['Long Strike'] = int(input('Long Strike Value:'))
            self.Leg['Long Strike Price'] = int(input('Long Strike Price:'))
            self.Leg['Expiry Date'] = datetime.strptime(input('Expiry Date(yyyymmdd):'), '%Y%m%d').date()
            
            
            if self.Leg['Credit'] == 'Y':
                self.Leg['Price Entry'] = abs(self.Leg['Short Strike Price'] - self.Leg['Long Strike Price'])
                self.Leg['Spread'] = abs(100*(self.Leg['Long Strike'] - self.Leg['Short Strike']))    
                self.Leg['Max Profit'] = self.Leg['Price Entry']
                self.Leg['Max Loss'] = abs(self.Leg['Spread'] - self.Leg['Price Entry'])
                
                
            else:
                self.Leg['Price Entry'] = abs(self.Leg['Long Strike Price'] - self.Leg['Short Strike Price'])
                self.Leg['Spread'] = abs(100*(self.Leg['Short Strike'] - self.Leg['Long Strike']))
                self.Leg['Max Profit'] = abs(self.Leg['Spread'] - self.Leg['Price Entry'])
                self.Leg['Max Loss'] = self.Leg['Price Entry']
            
            self.Leg['DTE'] = (self.Leg['Expiry Date'] - self.Leg['Entry Date']).days
            self.Strategy['Legs_Detail']['{0}'.format(self.Leg['Option Type'])] = self.Leg.copy() 
        
    def update_mkt_val(self, option_type):
        key = option_type
        self.Strategy['Legs_Detail'][key]['Last Update Date'] = datetime.now().date()
        self.Strategy['Legs_Detail'][key]['Short Strike Mkt Val'] = int(input('Enter Short Strike Mkt Value:'))
        self.Strategy['Legs_Detail'][key]['Long Strike Mkt Val'] = int(input('Enter Long Strike Mkt Value:'))
        self.Strategy['Legs_Detail'][key]['DTE'] = (self.Strategy['Legs_Detail'][key]['Expiry Date'] - self.Strategy['Legs_Detail'][key]['Last Update Date']).days
        
        if self.Strategy['Legs_Detail'][key]['Credit'] == 'Y':
            self.Strategy['Legs_Detail'][key]['Mkt Val'] = self.Strategy['Legs_Detail'][key]['Short Strike Mkt Val'] - self.Strategy['Legs_Detail'][key]['Long Strike Mkt Val']
            self.Strategy['Legs_Detail'][key]['PnL'] = self.Strategy['Legs_Detail'][key]['Price Entry'] - self.Strategy['Legs_Detail'][key]['Mkt Val']
                
        else:
            self.Strategy['Legs_Detail'][key]['Mkt Val'] = self.Strategy['Legs_Detail'][key]['Long Strike Mkt Val'] - self.Strategy['Legs_Detail'][key]['Short Strike Mkt Val']
            self.Strategy['Legs_Detail'][key]['PnL'] = self.Strategy['Legs_Detail'][key]['Mkt Val'] - self.Strategy['Legs_Detail'][key]['Price Entry']
        
        self.calc_pnl()
        
    def calc_pnl(self):
        for i in self.Strategy['Legs_Detail'].keys():
            self.Strategy['PnL'] += self.Strategy['Legs_Detail'][i]['PnL']
        
        
    def save_object(self, obj, underlying, expiry_date):
        pickle.dump(obj, open('{0}_{1}'.format(underlying, expiry_date), "wb"))
        print ('Changes Saved.')
        
    def load_object(self, underlying, expiry_date):
        return pickle.load(open('{0}_{1}'.format(underlying, expiry_date), "rb"))

    def print_strategy(self):
        print (self.Strategy['Legs_Detail'])
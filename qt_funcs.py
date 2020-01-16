#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 20:53:17 2019

@author: bhaskarnamrata
"""

from questrade_api import Questrade
from pandas.io.json import json_normalize
import pandas as pd
import json
from config import config
import psycopg2


class qt_analysis:
    def __init__(self):
        self.account_detail = 0,
        self.account_number = 0,
        self.account_balances = 0,
        self.account_df = pd.DataFrame(),
#        self.positions_df = pd.DataFrame(),
        self.positions = 0,
        self.symbolIds = [],
        self.closed_pos_df = pd.DataFrame(),
        self.positions_df = pd.DataFrame(),
        self.account_balances_df = pd.DataFrame()
        
        
        
    def qt_connect(self):
        q = Questrade()
        return q
    
    
    def get_symbols(self):
        self.symbolIds = self.positions_df['symbolId'].unique()

    
    def get_positions(self, q):
        ## Error code for missing Account Number 1018 (code: 1018)
        self.positions = q.account_positions(self.account_number)
        self.positions_df = self.positions_df[0].from_dict(json_normalize(self.positions['positions']), orient = 'columns')
        self.positions_df['underlying'] = 'YYY'
        self.positions_df['delta'] = 0.00
        self.positions_df['gamma'] = 0.00
        self.positions_df['theta'] = 0.00
        self.positions_df['DTE'] = 99
        self.positions_df['strategy'] = ''
        self.positions_df['PnlTarget'] = 0.00

    def enrich_positions(self, q):
        for i in self.positions_df['symbolId']:
            self.markets_options = q.markets_options(optionIds = [i])
            self.positions_df.loc[self.positions_df['symbolId'] == i, 'underlying'] = self.markets_options['optionQuotes'][0]['underlying']
            self.positions_df.loc[self.positions_df['symbolId'] == i, 'delta'] = self.markets_options['optionQuotes'][0]['delta']
            self.positions_df.loc[self.positions_df['symbolId'] == i, 'gamma'] = self.markets_options['optionQuotes'][0]['gamma']
            self.positions_df.loc[self.positions_df['symbolId'] == i, 'theta'] = self.markets_options['optionQuotes'][0]['theta']
            self.positions_df.loc[self.positions_df['symbolId'] == i, 'expiry'] = self.markets_options['optionQuotes'][0]['symbol'][3:10]
            
        for j in config.keys():
            self.positions_df.loc[self.positions_df['underlying'] == j, 'strategy'] = config[j]['strategy']
            self.positions_df.loc[self.positions_df['underlying'] == j, 'PnlTarget'] = config[j]['PnlTarget']*self.positions_df['totalCost']

        return self.positions_df
        
        
    def calc_positions(self):
        return 1
    
    def summarize_positions(self):
        print ('\nTotal Open P/L: ${0}'.format(self.positions_df['openPnl'].sum()))
        print ('\nGroup by Underlying: \n{0}\n'.format(self.positions_df[['symbol','underlying', 'expiry', 'totalCost', 'openPnl', 'delta', 'gamma', 'strategy', 'PnlTarget']].groupby(['underlying', 'strategy', 'expiry']).sum()))
        print ('\nDetailed breakdown by leg: \n{0}\n'.format(self.positions_df[['underlying', 'symbol','openPnl', 'delta', 'gamma']]))

    
    
    
    def get_account(self, q):
        self.account_detail = q.accounts
        self.account_number = self.account_detail['accounts'][0]['number']
        self.account_balances = q.account_balances(self.account_number)
        self.account_df = self.account_df[0].from_dict(json_normalize(self.account_detail['accounts'][0]), orient='columns')
        self.account_balances_df = self.account_balances_df.from_dict(json_normalize(self.account_balances['perCurrencyBalances'][1]), orient='columns')
    
    
    def db_write(self):
        try:
            connection = psycopg2.connect(user = "postgres",
                                          password = "santoshi9",
                                          host = "127.0.0.1",
                                          port = "5432",
                                          database = "qt_data")
        
            cursor = connection.cursor()
            query = 'SELECT * FROM qt_track.account'
            # Print PostgreSQL Connection properties

            cursor.execute(query)

            print ( connection.get_dsn_parameters(),"\n")
            # Print PostgreSQL version
            cursor.execute("SELECT version();")
            record = cursor.fetchone()
            print("You are connected to - ", record,"\n")
        except (Exception, psycopg2.Error) as error :
            print ("Error while connecting to PostgreSQL", error)
        finally:
            #closing database connection.
                if(connection):
                    cursor.close()
                    connection.close()
                    print("PostgreSQL connection is closed")

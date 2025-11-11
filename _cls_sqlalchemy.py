# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 12:23:03 2023

@author: Ronal.Barberi
"""
#%% Imported libraries

from sqlalchemy import create_engine
from urllib.parse import quote

#%% Create Class

class MySQLConnector61:

    @staticmethod
    def funConectMySql(database):
        varDbms = 'mysql+mysqldb'
        varUser = "alvaroquinones6955"
        varHost = "172.70.7.61"
        varPort = "3306"
        varPass = quote('4&3pXaW*smRkzQ3B1b9,')
        engine = None
        db = None
        cadena = f"{varDbms}://{varUser}:{varPass}@{varHost}:{varPort}/{database}"
        engine = create_engine(cadena)
        return engine

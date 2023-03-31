# -*- coding: utf-8 -*-

from configparser import ConfigParser
import mysql.connector


class MariaDB:
    
    def __init__(self):
        config = ConfigParser()
        config.read("config.ini")
        
        self.cnx = mysql.connector.connect(
            host=config.get("mysql", "host"),
            user=config.get("mysql", "user"),
            password=config.get("mysql", "password"),
            database=config.get("mysql", "database"),
            charset=config.get("mysql", "charset")
        )

    def __enter__(self):
        return self.cnx
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cnx.close()
        
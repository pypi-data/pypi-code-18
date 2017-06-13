#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymongo

try:
    # Create Client
    client = pymongo.MongoClient("localhost", 27017)
         
    # Use Database
    db = client.__getattr__("test")
     
    # Connect to Collection
    col = db.__getattr__("test_col")
    col.drop()
except:
    pass
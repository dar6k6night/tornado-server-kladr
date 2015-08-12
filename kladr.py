#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.ioloop
import tornado.web
from server_db import *
import chardet
import os, crypt

def get_json(name, code, typeshort, types):
    return '{{"name":"{0}", "code": "{1}", "typeshort": "{2}", "type": "{3}"}}'.format(str(name), str(code), str(typeshort), str(types.get(typeshort)))

def Normalize(text):
#    text = text.replace('/[^а-яА-Я0-9,\/._ёЁ]+/u', '')
    return text.decode('utf-8').lower().encode('utf-8')

def GetSearchRegion(query):
    if not query:
        return {}
    return get_regions_for_search(query)    

def GetSearchRecords(query, parentid, number, table):
    if not query:
        return {}
    if parentid and number:
        parentid = parentid[:number]
    else:
        parentid = ""
    return get_records_for_search(query, parentid, table)

def GetSearchForType(type, query, parentid):
    return {
        'region' : GetSearchRecords(query, '', False, 'regions'),
        'raion'  : GetSearchRecords(query, parentid, 2, 'raions'),
        'city'   : GetSearchRecords(query, parentid, 5, 'citys'),
        'street' : GetSearchRecords(query, parentid, 11, 'streets')
    }.get(type)

def GetTypeShorts():
    shorts = get_type_shorts()
    type_shorts = {}
    for elem in shorts:
        type_shorts[elem.get('TypeShort')] = elem.get('Type')
    return type_shorts

class MainHandler(tornado.web.RequestHandler):
    TypeShorts = GetTypeShorts()

    def post(self):
        self.write("oops")

    def get(self):
        reconnect()
        type = self.get_argument('type', False)
    	query = self.get_argument('query', False)
        parent_id = self.get_argument('ParentId', False)
        if query:
            query = query.encode('utf-8')
        query = Normalize(query)
        datas = GetSearchForType(type, query, parent_id)
        txt = "{ \"type\": \""+str(type)+"\", \"values\": [ "
        if datas:
            for elem in datas:
                if len(txt) > 40:
                    txt = txt + ", "
                json = get_json(elem.get('Name'), elem.get('Code'), elem.get('TypeShort'), self.TypeShorts)
                txt = txt + json
        txt = txt + " ] }"
        self.set_header("Access-Control-Allow-Origin","*")
        self.set_header("Access-Control-Allow-Methods","POST, GET, OPTIONS")
        self.set_header("Access-Control-Expose-Headers","Access-Control-Allow-Origin")
        self.set_header("Access-Control-Allow-Headers:","Origin, X-Requested-With, Content-Type, Accept")
        self.set_header("Content-type", "application/json")
        self.write(txt)

    def options(self):
        self.set_header("Access-Control-Allow-Origin","*")
        self.set_header("Access-Control-Allow-Methods","POST, GET, OPTIONS")
        self.set_header("Access-Control-Expose-Headers","Access-Control-Allow-Origin")
        self.set_header("Access-Control-Allow-Headers:","Origin, X-Requested-With, Content-Type, Accept")

application = tornado.web.Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":    
    application.listen(999)
    tornado.ioloop.IOLoop.instance().start()
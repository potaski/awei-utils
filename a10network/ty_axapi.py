"""
Created on 20160922
Author: zhangwei

A10NetWorks AX serial: AXAPI v1x
"""

# coding:utf-8

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
from xml.etree import ElementTree
import ssl
import requests


class TLSv1_Adapter(HTTPAdapter):
    
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(
            num_pools=connections, maxsize=maxsize, block=block,
            ssl_version=ssl.PROTOCOL_TLSv1
        )
        
        
class AxApi:
    
    def __init__(self, axip):
        self.req = requests.Session()
        self.req.mount('https://',TLSv1_Adapter())
        self.axip = axip
        self.uri_beg = 'https://{}/services/rest/V1.1'.format(self.axip)
        
    def conn_api(self, uri):
        try:
            res = self.req.get(uri, verify=False, timeout=5)
            return res.content
        except Exception,msg:
            print msg
            return ''
        
    def login(self, username='zhangwei', password=''):
        uri = self.uri_beg + '/?method=authenticate&username={}&password={}'.format(username, password)
        res = self.conn_api(uri)
        return res

    def logout(self, session_id=''):
        uri = self.uri_beg + '/?session_id={}&method=session.close'.format(session_id)
        res = self.conn_api(uri)
        return res
    
    def axapi_function(self, session_id='', method=''):
        if method == 'allinfo_servicegroup':
            uri_method = 'method=slb.servicegroup.getAll'
            
        elif method == 'allinfo_virtualserver':
            uri_method = 'method=slb.vip.getAll'
            
        elif method == 'allinfo_natpool':
            uri_method = 'method=nat.pool.getAll'
            
        elif method == 'perf_virtualserver':
            uri_method = 'method=slb.vip.fetchAllStatistics'
            
        elif method == 'perf_natpool':
            uri_method = 'method=nat.pool.fetchAllStatistics'
            
        else:
            uri_method = ''
            
        uri = '{}/?session_id={}&{}'.format(self.uri_beg, session_id, uri_method)
        res = self.conn_api(uri)
        return res
    

class Xml2Dict(object):

    def __init__(self, coding='UTF-8'):
        self.coding = coding

    def parse_node(self, node):
        tree = {}
        #Save childrens
        for child in node.getchildren():
            ctag = child.tag
            cattr = child.attrib
            ctext = child.text.strip().encode(self.coding) if child.text is not None else ''
            ctree = self.parse_node(child)

            if not ctree:
                cdict = self.make_dict(ctag, ctext, cattr)
            else:
                cdict = self.make_dict(ctag, ctree, cattr)

            if ctag not in tree: # First time found
                tree.update(cdict)
                continue

            atag = '@' + ctag
            atree = tree[ctag]
            if not isinstance(atree, list):
                if not isinstance(atree, dict):
                    atree = {}

                if atag in tree:
                    atree['#'+ctag] = tree[atag]
                    del tree[atag]

                tree[ctag] = [atree] # Multi entries, change to list

            if cattr:
                ctree['#'+ctag] = cattr

            tree[ctag].append(ctree)

        return  tree

    def make_dict(self, tag, value, attr=None):
        """ Generate a new dict with tag and value
        If attr is not None then convert tag name to @tag
        and convert tuple list to dict
        """
        ret = {tag: value}
        # Save attributes as @tag value
        if attr:
            atag = '@' + tag
            aattr = {}
            for k, v in attr.items():
                aattr[k] = v

            ret[atag] = aattr
            del atag
            del aattr

        return ret

    def parse(self, xml):
        #Parse xml string to python dict
        EL = ElementTree.fromstring(xml)
        return self.make_dict(EL.tag, self.parse_node(EL), EL.attrib)

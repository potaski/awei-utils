"""
Created on 2016-09-27 10:22
Author: zhangwei
Description: 获取A10 VirtualServer 和 NetPool 信息
python2
"""

# coding:utf-8


from ty_axapi import AxApi
from ty_axapi import Xml2Dict
from xml.etree import ElementTree
import sys


def exec_vs_perf(xml_string):
    dict_out = {}
    parsedict = Xml2Dict()
    dict_a = parsedict.parse(xml_string)
    
    if dict_a['@response']['status'] == 'ok':
        dict_b = dict_a['response']['virtual-servers']
        
        for data in dict_b['virtual-server']:
            dict_c = data['#virtual-server']
            dict_tmp = {}
            
            for key in ['status','address','cur_conns']:
                dict_tmp[key] = dict_c[key]
                
            dict_out[dict_c['name']] = dict_tmp
            
    return dict_out     # dict_out[vs_name] = {status:?, address:?, cur_coons:?}
    """  Return As String
    if dict_a['@response']['status'] == 'ok':
        dict_b = dict_a['response']['virtual-servers']
        for data in dict_b['virtual-server']:
            dict_b = dict_a['response']['virtual-servers']
            dict_c = data['#virtual-server']
            str_out += '{}\t{}\t{}\t{}\n'.format(dict_c['name'],
                                                 dict_c['status'],
                                                 dict_c['address'],
                                                 dict_c['cur_conns'])

    else:
        print 'info error'
        
    return str_out
    """

def exec_vs_info(xml_string):
    dict_out = {}
    parsedict = Xml2Dict()
    dict_a = parsedict.parse(xml_string)
    if dict_a['@response']['status'] == 'ok':
        dict_b = dict_a['response']['virtual-servers']
        
        for data in dict_b['virtual-server']:
            dict_c = data['#virtual-server']
            dict_tmp = {}
            
            for key in ['status','arp_disabled','ha_group']:
                dict_tmp[key] = dict_c[key]
                
            dict_out[dict_c['name']] = dict_tmp
            
    return dict_out     # dict_out[vs_name] = {status:?, arp_disabled:?, ha_group:?}

def exec_np_info(xml_string):
    dict_out = {}
    parsedict = Xml2Dict()
    dict_a = parsedict.parse(xml_string)
    if dict_a['@response']['status'] == 'ok':
        dict_b = dict_a['response']['pools']
        
        for data in dict_b['pool']:
            dict_c = data['#pool']
            dict_out[dict_c['name']] = dict_c['ha_group']
            
    return dict_out     # dict_out[np_name] = ha_group

def exec_np_perf(xml_string):
    dict_out = {}
    parsedict = Xml2Dict()
    dict_a = parsedict.parse(xml_string)
    if dict_a['@response']['status'] == 'ok':
        dict_b = dict_a['response']['pools']
        
        for dict_c in dict_b['pool']:
            dict_tmp = {}
            for key in ['port_usage','total_failed']:
                dict_tmp[key] = dict_c['#pool'][key]
                
            dict_out[dict_c['#pool']['name']] = dict_tmp
            
    return dict_out     # dict_out[np_name] = {port_usage:?, total_failed:?}



if __name__ == '__main__':
    lst_a10 = ['10.1.1.1', '10.1.1.2']
    dict_haid ={'1': lst_a10[0], '2': lst_a10[1]}
    dict_res = {}

    # A10-HA1
    for ip in lst_a10:
        obj = AxApi(ip)
        res = obj.login()
        tree = ElementTree.fromstring(res)
        
        if tree.attrib['status'] == 'ok':
            session_id = tree.find('session_id').text
            
        else:
            print 'login {} failed'.format(ip)
            sys.exit()
                
        if ip == '10.1.1.1':
            VS_info = obj.axapi_function(session_id, method='allinfo_virtualserver')
            NP_info = obj.axapi_function(session_id, method='allinfo_natpool')
            
        dict_res['{}_vs'.format(ip)] = obj.axapi_function(session_id, method='perf_virtualserver')
        dict_res['{}_np'.format(ip)] = obj.axapi_function(session_id, method='perf_natpool')
        
        obj.logout(session_id)
   
    # XML2DICT
    dict_VS_info = exec_vs_info(VS_info)
    dict_NP_info = exec_np_info(NP_info)
    for k,v in dict_res.items():
        try:
            dict_res[k] = exec_np_perf(v)
        except:
            dict_res[k] = exec_vs_perf(v)
        
    # 
    
    # Virtual Server
    str_out = 'VirtualServer\tHa_Group\tStatus\tArp_Disabled\tVIP\tCur_Coons\n'
    for k,v in dict_VS_info.items():
        vs_name = k
        vs_haid = v['ha_group']
        vs_perf = dict_res['{}_vs'.format(dict_haid[vs_haid])][vs_name]
        str_out += '{}\t{}\t{}\t{}\t{}\t{}\n'.format(
            vs_name, vs_haid, vs_perf['status'], 
            dict_VS_info[vs_name]['arp_disabled'], vs_perf['address'],
            vs_perf['cur_conns']
        )
        
    print str_out
    
    # Nat Pool
    str_out = 'NatPool\tHa_Group\tPort_Usage\tTotal_Failed\n'
    for k,v in dict_NP_info.items():
        np_name = k
        np_haid = v
        np_perf = dict_res['{}_np'.format(dict_haid[np_haid])][np_name]
        str_out += '{}\t{}\t{}\t{}\n'.format(
            np_name, np_haid, np_perf['port_usage'], np_perf['total_failed']
        )
        
    print str_out

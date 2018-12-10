#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
-------------------- Copyright --------------------
Date    : 2018-12-10 08:44:11
Author  : hnawei (potaski@qq.com)
Describe: how to use saltstack by python api
Version : 1.0.0
-------------------- History --------------------
2018/12/10 - First Version(salt 2017 or 2018, python3.6)
-------------------- End --------------------
"""


# import saltstack
import salt.client
import salt.runner

# import standard package
import json
import time

# init saltstack
opts = salt.config.master_config('/etc/salt/master')
runner = salt.runner.RunnerClient(opts)
client = salt.client.LocalClient()

# use saltstack in front
def user_salt_in_front():
    """ Synchronous
    return ret: results as JSON
    """
    ret = client.cmd(tgt='*', fun='test.ping')
    print(json.dumps(ret, indent=4, sort_keys=True, ensure_ascii=False))
    return ret

# use saltstack in backend
def user_salt_in_backend(hosts):
    """ Asynchronous
    param hosts: host minion id as LIST
    return ret: results as JSON
    """
    max_retry = 10
    interval = 2
    host_num = len(hosts)
    jid = local.cmd_async(tgt_type='list', tgt=hosts, , fun='test.ping')
    # print('saltstack jid = ', jid)
    for i in range(max_retry):
        time.sleep(interval)
        ret = runner.cmd(
            fun='jobs.lookup_jid', kwarg={'jid': jid}, print_event=False
        )
        if len(ret) == host_num:
            # print('all servers had responded')
            break
    print(json.dumps(ret, indent=4, sort_keys=True, ensure_ascii=False))
    return ret
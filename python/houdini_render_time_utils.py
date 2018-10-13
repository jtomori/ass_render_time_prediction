"""
Collection of scripts which are called by Houdini renders.
"""

import os
import hou
import json
import time
import cpuinfo
import subprocess
import re

re_map = {'Machine': 'Machine: ',
            'CPU':'CPU  : ',
            'Cache': 'Cache: ',
            'Number of cores':'Number of cores: ',
            'Number of threads': 'Number of threads: '}

def _client_cpu_info(payload):
    """
    Get cpu information and relevant features
    payload(dict): render client information
    return(dict): payload incl. cpu info
    """
    if not cpuinfo.cpu.info:
        payload['processor_name'] = 'failed'
        return payload

    if 'ProcessorNameString' in cpuinfo.cpu.info[0]:
        _processor = cpuinfo.cpu.info[0]['ProcessorNameString']
        payload['processor_name'], indicators  = _processor, _processor.split()
        payload['logical_processors'] = len(cpuinfo.cpu.info)
        payload['GHz'] = float(indicators[-1].replace('GHz', ''))
        payload['model'] = indicators[1].replace('(R)', '')
        payload['rev'] = indicators[3]
        payload['v'] = float(indicators[4].replace('v', ''))
        payload['abs_GHz'] = payload['logical_processors'] * payload['GHz']

    return payload


def client_cpu_info(payload):
    """
    Get cpu information and relevant features using GetSys64.exe
    payload(dict): render client information
    return(dict): payload incl. cpu info
    """
    getsys_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'utils')
    system_info_output = subprocess.getoutput(os.path.join(getsys_path, 'GetSys64.exe'))
    for feat, pat in re_map.items():
        pattern = r"{0}.*".format(pat)
        ret = re.findall(pattern, system_info_output)[0]
        if 'CPU' == feat:
            ret = ret.replace(pat, '')
            process_indicators = ret.split()
            payload['sockets'] = float(process_indicators[0])
            payload['MHz'] = float(process_indicators[-2])
            payload['id'] = str(' '.join(process_indicators[3:5]))
            payload['v'] = float(process_indicators[5].replace('v', ''))
        elif 'Cache' in ret:
            ret = ret.replace(pat, '')
            cache_indicators = ret.split()
            payload['cache KB'] = float(cache_indicators[0])+\
                               float(cache_indicators[4])+\
                               float(cache_indicators[8])
        elif 'Number of cores' == feat:
            cores_indicators = ret.replace(pat, '')
            payload['cores'] = float(cores_indicators)
        elif 'Number of threads' == feat:
            threads_indicators = ret.replace(pat, '')
            payload['threads'] = float(threads_indicators)

def timer_start(attrib_name="timer_start"):
    """
    Saves current time into hou.session object, this function should be in Pre-Render script

    attrib_name - name of attribute to save to
    """

    setattr(hou.session, attrib_name, time.time())

def timer_duration(payload, attrib_name="timer_start"):
    """
    Computes and returns difference between current time and time saved in hou.session object

    If attribute doesn't exist, None will be returned

    attrib_name - name of attribute to read from
    """

    try:
        payload['render_time'] = time.time() - getattr(hou.session, attrib_name)
    except AttributeError as e:
        return None

def set_json_file_path():
    """
    todo
    """

    me = hou.pwd()
    out_img = me.parm("ar_picture").eval()
    out_img = ".".join( out_img.split(".")[:-1] )

    return out_img

def save_render_time(file=None, payload = {}):
    """
    Saves render timwe into a file, this function should be in Post-Render script
    """
    timer_duration(payload)
    client_cpu_info(payload)
    with open('{}.json'.format(file), 'w') as outfile:
        json.dump(payload, outfile)


save_render_time()
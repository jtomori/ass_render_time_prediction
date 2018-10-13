"""
Collection of scripts which are called by Houdini renders.
"""

import os
import hou
import json
import time
import cpuinfo
import subprocess
#out  =  subprocess.getoutput('wmic MEMORYCHIP get BankLabel,DeviceLocator,Capacity,Tag, MemoryType')
#print (out)

def client_cpu_info(payload):
    """
    return cpu info on windows
    """
    if cpuinfo.cpu.info:
        if 'ProcessorNameString' in cpuinfo.cpu.info[0]:
            _processor = cpuinfo.cpu.info[0]['ProcessorNameString']
            payload['processor_name'], indicators  = _processor, _processor.split()
            print(indicators)
            payload['GHz'] = indicators[-1].replace('GHz', '')
            payload['model'] = indicators[1].replace('(R)', '')
            payload['rev'] = indicators[3]
            payload['v'] = indicators[4].replace('v', '')
        payload['logical_processors'] = len(cpuinfo.cpu.info)
    return payload

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

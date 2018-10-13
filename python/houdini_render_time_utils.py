"""
Collection of scripts which are called by Houdini renders.
"""

import hou
import time

def timer_start(attrib_name="timer_start"):
    """
    Saves current time into hou.session object, this function should be in Pre-Render script

    attrib_name - name of attribute to save to
    """
    
    setattr(hou.session, attrib_name, time.time())

def timer_duration(attrib_name="timer_start"):
    """
    Computes and returns difference between current time and time saved in hou.session object

    If attribute doesn't exist, None will be returned

    attrib_name - name of attribute to read from
    """

    try:
        return time.time() - getattr(hou.session, attrib_name)
    except AttributeError:
        return None

def save_render_time(file=None):
    """
    Saves render timwe into a file, this function should be in Post-Render script
    """

    render_time = timer_duration()
    if render_time:
        print "Render took: {} seconds, machine: {}, user: {}".format(render_time, hou.getenv("COMPUTERNAME"), hou.getenv("USERNAME"))
    else:
        print "None was returned"
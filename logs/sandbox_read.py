import json
import os
"""
with open('test_scene_2.hipnc.json') as json_data:
    data = json.load(json_data)
    for _id in data:
        for param in data[_id]:
            print (param)
        import pdb
        pdb.set_trace()

        _file = 'scene_2/log_{0}.json'.format(_id)
        if os.path.exists(_file):

            with open(_file) as json_data:
                _logs = json.load(json_data)

            print(float(_logs["render 0000"]["frame time"]["microseconds"])/1000000)

"""


def rec(parent, data, rel_flat):
    for d, v in data.items():
        if isinstance(v, dict):
            rec("{0}/{1}".format(parent,d), v, rel_flat)

        else:
            if not isinstance(v, list):
                if not "{0}/{1}".format(parent,d) in rel_flat.keys():
                    rel_flat["{0}/{1}".format(parent,d)] = v
            else:
                #print ("{0}/{1}".format(parent,d))
                pass


meta = {}
with open('test_scene_2.hipnc.json') as json_data:
    _data = json.load(json_data)
    for _id in _data:
        #print (_id)
        rel_flat = {}
        for param in _data[_id]:
            rel_flat[param] = _data[_id][param]

        _file = 'scene_2/log_{0}.json'.format(_id)
        if os.path.exists(_file):
            with open(_file) as json_data:
                data = json.load(json_data)
                rec("",data, rel_flat)
            meta[_id] = rel_flat

with open('output_data.json', 'w') as outfile:
    json.dump(meta, outfile)


meta_list = []

for key, val in meta.items():
    tmp_dict = val
    tmp_dict["frame"] = key
    meta_list.append(tmp_dict)

import csv

all_keys = []

for _dict in meta_list:
    all_keys.extend(_dict.keys())

all_keys = list(set(all_keys))

#keys = meta_list[0].keys()

with open('output_data.csv', 'w') as output_file:
    dict_writer = csv.DictWriter(output_file, all_keys)
    dict_writer.writeheader()
    dict_writer.writerows(meta_list)
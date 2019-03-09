import csv

def to_square(value, *args):
    return value**2

def to_seconds(microseconds, *args):
    return microseconds/(10**6)

def to_pixels(y, x, *args):
    return y * x

def traverse_dict(parent, data, rel_flat, *args):
    for d, v in data.items():
        if d.startswith("render 0"):
           d = d.split(" ")[0]
        if isinstance(v, dict):
            traverse_dict("{0}/{1}".format(parent,d), v, rel_flat)
        else:
            if not isinstance(v, list):
                if not "{0}/{1}".format(parent,d) in rel_flat.keys():
                    rel_flat["{0}/{1}".format(parent,d)] = v
            else:
                print ("{0}/{1}".format(parent,d))

def to_csv(json_file, scene_dir, *args):
	meta = {}
	with open(json_file) as json_data:
		_data = json.load(json_data)
		for _id in _data:
		    rel_flat = {}
		    for param in _data[_id]:
		        rel_flat[param] = _data[_id][param]
		    _file = '{0}/log_{1}.json'.format(scene_dir, _id)
		    if os.path.exists(_file):
		        with open(_file) as json_data:
		            data = json.load(json_data)
		            traverse_dict("",data, rel_flat)
		        meta[_id] = rel_flat

	with open('output_data.json', 'w') as outfile:
		json.dump(meta, outfile)

	meta_list = []

	for key, val in meta.items():
		tmp_dict = val
		tmp_dict["frame"] = key
		meta_list.append(tmp_dict)

	all_keys = []
	for _dict in meta_list:
		all_keys.extend(_dict.keys())

	all_keys = list(set(all_keys))

	with open('output_data.csv', 'w') as output_file:
		dict_writer = csv.DictWriter(output_file, all_keys)
		dict_writer.writeheader()
		dict_writer.writerows(meta_list)

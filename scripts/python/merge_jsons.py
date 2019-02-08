"""
Functions for collecting and merging json files.
"""

import os
import json

def merge_jsons(jsons_path=None, key="hostname", output_path=None):
    """
    Finds all .json files in jsons_path directory and merges them into one dictionary saved in output_path
    It uses key parameter value as keys for the merged dict

    If output_path is not set, it prints the merged dict and its length
    """

    json_list = [os.path.join(jsons_path, f) for f in os.listdir(jsons_path) if f.endswith(".json")]

    merge_dict = {}

    """
    # organise based on key parameter
    for file in json_list:
        with open(file) as f:
            file_dict = json.load(f)
        merge_dict[ file_dict[key] ] = file_dict
    """
    # organise based on frame number
    for file in json_list:
        with open(file) as f:
            file_dict = json.load(f)
        merge_dict[ os.path.basename(file).split(".")[0].split("_")[-1] ] = file_dict
    
    if output_path:
        with open(output_path, 'w') as f:
            json.dump(merge_dict, f)
    else:
        print json.dumps(merge_dict, sort_keys=True, indent=4)
        print "Dict has {} keys".format(len(merge_dict))

if __name__ == "__main__":
    merge_jsons(r'S:\020_Preproduction\050_RND\540_farm_submission_testing\code\ass_render_time_prediction\scenes\render', key="Machine", output_path=r'S:\020_Preproduction\050_RND\540_farm_submission_testing\code\ass_render_time_prediction\scenes\dataset_2.json')

    #merge_jsons(r'S:\020_Preproduction\050_RND\540_farm_submission_testing\code\ass_render_time_prediction\scenes\render', key="Machine")

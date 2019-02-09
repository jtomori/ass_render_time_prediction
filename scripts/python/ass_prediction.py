import hou
import json
import random
import logging

logging.basicConfig(level=logging.DEBUG)

class GenericSamples(object):
    """
    A base class containing general implementation of functions used for generating and setting random samples on parameters.
    
    parameters dictionary in this case shows different values which are expected:
        if value is integer, then integers in the range (inclusive) are chosen
        if value is float, then floats in the range (inclusive) are chosen
        if there are more than two values, then N of the specified values are chosen
    """
    parameters = {
        "integer_range"                 : [1, 4],
        "float_range"                   : [0.2, 0.3],
        "random_choice"                 : [1, 14, 22, 73, 18]
    }

    @classmethod
    def generateSamples(cls, samples):
        """
        Generates N (samples parameter) amount of samples within a range as specified in cls.parameters dictionary.
        Returns dictionary with the same keys, but with N random values.
        """
        samples_dict = {}
        
        for key, value in cls.parameters.iteritems():
            if len(value) > 2:
                samples_dict[key] = [random.choice(value) for i in range (samples)]
            elif isinstance(value[0], int):
                samples_dict[key] = [random.randint(value[0], value[1]) for i in range (samples)]
            elif isinstance(value[0], float):
                samples_dict[key] = [random.random() * (value[1] - value[0]) + value[0] for i in range (samples)]
        
        return samples_dict
            
class HoudiniArnoldSamples(GenericSamples):
    """
    Implementation for Arnold in Houdini.
    """
    parameters = {
        "ar_AA_samples"                 : [1, 10],
        "ar_GI_diffuse_samples"         : [0, 10],
        "ar_GI_specular_samples"        : [0, 10],
        "ar_GI_transmission_samples"    : [0, 10],
        "ar_GI_sss_samples"             : [0, 10],
        "ar_GI_volume_samples"          : [0, 10],
        "ar_indirect_specular_blur"     : [0, 10],
        "ar_sss_use_autobump"           : [0, 1],
        #"ar_GI_total_depth"             : [0, 50],
        "ar_GI_diffuse_depth"           : [0, 10],
        "ar_GI_specular_depth"          : [0, 10],
        "ar_GI_transmission_depth"      : [0, 20],
        "ar_GI_volume_depth"            : [0, 10],
        "ar_auto_transparency_depth"    : [0, 20],
        "ar_low_light_threshold"        : [0.0, 0.2],
        "ar_mb_xform_keys"              : [1, 10],
        "ar_mb_dform_keys"              : [1, 10],
        "ar_bucket_size"                : [16, 1024],
        "ar_pixel_filter_width"         : [0.0, 10.0],
        "ar_indirect_sample_clamp"      : [0.0, 30.0],
        "res_overridex"                 : [256, 512, 1024, 2048, 4096, 8192, 640, 1280, 1920, 3840],
        "res_overridey"                 : [256, 512, 1024, 2048, 4096, 8192, 480, 720, 1080, 2160]
    }

    @classmethod
    def setParameters(cls, node, samples):
        """
        Sets N (samples parameter) random samples on parameters specified in cls.parameters dictionary on a passed node (node parameter).
        """
        if node.type().name() != "arnold":
            logging.error("Specified node is not arnold type.")
            return
        
        samples_dict = cls.generateSamples(samples)

        for parm, samples in samples_dict.iteritems():
            keyframes = []
            for i in range(len(samples)):
                keyframe_dict = {}
                keyframe_dict["value"] = samples[i]
                keyframe_dict["frame"] = i+1

                keyframe = hou.Keyframe()
                keyframe.fromJSON(keyframe_dict)

                keyframes.append(keyframe)
            
            node.parm(parm).setKeyframes( tuple(keyframes) )
    
    @classmethod
    def setParametersShelf(cls):
        """
        Calls cls.setParameters() with node specified by user. Samples range is taken from timeline settings, assuming timeline starts at frame 1.
        Intended to be run from Shelf.
        """
        node = hou.selectedNodes()[0]
        samples = int(hou.playbar.frameRange()[1])

        cls.setParameters(node, samples)
    
    @classmethod
    def getAdditionalInfoDict(cls, node):
        """
        Returns a dictionary with parameter values over frame range. This can be used to save animated values of parameters which are not found in logs.
        """
        parameters = cls.parameters.keys()

        out_dict = {}

        for parm in parameters:
            parm_keyframes = node.parm(parm).keyframes()
            for keyframe in parm_keyframes:
                frame = int(keyframe.frame())
                value = keyframe.value()

                if frame not in out_dict:
                    out_dict[frame] = {}

                out_dict[frame][parm] = value

        return out_dict
    
    @classmethod
    def getAdditionalInfoDictShelf(cls):
        """
        Shelf tool which will export JSON with all keyframes from parameters specified in cls.getAdditionalInfoDict() into scenefile.json
        """
        node = hou.selectedNodes()[0]
        out_dict = cls.getAdditionalInfoDict(node)

        hip_file = hou.getenv("HIPFILE")

        with open(hip_file + ".json", "w") as out_file:
            json.dump(out_dict, out_file)

if __name__ == "__main__":
    print HoudiniArnoldSamples.generateSamples(5)

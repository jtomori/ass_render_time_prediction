class ArnoldSamples(object):
    """
    dictionary of parameters which are used for different render samples
    "parameter_name" : [minimum_value, maximum_value]
    if value is integer, then integers are chosen
    if value is float, then floats are chosen
    if there are more than two values, then the exact values are chosen
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
        "ar_GI_total_depth"             : [0, 50],
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
        Generates N (samples parameter) random samples on parameters specified in cls.parameters dictionary on a passed node (node parameter).
        """
        pass
    
    @classmethod
    def setParametersShelf(cls):
        """
        Calls cls.setParameters() with node and samples specified by user. Intended to be run from Shelf.
        """
        pass
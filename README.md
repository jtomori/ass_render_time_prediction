# ASS render time prediction
Predicting render times for Arnold renderer scenes

<br>

### Versions used
* Houdini 16.5.571
* Arnold 5.2.0.1
* htoa 3.1.1

<br>

### Dataset 1
* This is to determine impact of computers parameters on rendering of an example scene
* Rendering one scene on multiple different computers
* Computer parameters captured:
    * Total GHz number: `cores * frequency`
    * RAM size
    * RAM type (DDR*)
    * RAM frequency
    * SSD?
    * CPU model
    * Hyperthreading
    * CPU cache

<br>

### Dataset 2
* This dataset is used to determine ratio of render times between different scenes and an example scene
* Rendering different scenes on the same computer
* Scene parameters captured:
    * Amount of pixels: `resolution_x * resolution_y`
    * Samples
        * AA
        * diffuse
        * specular
        * transmission
        * volume indirect
        * bssrdf
        * transparency
    * Count of nodes
    * Scene bounds
    * Amount of geometry
    * Size of ASS file
    * Size of all textures referenced from the ASS file
    * Network speed
    * DoF?
    * Motion blur?
* Notes
    * included ASS files are not expanded and followed

# -*- coding: utf-8 -*-
"""
Given a JSON file generate scripts for coloring the representation in Chimera and VMD.
"""
from __future__ import print_function
import utils as u
import yaml
import six
import re

def chimera_color(json_file, out_file, model_number="", verbose=True, color_map=None, default_color="#d2d2b4b48c8c"):
    d=u.load_json_data(json_file)

    with open(out_file+'.chimera', 'w') as f:        
        for s in d.segments:
            template = """color {color} #{model}:{start}-{end}"""
            s['model']=model_number
            
            #override the color of segmetns if map is present
            if not color_map is None:
                s['color']=color_map.get(s.name, s.get('color', default_color))
            else:
                s['color']=s.get('color', default_color)

            line = template.format(**s)
            if verbose:
                print(line)
            f.write(line+"\n")


if __name__ == "__main__":
    import argparse    
    parser=argparse.ArgumentParser(__doc__)
    parser.add_argument("-j","--json", default='data.json', help='specify path to json file')
    parser.add_argument("-o","--out-file", default=None, help='Output name (without extension) of the coloring script. Default taken from json')
    parser.add_argument("-v","--verbose", default=True, help='print scripts to screen')
    parser.add_argument("-m","--color-map", default=None, help='colormap to override colors given in the json. Works even if no colors are present in the Json')
    

    a = parser.parse_args()
    
    if a.out_file is None:
        a.out_file = a.json.replace('.json','')

    if not a.color_map is None:
        a.color_map = u.load_json_data(a.color_map)
    chimera_color(a.json, a.out_file, verbose=a.verbose, color_map=a.color_map)

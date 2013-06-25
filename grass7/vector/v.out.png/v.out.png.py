#!/usr/bin/env python
# -*- coding: utf-8 -*-
############################################################################
#
# MODULE:       v.out.png
# AUTHOR(S):    Luca Delucchi, Fondazione E. Mach (Italy)
#
# PURPOSE:      Pack up a vector map, collect vector map elements => gzip
# COPYRIGHT:    (C) 2011 by the GRASS Development Team
#
#               This program is free software under the GNU General
#               Public License (>=v2). Read the file COPYING that
#               comes with GRASS for details.
#
#############################################################################

#%module
#% description: Export vector map as PNG
#% keywords: vector, export, PNG
#%end
#%option G_OPT_V_INPUT
#%end
#%option G_OPT_F_OUTPUT
#% label: Name for new PNG file
#%end
#%option
#% key: rgb_column
#% type: string
#% description: Name of color definition column
#%end
#%option
#% key: compression
#% type: integer
#% options: 0-9
#% label: Compression level of PNG file
#% description: (0 = none, 1 = fastest, 9 = best)
#% answer: 6
#%end
#%option
#% key: width
#% type: integer
#% label: Width of PNG file
#% answer: 640
#%end
#%option
#% key: height
#% type: integer
#% label: Height of PNG file
#% answer: 480
#%end

from grass.script import core as grass
from grass.script import gisenv
from grass.pygrass.vector import Vector
from grass.pygrass.modules.shortcuts import display as d
import os
import sys


def main():
    MONITOR = None
    in_vect = Vector(options['input'])
    in_vect.open()
    os.environ['GRASS_RENDER_IMMEDIATE'] = 'png'
    os.environ['GRASS_PNGFILE'] = options['output']
    os.environ['GRASS_PNG_COMPRESSION'] = options['compression']
    os.environ['GRASS_WIDTH'] = options['width']
    os.environ['GRASS_HEIGHT'] = options['height']
    genv = gisenv()
    if 'MONITOR' in genv:
        MONITOR = genv['MONITOR']
        MONITOR_WX0_PID = genv['MONITOR_WX0_PID']
        MONITOR_wx0_CMDFILE = genv['MONITOR_wx0_CMDFILE']
        MONITOR_wx0_ENVFILE = genv['MONITOR_wx0_ENVFILE']
        MONITOR_wx0_MAPFILE = genv['MONITOR_wx0_MAPFILE']
    if options['rgb_column']:
        d.vect(map=in_vect.name, rgb_column=options['rgb_column'], flags='a',
               quiet=True)
    else:
        d.vect(map=in_vect.name)

if __name__ == "__main__":
    options, flags = grass.parser()
    sys.exit(main())

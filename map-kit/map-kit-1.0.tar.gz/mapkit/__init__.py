from pipehtml import c
from pipeleaflet import b
from pipevts import a,cln
from nlgeojson import make_blocks,make_lines,make_points,make_line,geodf_to_nldf
from postgis_interface import *
from pipegls import * 
from ident import *
from quickmaps import *
from map_xyz import *


def eval_config(config):
	import pipegls
	pipegls.eval_config(config)
	del config
	del pipegls
	import pipegls

def make_config(data,typestring):
	import pipegls
	stuff = pipegls.make_config(data,typestring)
	del data
	del typestring
	del pipegls
	return stuff

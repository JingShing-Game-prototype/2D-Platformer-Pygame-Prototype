from crt_shader import Graphic_engine
import pygame, os, sys

def resource_path(relative):
	if hasattr(sys, "_MEIPASS"):
		absolute_path = os.path.join(sys._MEIPASS, relative)
	else:
		absolute_path = os.path.join(relative)
	return absolute_path

pygame.init()

level_map = [
'                            ',
'                            ',
'                            ',
' XX    XXX            XX    ',
' XX P                       ',
' XXXX         XX         XX ',
' XXXX       XX              ',
' XX    X  XXXX    XX  XX    ',
'       X  XXXX    XX  XXX   ',
'    XXXX  XXXXXX  XX  XXXX  ',
'XXXXXXXX  XXXXXX  XX  XXXX  ']

tile_size = 64
# screen_width = 1200
# screen_height = len(level_map) * tile_size
screen_width = 64*15
screen_height = 640

VIRTUAL_RES = (screen_width, screen_height)
REAL_RES = (1280, 720)
# VIRTUAL_RES = (800, 600)
# REAL_RES = (800, 600)

def get_map_width_and_height(map, tile_size):
	map_width = len(map[0])*tile_size
	map_height = len(map) * tile_size
	return map_width, map_height
map_width, map_height = get_map_width_and_height(level_map, tile_size)


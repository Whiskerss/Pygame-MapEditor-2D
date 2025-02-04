import pygame
import json

# TODU: dynamisk AUTOTILE_MAP
AUTOTILE_MAP = {
    tuple(sorted([(0, 1), (1, 0)])): 0,
    tuple(sorted([(-1, 0), (0, 1)])): 1,
    tuple(sorted([(-1, 0), (0, -1)])): 2,
    tuple(sorted([(1, 0), (0, -1)])): 3,
    tuple(sorted([(1, 0), (-1, 0)])): 4,
    tuple(sorted([(0, 1), (0, -1)])): 5,
    tuple(sorted([(0, 1)])): 6,
    tuple(sorted([(-1, 0)])): 7,
    tuple(sorted([(0, -1)])): 8,
    tuple(sorted([(1, 0)])): 9,
    tuple(sorted([(1, 0), (-1, 0), (0, -1)])): 10,
    tuple(sorted([(1, 0), (-1, 0), (0, 1)])): 11,
    tuple(sorted([(1, 0), (0, -1), (0, 1)])): 12,
    tuple(sorted([(-1, 0), (0, -1), (0, 1)])): 13,
    tuple(sorted([(1, 0), (-1, 0), (0, -1), (0, 1)])): 14,
}
# TODU: dynamisk AUTOTILE_TYPES
AUTOTILE_TYPES = {'wall'}

NEIGHBOR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]

class Tilemap:
    def __init__(self, game, tile_size=30):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []

    def titles_around(self, pos):
        tiles = []
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in NEIGHBOR_OFFSETS:
            check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles
    
    def save(self, path):
        file = open(path, 'w')
        json.dump({'tile_size': self.tile_size, 'tilemap': self.tilemap, 'offgrid': self.offgrid_tiles}, file)
        file.close()

    def load(self, path):
        file = open(path, 'r')
        map_data = json.load(file)
        file.close()

        self.tile_size = map_data['tile_size']
        self.tilemap = map_data['tilemap']
        self.offgrid_tiles = map_data['offgrid']
    
    def autotile(self):
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            neighbors = set()
            for shift in [(1, 0), (-1, 0), (0, -1), (0, 1)]:
                check_loc = str(tile['pos'][0] + shift[0]) + ';' + str(tile['pos'][1] + shift[1])
                if check_loc in self.tilemap:
                    if self.tilemap[check_loc]['type'] == tile['type']:
                        neighbors.add(shift)
            neighbors = tuple(sorted(neighbors))
            if (tile['type'] in AUTOTILE_TYPES) and (neighbors in AUTOTILE_MAP):
                tile['variant'] = AUTOTILE_MAP[neighbors]

    def render(self, surf, offset=(0, 0)):
        for tile in self.offgrid_tiles:
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))
        
        for x in range(offset[0] // self.tile_size, (offset[0] + surf.get_width()) // self.tile_size + 1):
            for y in range(offset[1] // self.tile_size, (offset[1] + surf.get_height()) // self.tile_size + 1):
                loc = str(x) + ';' + str(y)
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size))  
import sys
import pygame

from scripts.utils import load_images
from scripts.tilemap import Tilemap

RENDER_SCALE = 1.0

class MapEditor:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Map Editor 2D')
        self.screen = pygame.display.set_mode((1000, 900))
        self.display = pygame.Surface((1000, 900))
        self.clock = pygame.time.Clock()

        # TODU: dynamisk assets
        self.assets = {
            'wall': load_images('tiles/wall'),
            'floor': load_images('tiles/floor'),
            'spawner': load_images('tiles/spawner'),
        }
        self.tile_list = list(self.assets)
        self.tile_group = 0
        self.tile_variant = 0

        self.movement = [False, False, False, False]

        
        self.tilemap = Tilemap(self, tile_size=30)
        # TODU: dynamisk file load
        try:
            self.tilemap.load('assets/maps/map.json')
        except FileNotFoundError:
            pass

        # TODU: user interface
        self.scroll = [0, 0]
        self.speed = 2

        self.left_clicking = False
        self.right_clicking = False
        self.shift = False
        self.ongrid = True


    def run(self):
        while True:
            self.display.fill((150, 150, 150))

            self.scroll[0] += (self.movement[1]- self.movement[0]) * self.speed
            self.scroll[1] += (self.movement[3]- self.movement[2]) * self.speed

            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
            self.tilemap.render(self.display, offset=render_scroll)

            current_tile_img = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()
            current_tile_img.set_alpha(100)

            mpos = pygame.mouse.get_pos()
            mpos = (mpos[0] / RENDER_SCALE, mpos[1] / RENDER_SCALE)
            tile_pos = (int((mpos[0] + self.scroll[0]) // self.tilemap.tile_size), int((mpos[1] + self.scroll[1]) // self.tilemap.tile_size))

            if self.ongrid:
                self.display.blit(current_tile_img, (tile_pos[0] * self.tilemap.tile_size - self.scroll[0], tile_pos[1] * self.tilemap.tile_size - self.scroll[1]))
            else:
                self.display.blit(current_tile_img, mpos)

            if self.left_clicking and self.ongrid:
                self.tilemap.tilemap[str(tile_pos[0]) + ';' + str(tile_pos[1])] = {'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': tile_pos}
            if self.right_clicking:
                tile_loc = str(tile_pos[0]) + ';' + str(tile_pos[1])
                if tile_loc in self.tilemap.tilemap:
                    del self.tilemap.tilemap[tile_loc]
                for tile in self.tilemap.offgrid_tiles.copy():
                    tile_img = self.assets[tile['type']][tile['variant']]
                    tile_r = pygame.Rect(tile['pos'][0] - self.scroll[0], tile['pos'][1] - self.scroll[1], tile_img.get_width(), tile_img.get_height())
                    if tile_r.collidepoint(mpos):
                        self.tilemap.offgrid_tiles.remove(tile)


            self.display.blit(current_tile_img, (5, 5))

            for event in pygame.event.get():
                # -- Exit Game --
                if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                # -- Mouse Down --
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.left_clicking = True
                        if not self.ongrid:
                            self.tilemap.offgrid_tiles.append({'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': (mpos[0] + self.scroll[0], mpos[1] + self.scroll[1])})
                    if event.button == 3:
                        self.right_clicking = True
                    if self.shift:
                        if event.button == 4:
                            self.tile_variant = (self.tile_variant - 1 ) % len(self.assets[self.tile_list[self.tile_group]])
                        if event.button == 5:
                            self.tile_variant = (self.tile_variant + 1 ) % len(self.assets[self.tile_list[self.tile_group]])
                    else:
                        if event.button == 4:
                            self.tile_group = (self.tile_group - 1 ) % len(self.tile_list)
                            self.tile_variant = 0
                        if event.button == 5:
                            self.tile_group = (self.tile_group + 1 ) % len(self.tile_list)
                            self.tile_variant = 0

                # -- Mouse Up --
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.left_clicking = False
                    if event.button == 3:
                        self.right_clicking = False
            
                # -- Key Down --        
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_w:
                        self.movement[2] = True
                    if event.key == pygame.K_s:
                        self.movement[3] = True
                    if event.key == pygame.K_g:
                        self.ongrid = not self.ongrid
                    if event.key == pygame.K_t:
                        self.tilemap.autotile()
                    if event.key == pygame.K_o:
                        self.tilemap.save('assets/maps/map.json')
                    if event.key == pygame.K_LSHIFT:
                        self.shift = True

                # -- Key Up --
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False
                    if event.key == pygame.K_w:
                        self.movement[2] = False
                    if event.key == pygame.K_s:
                        self.movement[3] = False
                    if event.key == pygame.K_LSHIFT:
                        self.shift = False

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

MapEditor().run()
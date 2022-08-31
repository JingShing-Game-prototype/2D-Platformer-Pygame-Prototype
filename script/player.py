import pygame
from entity import Entity

class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, create_jump_or_run_particles):
        super().__init__(groups)
        self.import_character_assets()
        self.obstacle_sprites = obstacle_sprites
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['idle'][self.frame_index]
        # self.image = pygame.Surface((32, 64))
        # self.image.fill('red')
        self.rect = self.image.get_rect(topleft = pos)

        # dust particles
        self.create_jump_or_run_particles = create_jump_or_run_particles
        
        # player movement
        self.direction = pygame.math.Vector2(0, 0)
        self.or_speed = 8
        self.speed = self.or_speed
        self.or_gravity = 0.8
        self.gravity = self.or_gravity
        self.or_jump_speed = -16
        self.jump_speed = self.or_jump_speed

        # player status
        self.status = 'idle'
        self.flip = False
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

    def import_character_assets(self):
        self.animations = {
            'idle':[],
            'run':[],
            'jump':[],
            'fall':[],
        }
        for index, animation in enumerate(self.animations.keys()):
            image = pygame.Surface((32, 64))
            value_r = (index*30)%255
            value_g = (index*60)%255
            value_b = (index*90)%255
            image.fill((value_r, value_g, value_b))
            self.animations[animation].append(image)

    def animate(self):
        animation = self.animations[self.status]

        # loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)] if not self.flip else pygame.transform.flip(animation[int(self.frame_index)], True, False)

        # set rect
        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright = self.rect.topright)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft = self.rect.topleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop = self.rect.midtop)
        else:
            self.rect = self.image.get_rect(center = self.rect.center)

    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.flip = False
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.flip = True
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] and self.on_ground:
            self.gravity = self.or_gravity
            self.jump()
            self.create_jump_or_run_particles(self.rect.midbottom)

    def get_status(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > self.gravity+0.1:
            self.status = 'fall'
        else:
            if self.direction.x !=0:
                self.status = 'run'
            else:
                self.status = 'idle'

    def update(self):
        self.common_cooldown()
        self.get_input()
        self.get_status()
        self.animate()
        self.run_dust_animation()
        self.move()
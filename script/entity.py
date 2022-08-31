import pygame
from random import randint
from settings import resource_path, map_width, map_height

# for player or enemy
class Entity(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.used_groups = groups
        self.object_type = 'entity'
        self.type = None
        self.frame_index = 0
        self.animation_speed = 0.15

        # status
        self.invinsible = False
        self.invinsible_time = None
        self.invinsible_duration = 500
        self.or_health = 100
        self.health = self.or_health
        self.status = 'idle'
        self.crouch = False
        self.flip = False
        # not flip is right
        # flip is left
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

        # movement
        self.direction = pygame.math.Vector2(0, 0)
        self.or_speed = 8
        self.speed = self.or_speed
        self.or_gravity = 0.8
        self.gravity = self.or_gravity
        self.or_jump_speed = -16
        self.jump_speed = self.or_jump_speed

    def run_dust_animation(self):
        if self.status == 'run' and self.on_ground:
            # self.dust_frame_index += self.dust_animation_speed
            # if self.dust_frame_index >= len(self.dust_run_particles):
            #     self.dust_frame_index = 0
            # dust_particle = self.dust_run_particles[int(self.dust_frame_index)] if not self.flip else pygame.transform.flip(self.dust_run_particles[int(self.dust_frame_index)], True, False)
            # pos = self.rect.bottomleft - pygame.math.Vector2(6, 10) if not self.flip else self.rect.bottomright - pygame.math.Vector2(6, 10)
            self.create_jump_or_run_particles(self.rect.midbottom, 'run')

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

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed

    def move(self):
        self.rect.x += self.direction.x * self.speed
        self.collision('horizontal')
        self.apply_gravity()
        self.collision('vertical')
        self.over_border()

    def over_border(self):
        # if out map it's a loop
        if self.rect.y < -100 and self.direction.y < 0:
            self.rect.y = 0
            self.direction.y = 0
        elif self.rect.y > map_height + 200:
            self.rect.y -= 1000
            self.direction.y = 0
        if self.rect.x > map_width + 500:
            self.rect.x = 0
        elif self.rect.x < 0 - 500:
            self.rect.x = map_width

    def collision(self, direction):
        for sprite in self.obstacle_sprites:
            if sprite == self:
                pass
            else:
                if direction == 'horizontal':
                    if sprite.rect.colliderect(self.rect):
                        if self.direction.x < 0:
                            self.rect.left = sprite.rect.right
                            self.on_left = True
                            self.current_x = self.rect.left
                        if self.direction.x > 0:
                            self.rect.right = sprite.rect.left
                            self.on_right = True
                            self.current_x = self.rect.right

                    if self.on_left and (self.rect.left < self.current_x or self.direction.x >= 0):
                        self.on_left = False
                    if self.on_right and (self.rect.right > self.current_x or self.direction.x <= 0):
                        self.on_right = False

                elif direction == 'vertical':
                    if sprite.rect.colliderect(self.rect):
                        if self.direction.y > 0:
                            self.rect.bottom = sprite.rect.top
                            self.direction.y = 0
                            self.on_ground = True
                        elif self.direction.y < 0:
                            self.rect.top = sprite.rect.bottom
                            self.direction.y = 0
                            self.on_ceiling = True

            if self.on_ground and self.direction.y < 0 or self.direction.y > 1:
                self.on_ground = False
            if self.on_ceiling and self.direction.y > 0.1:
                self.on_ceiling = False

    def common_cooldown(self):
        now = pygame.time.get_ticks()
        if self.invinsible:
            if now - self.invinsible_time > self.invinsible_duration:
                self.invinsible = False

    def get_damage(self, value):
        if not self.invinsible:
            self.health -= value
            if self.health <= 0:
                # create body flesh
                for _ in range(randint(5, 10)):
                    self.create_flesh(self.rect.center)
                self.move_to_object_pool(self.weapon)
                # self.weapon.kill()
                self.move_to_object_pool(self)
            else:
                self.invinsible = True
                self.invinsible_time = pygame.time.get_ticks()

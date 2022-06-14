import time

import pygame as pg
import pygame as pg
from random import uniform, choice, random
from settings import *
from tilemap import collide_hit_rect

vec = pg.math.Vector2


def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y, speed):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.speed = speed
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.rot = 0
        self.last_shot = 0
        self.health = PLAYER_HEALTH
        self.weapon = 'book'

    def get_keys(self):
        self.rot_speed = 0
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        mouse = pg.mouse.get_pressed(num_buttons=3)
        mouse_pos = pg.mouse.get_pos()
        player_center = pg.math.Vector2(480, 360)
        center = pg.math.Vector2(1, 0)
        self.angle = pg.math.Vector2(mouse_pos - player_center).angle_to(center)
        if (self.angle < 0):
            self.angle = 360 + self.angle
        # print(self.angle)

        # 방향키 설정
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel = vec(-self.speed, 0)
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel = vec(self.speed, 0)
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel = vec(0, -self.speed)
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel = vec(0, self.speed)
        if keys[pg.K_LEFT] and keys[pg.K_UP]:  # 대각선 이동 실험
            self.vel = vec(-self.speed, -self.speed)
        if keys[pg.K_RIGHT] and keys[pg.K_UP]:  # 대각선 이동 실험
            self.vel = vec(self.speed, -self.speed)
        if keys[pg.K_LEFT] and keys[pg.K_DOWN]:  # 대각선 이동 실험
            self.vel = vec(-self.speed, self.speed)
        if keys[pg.K_RIGHT] and keys[pg.K_DOWN]:  # 대각선 이동 실험
            self.vel = vec(self.speed, self.speed)

        if keys[pg.K_a] and keys[pg.K_w]:  # 대각선 이동 실험
            self.vel = vec(-self.speed, -self.speed)
        if keys[pg.K_d] and keys[pg.K_w]:  # 대각선 이동 실험
            self.vel = vec(self.speed, -self.speed)
        if keys[pg.K_a] and keys[pg.K_s]:  # 대각선 이동 실험
            self.vel = vec(-self.speed, self.speed)
        if keys[pg.K_d] and keys[pg.K_s]:  # 대각선 이동 실험
            self.vel = vec(self.speed, self.speed)

        if keys[pg.K_SPACE] or mouse[0]:
            self.shoot()

    def shoot(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > WEAPONS[self.weapon]['rate']:
            self.last_shot = now
            dir = vec(1, 0).rotate(-self.rot)
            pos = self.pos + BARREL_OFFSET.rotate(-self.rot)
            self.vel = vec(-WEAPONS[self.weapon]['kickback'], 0).rotate(-self.rot)
            for i in range(WEAPONS[self.weapon]['bullet_count']):
                spread = uniform(-WEAPONS[self.weapon]['spread'], WEAPONS[self.weapon]['spread'])
                Bullet(self.game, pos, dir.rotate(spread))
                # snd = choice(self.game.weapon_sounds[self.weapon])
                # if snd.get_num_channels() > 2:
                # snd.stop()
                # snd.play()

    def update(self):
        self.get_keys()
        self.rot = self.angle  # 이부분이 이미지 움직이는 파트
        self.image = pg.transform.rotate(self.game.player_img, 0)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center

    def add_health(self, amount):
        self.health += amount
        if self.health > PLAYER_HEALTH:
            self.health = PLAYER_HEALTH


class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y, type):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # self.image = game.mob_img
        self.image = game.mob_images[type]
        self.rect = self.image.get_rect()
        self.type = type
        self.hit_rect = MOB[type]['hit_rect'].copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.health = MOB[type]['mob_health']
        self.speed = MOB[type]['mob_speeds']

    def avoid_mobs(self):
        for mob in self.game.mobs:
            if mob != self:
                dist = self.pos - mob.pos
                if 0 < dist.length() < 50:
                    self.acc += dist.normalize()

    def update(self):
        dis = self.game.player.pos - self.pos
        if (pg.math.Vector2.length(dis) < 200):
            self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
        self.rot = (self.game.player.pos - self.pos).angle_to(vec(1, 0))

        # self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.avoid_mobs()
        self.acc = vec(1, 0).rotate(-self.rot)
        self.acc.scale_to_length(self.speed)
        self.acc += self.vel * -1
        self.vel += self.acc * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        if self.health <= 0:
            choice(self.game.zombie_hit_sounds).play()
            self.kill()

    def draw_health(self):
        if self.health > (MOB[self.type]['mob_health'] / 3) * 2:
            col = GREEN
        elif self.health > (MOB[self.type]['mob_health'] / 3):
            col = YELLOW
        else:
            col = RED
        width = int(self.rect.width * self.health / MOB[self.type]['mob_health'])
        self.health_bar = pg.Rect(0, 0, width, 7)
        if self.type == 'boss':
            width = width * 4
            self.health_bar = pg.Rect(0, 0, width, 10)
        if self.health < MOB[self.type]['mob_health'] - 1:
            pg.draw.rect(self.image, col, self.health_bar)


class Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, dir):
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # self.image = game.bullet_images[WEAPONS[game.player.weapon]['bullet_size']]
        self.image = game.bullet_image
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos
        # spread = uniform(-GUN_SPREAD, GUN_SPREAD)
        self.vel = dir * WEAPONS[game.player.weapon]['bullet_speed']
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > WEAPONS[self.game.player.weapon]['bullet_lifetime']:
            self.kill()


class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y


class Item(pg.sprite.Sprite):
    def __init__(self, game, pos, type):
        self.groups = game.all_sprites, game.items
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.item_images[type]
        self.rect = self.image.get_rect()
        self.type = type
        self.rect.center = pos
        self.pos = pos

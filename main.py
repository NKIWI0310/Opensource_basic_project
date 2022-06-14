import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
from tilemap import *
import time

# HUD functions

def draw_player_health(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    if pct > 0.6:
        col = GREEN
    elif pct > 0.3:
        col = YELLOW
    else:
        col = RED
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)

class Game:
    def __init__(self):
        self.draw_debug = None
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)  # 꾹누르면 움직이게 하는 코드 (500밀리초동안기다리고,100밀리초동안 반복)
        self.load_data()

    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def load_data(self):
        self.check_time1 = 0  # speed1
        self.check_time2 = 0  # speed2
        self.check_time3 = 0  # invincible1
        self.check_time4 = 0  # invincible2
        self.check_time5 = 0  # power_up1
        self.check_time6 = 0  # power_up2
        self.invincible_check1 = 0
        self.invincible_check2 = 0
        self.power_up1_check1 = 0
        self.power_up2_check2 = 0
        game_folder = path.dirname(__file__)  # 현재 main이있는 파일 경로
        img_folder3 = path.join(game_folder, 'frames')
        map_folder = path.join(game_folder, 'maps2')
        snd_folder = path.join(game_folder, 'snd')  # add
        pain_folder = path.join(snd_folder, 'pain')  # add
        music_folder = path.join(game_folder, 'music')  # add
        img_folder = path.join(game_folder, 'img')
        self.start_img = pg.image.load(path.join(img_folder, '그림.png'))
        self.badend_img = pg.image.load(path.join(img_folder, 'hapend.png'))
        self.hapend_img = pg.image.load(path.join(img_folder, 'badend.png'))
        self.title_font = path.join(img_folder, 'ZOMBIE.TTF')
        self.start_font = path.join(img_folder, 'aa.ttf')
        self.map = TiledMap(path.join(map_folder, 'newmap.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.player_img = pg.image.load(path.join(img_folder3, PLAYER_IMG)).convert_alpha()
        self.bullet_images = {}
        self.bullet_image = pg.image.load(path.join(img_folder3, 'book.png')).convert_alpha()
        self.item_images = {}
        for item in ITEM_IMAGES:
            self.item_images[item] = pg.image.load(path.join(img_folder3, ITEM_IMAGES[item])).convert_alpha()
        self.mob_images = {}
        for mob in MOB_IMAGES:
            self.mob_images[mob] = pg.image.load(path.join(img_folder3, MOB_IMAGES[mob])).convert_alpha()
            if mob == 'boss':
                self.mob_images[mob] = pg.transform.scale(self.mob_images[mob], (64, 64))
        # Sound loading
        pg.mixer.music.load(path.join(music_folder, BG_MUSIC))  # 뮤직폴더에서 가져오기 위해 선언
        self.effects_sounds = {}  ##힐팩사운드
        for type in EFFECTS_SOUNDS:
            if (type == 'level_start'):
                start_music = pg.mixer.Sound(path.join(snd_folder, EFFECTS_SOUNDS[type]))
                start_music.set_volume(0.1)
                self.effects_sounds[type] = start_music
            else:
                effect = pg.mixer.Sound(path.join(snd_folder, EFFECTS_SOUNDS[type]))
                effect.set_volume(0.2)
                self.effects_sounds[type] = effect
        self.weapon_sounds = {}  ##무기소리
        for snd in WEAPON_SOUNDS_GUN:
            s = pg.mixer.Sound(path.join(snd_folder, WEAPON_SOUNDS_GUN[snd]))
            s.set_volume(0.2)
            self.weapon_sounds[snd] = s
        self.player_hit_sounds = []  ##플레이어 소리
        for player in PLAYER_HIT_SOUNDS:
            self.player_hit_sounds.append(pg.mixer.Sound(path.join(pain_folder, player)))
        self.zombie_hit_sounds = []  ##좀비 히트소리
        for mob in ZOMBIE_HIT_SOUNDS:
            self.zombie_hit_sounds.append(pg.mixer.Sound(path.join(snd_folder, mob)))

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.items = pg.sprite.Group()
        for tile_object in self.map.tmxdata.objects:
            obj_center = vec(tile_object.x + tile_object.width / 2,
                             tile_object.y + tile_object.height / 2)
            if tile_object.name == 'player':
                self.player = Player(self, obj_center.x, obj_center.y, PLAYER_SPEED1)
            if tile_object.name == 'guard_zombie':
                Mob(self, obj_center.x, obj_center.y, tile_object.name)
            if tile_object.name == 'normal_zombie':
                Mob(self, obj_center.x, obj_center.y, tile_object.name)
            if tile_object.name in ['boss_zombie']:
                Mob(self, obj_center.x, obj_center.y, tile_object.name)
            if tile_object.name in ['yellow_zombie']:
                Mob(self, obj_center.x, obj_center.y, tile_object.name)
            if tile_object.name in ['dog_zombie']:
                Mob(self, obj_center.x, obj_center.y, tile_object.name)
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name in ['health1']:
                Item(self, obj_center, tile_object.name)
            if tile_object.name in ['health2']:
                Item(self, obj_center, tile_object.name)
            if tile_object.name in ['speed1']:
                Item(self, obj_center, tile_object.name)
            if tile_object.name in ['speed2']:
                Item(self, obj_center, tile_object.name)
            if tile_object.name in ['invincible1']:
                Item(self, obj_center, tile_object.name)
            if tile_object.name in ['invincible2']:
                Item(self, obj_center, tile_object.name)
            if tile_object.name in ['power_up1']:
                Item(self, obj_center, tile_object.name)
            if tile_object.name in ['power_up2']:
                Item(self, obj_center, tile_object.name)
            if tile_object.name in ['notebook']:
                Item(self, obj_center, tile_object.name)
            if tile_object.name in ['chest']:
                Item(self, obj_center, tile_object.name)
            if tile_object.name in ['newspaper']:
                Item(self, obj_center, tile_object.name)
            if tile_object.name in ['tablet']:
                Item(self, obj_center, tile_object.name)
            if tile_object.name in ['book']:
                Item(self, obj_center, tile_object.name)
        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False
        self.effects_sounds['level_start'].play()  ##시작할때 음악

    def run(self):  # 동작시키는 함수
        # game loop - set self.playing = False to end the game
        self.playing = True
        pg.mixer.music.play(loops=-1)  # add -1이면 반복재생
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()  # event
            self.update()  # update
            self.draw()  # draw
            if (len(self.mobs) == 0):
                break;
        if self.playing == True:
            return "win"
        if len(self.mobs) != 0:
            return "lose"

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.timer = pg.time.get_ticks() / 1000
        if self.check_time1 != 0:
            if self.check_time1 + SPEED_TIME_LIMIT1 < self.timer:
                self.player.speed = PLAYER_SPEED1
                self.check_time1 = 0
        if self.check_time2 != 0:
            if self.check_time2 + SPEED_TIME_LIMIT2 < self.timer:
                self.player.speed = PLAYER_SPEED1
                self.check_time2 = 0
        self.all_sprites.update()
        self.camera.update(self.player)
        hits = pg.sprite.spritecollide(self.player, self.items, False)
        hits2 = pg.sprite.spritecollide(self.player, self.items, False)

        for tile_object in self.map.tmxdata.objects:
            obj_center = vec(tile_object.x + tile_object.width / 2,
                             tile_object.y + tile_object.height / 2)

        for hit in hits:
            if hit.type == 'health1' and self.player.health < PLAYER_HEALTH:
                self.effects_sounds['health_up'].play()
                hit.kill()
                self.player.add_health(HEALTH_PACK_AMOUNT1)

            if hit.type == 'health2' and self.player.health < PLAYER_HEALTH:
                self.effects_sounds['health_up'].play()
                hit.kill()
                self.player.add_health(HEALTH_PACK_AMOUNT2)

            if hit.type == 'speed1':
                self.effects_sounds['health_up'].play()
                hit.kill()
                self.check_time1 = self.timer
                self.player.speed = PLAYER_SPEED2

            if hit.type == 'speed2':
                self.effects_sounds['health_up'].play()
                hit.kill()
                self.check_time2 = self.timer
                self.player.speed = PLAYER_SPEED3

            if hit.type == 'invincible1':
                self.effects_sounds['health_up'].play()
                hit.kill()
                self.check_time3 = self.timer
                self.invincible_check1 = 1

            if hit.type == 'invincible2':
                self.effects_sounds['health_up'].play()
                hit.kill()
                self.check_time4 = self.timer
                self.invincible_check2 = 1

            if hit.type == 'power_up1':
                self.effects_sounds['health_up'].play()
                hit.kill()
                self.check_time5 = self.timer
                self.power_up1_check1 = 1

            if hit.type == 'power_up2':
                self.effects_sounds['health_up'].play()
                hit.kill()
                self.check_time6 = self.timer
                self.power_up2_check2 = 1

        for hit in hits:
            game_folder = path.dirname(__file__)  # 현재 main이있는 파일 경로
            img_folder3 = path.join(game_folder, 'frames')

            if hit.type == 'notebook':
                self.effects_sounds['health_up'].play()
                hit.kill()
                self.player.weapon = 'notebook'
                self.bullet_image = pg.image.load(path.join(img_folder3, ITEM_IMAGES['notebook'])).convert_alpha()

            if hit.type == 'newspaper':
                self.effects_sounds['health_up'].play()
                hit.kill()
                self.player.weapon = 'newspaper'
                self.bullet_image = pg.image.load(path.join(img_folder3, ITEM_IMAGES['newspaper'])).convert_alpha()

            if hit.type == 'tablet':
                self.effects_sounds['health_up'].play()
                hit.kill()
                self.player.weapon = 'tablet'
                self.bullet_image = pg.image.load(path.join(img_folder3, ITEM_IMAGES['tablet'])).convert_alpha()

            if hit.type == 'book':
                self.effects_sounds['health_up'].play()
                hit.kill()
                self.player.weapon = 'book'
                self.bullet_image = pg.image.load(path.join(img_folder3, ITEM_IMAGES['book'])).convert_alpha()

        # mobs hit player
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        for hit in hits:
            if random() < 0.7:
                choice(self.player_hit_sounds).play()
            if self.invincible_check1 == 0 and self.invincible_check2 == 0:
                self.player.health -= MOB[hit.type]['mob_damage']
            else:
                if self.check_time3 != 0:
                    if self.check_time3 + INVINCIBLE_TIME_LIMIT1 < self.timer:
                        self.player.health -= 0
                        self.invincible_check1 = 0
                if self.check_time4 != 0:
                    if self.check_time4 + INVINCIBLE_TIME_LIMIT2 < self.timer:
                        self.player.health -= 0
                        self.invincible_check2 = 0
            hit.vel = vec(0, 0)
            if self.player.health <= 0:
                self.playing = False
            if hits:
                self.player.pos += vec(MOB[hit.type]['mob_knockback'], 0).rotate(-hits[0].rot)

        # bullets hit mobs
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for hit in hits:
            if (hit.health > 0):
                self.weapon_sounds['gun'].play()
            if self.power_up1_check1 == 0:
                hit.health -= WEAPONS[self.player.weapon]['damage'] * len(hits[hit])
            if self.power_up2_check2 == 0:
                hit.health -= WEAPONS[self.player.weapon]['damage'] * len(hits[hit])

            else:
                if self.check_time5 != 0:
                    if self.check_time5 + POWER_UP_TIME1 > self.timer:
                        hit.health -= (WEAPONS[self.player.weapon]['damage'] * 1.5) * len(hits[hit])
                    else:
                        self.power_up1_check1 = 0
                if self.check_time6 != 0:
                    if self.check_time6 + POWER_UP_TIME2 > self.timer:
                        hit.health -= (WEAPONS[self.player.weapon]['damage'] * 1.5) * len(hits[hit])
                    else:
                        self.power_up1_check1 = 0
            hit.vel = vec(0, 0)

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        for sprite in self.all_sprites:
            if isinstance(sprite, Mob):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.draw_debug:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(sprite.hit_rect), 1)
        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(wall.rect), 1)
        self.draw_text('남은 좀비 수 : {}'.format(len(self.mobs)), self.start_font, 30, RED,
                       WIDTH - 20, 10, align="ne")

        draw_player_health(self.screen, 10, 10, self.player.health / PLAYER_HEALTH)
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_h:
                    self.draw_debug = not self.draw_debug

    def show_start_screen(self):
        self.screen.blit(self.start_img, [0, 0])
        self.draw_text("대학교 탈출일지", self.start_font, 50, RED,
                      WIDTH / 2, HEIGHT - HEIGHT * 3 / 4, align="center")
        self.draw_text("시작 : 아무키나 누르세요", self.start_font, 25, BLACK,
                       WIDTH / 2, HEIGHT - HEIGHT * 1 / 2, align="center")
        self.draw_text("게임 종료 : ESC를 누르세요", self.start_font, 25, BLACK,
                       WIDTH / 2, HEIGHT - HEIGHT * 1.3 / 3, align="center")
        pg.display.flip()
        self.wait_for_key()

    def show_rego_screen(self):
        self.screen.blit(self.badend_img, [0, 0])
        self.draw_text("게임 오버", self.start_font, 50, RED,
                       WIDTH / 2, HEIGHT / 2, align="center")
        self.draw_text("다시 시작 : 아무키나 누르세요", self.start_font, 25, RED,
                       WIDTH / 2, HEIGHT * 3 / 4, align="center")
        self.draw_text("게임 종료 : ESC를 누르세요", self.start_font, 25, RED,
                       WIDTH / 2, HEIGHT * 5 / 6, align="center")
        pg.display.flip()
        self.wait_for_key()

    def show_end_screen(self):
        self.screen.blit(self.hapend_img, [0, 0])
        self.draw_text("탈출!", self.start_font, 50, RED,
                       WIDTH / 2, HEIGHT / 2, align="center")
        self.draw_text("다시 시작 : 아무키나 누르세요", self.start_font, 25, BLACK,
                       WIDTH / 2, HEIGHT * 3 / 4, align="center")
        self.draw_text("게임 종료 : ESC를 누르세요", self.start_font, 25, BLACK,
                       WIDTH / 2, HEIGHT * 5 / 6, align="center")
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        pg.event.wait()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        waiting = False
                        self.quit()
                    else:
                        waiting = False
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()


is_paused = False


def toggle_pause():
    global is_paused
    if is_paused == True:
        is_paused = False
    else:
        is_paused = True


# create the game object
g = Game()
g.show_start_screen()
g.effects_sounds['level_start'].play()

while True:
    g.new()
    result = g.run()
    if result == "lose":
        g.show_rego_screen()
    if result == "win":
        g.show_end_screen()

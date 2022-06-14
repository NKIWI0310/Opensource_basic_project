import pygame as pg

vec = pg.math.Vector2

# 컬러 정하기
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (100, 55, 5)
CYAN = (0, 255, 255)

# 게임 세팅
WIDTH = 960
HEIGHT = 720
FPS = 60
TITLE = "대학교 탈출하기"

SPEED_TIME_LIMIT1 = 5
SPEED_TIME_LIMIT2 = 8
INVINCIBLE_TIME_LIMIT1 = 10
INVINCIBLE_TIME_LIMIT2 = 15
POWER_UP_TIME1 = 5
POWER_UP_TIME2 = 8

# Player settings
PLAYER_HEALTH = 100
PLAYER_SPEED1 = 230
PLAYER_SPEED2 = 500
PLAYER_SPEED3 = 510
PLAYER_ROT_SPEED = 250
PLAYER_IMG = 'hero1.png'
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)
BARREL_OFFSET = vec(30, 10)

# Weapon settings
BULLET_IMG = 'weapon_katana.png'
WEAPONS = {}
WEAPONS['newspaper'] = {'bullet_speed': 500,
                     'bullet_lifetime': 4000,
                     'rate': 230,
                     'kickback': 200,
                     'spread': 0,
                     'damage': 25,
                     'bullet_size': 'lg',
                     'bullet_count': 1,
                     'bullet_image': 'newspaper.gif'}

WEAPONS['notebook'] = {'bullet_speed': 150,
                   'bullet_lifetime': 3500,
                   'rate': 400,
                   'kickback': 250,
                   'spread': 3,
                   'damage': 75,
                   'bullet_size': 'lg',
                   'bullet_count': 1,
                   'bullet_image': 'notebook.gif'}

WEAPONS['tablet'] = {'bullet_speed': 300,
                          'bullet_lifetime': 3000,
                          'rate': 200,
                          'kickback': 50,
                          'spread': 10,
                          'damage': 1000,
                          'bullet_size': 'lg',
                          'bullet_count': 5,
                          'bullet_image': 'tablet1.gif'
                          }

WEAPONS['book'] = {'bullet_speed': 700,
                   'bullet_lifetime': 8000,
                   'rate': 600,
                   'kickback': 500,
                   'spread': 1,
                   'damage': 50,
                   'bullet_size': 'lg',
                   'bullet_count': 1,
                   'bullet_image': 'book.png'
                   }

# Mob settings
MOB = {}
MOB['guard_zombie'] = {
    'mob_speeds': 100,
    'mob_health': 500,
    'hit_rect': pg.Rect(0, 0, 30, 30),
    'mob_damage': 10,
    'mob_knockback': 15,
    'avoid_radius': 50
}
MOB['normal_zombie'] = {
    'mob_speeds': 200,
    'mob_health': 400,
    'hit_rect': pg.Rect(0, 0, 30, 30),
    'mob_damage': 5,
    'mob_knockback': 10,
    'avoid_radius': 200
}
MOB['yellow_zombie'] = {
    'mob_speeds': 100,
    'mob_health': 360,
    'hit_rect': pg.Rect(0, 0, 30, 30),
    'mob_damage': 60,
    'mob_knockback': 100,
    'avoid_radius': 50
}

MOB['boss_zombie'] = {
    'mob_speeds': 100,
    'mob_health': 3000,
    'hit_rect': pg.Rect(0, 0, 30, 30),
    'mob_damage': 34,
    'mob_knockback': 100,
    'avoid_radius': 50
}

MOB['dog_zombie'] = {
    'mob_speeds': 350,
    'mob_health': 500,
    'hit_rect': pg.Rect(0, 0, 150, 150),
    'mob_damage': 20,
    'mob_knockback': 100,
    'avoid_radius': 200
}

MOB_IMAGES = {'guard_zombie': '수위좀비.png',
              'normal_zombie': 'normal_zombie.png',
              'yellow_zombie': 'zombie2.png',
              'boss_zombie': 'boss.png',
              'dog_zombie': '개좀비.png'
              }

# Items
ITEM_IMAGES = {'health1': 'flask_red.png',
               'health2': 'flask_big_red.png',
               'notebook': 'notebook.gif',
               'newspaper': 'newspaper.gif',
               'tablet': 'tablet1.gif',
               'book': 'book.png',
               'speed1': 'flask_blue.png',
               'speed2': 'flask_big_blue.png',
               'invincible1': 'flask_green.png',
               'invincible2': 'flask_big_green.png',
               'power_up1': 'flask_yellow.png',
               'power_up2': 'flask_big_yellow.png'
               }
HEALTH_PACK_AMOUNT1 = 20
HEALTH_PACK_AMOUNT2 = 40

BG_MUSIC = '과제곡.mp3'
PLAYER_HIT_SOUNDS = ['pain8.wav', 'pain9.wav', 'pain10.wav', 'pain11.wav']
ZOMBIE_HIT_SOUNDS = ['splat-15.wav']
WEAPON_SOUNDS_GUN = {'gun': 'sfx_weapon_singleshot2.wav', 'attack': 'shout_effect.mp3'}
EFFECTS_SOUNDS = {'level_start': 'level_start.wav',
                  'health_up': 'health_pack.wav'}

#Composed by: Jon K. Fite
import pygame as pg
import random
from os import path
from time import sleep

img_folder = path.join(path.dirname(__file__), 'Img')
snd_folder = path.join(path.dirname(__file__), 'Snd')

HEIGHT = 600
WIDTH = 1200
FPS = 60
TITLE = 'Space Invaders for David'
turn = False
round2 = False

#define colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)

pg.init()
pg.mixer.init()
window = pg.display.set_mode((WIDTH,HEIGHT))
pg.display.set_caption(TITLE)
clock = pg.time.Clock()

font_name = pg.font.match_font('arial')
def draw_text(surf,x,y,text,size, color):
	font = pg.font.Font(font_name, size)
	text_surface = font.render(text, True, color)
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x,y)
	surf.blit(text_surface, text_rect)

def show_go_screen():
	window.fill(BLUE)
	window.blit(bg, bg_rect)
	draw_text(window, WIDTH//2, HEIGHT//4, 'SPACE INVADERS', 30, WHITE)
	draw_text(window, WIDTH//2, HEIGHT * 1/2, 'Arrow Keys to move. Space to shoot', 20, WHITE)
	draw_text(window, WIDTH//2, HEIGHT *3/4, 'Press any key to start', 15, WHITE)
	pg.display.flip()
	sleep(0.5)
	waiting = True
	while waiting:
		clock.tick(FPS)
		for event in pg.event.get():
			if event.type == pg.QUIT:
				waiting = False
				pg.quit()
			if event.type == pg.KEYUP:
				waiting = False

def draw_lives(surf, x, y, lives, img):
	for i in range(lives):
		img_rect = img.get_rect()
		img_rect.x = x + 40 * i
		img_rect.y = y
		surf.blit(img, img_rect)

def win_screen():
	global music_on
	draw_text(window, WIDTH//2, HEIGHT//2, 'YOU WON!!!', 100, WHITE)
	draw_text(window, WIDTH//2, HEIGHT//2 + 100, 'Press any key to continue', 25, WHITE)
	pg.display.flip()
	music_on = False
	pg.mixer.music.stop()
	pg.mixer.music.load(path.join(snd_folder, 'Curry.mp3'))
	pg.mixer.music.set_volume(0.4)
	pg.mixer.music.play(loops=-1)
	sleep(2)
	waiting = True
	while waiting:
		clock.tick(FPS)
		for event in pg.event.get():
			if event.type == pg.QUIT:
				waiting = False
				pg.quit()
			if event.type == pg.KEYUP:
				waiting = False

class Player(pg.sprite.Sprite):
	def __init__(self):
		pg.sprite.Sprite.__init__(self)
		self.image = pg.transform.scale(player_img,(75, 58))
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.radius = 28
		#pg.draw.circle(self.image, RED, self.rect.center, self.radius)
		self.rect.centerx = WIDTH / 2
		self.rect.bottom = HEIGHT - 50
		self.speedx = 0
		self.max_speed = 5
		self.reload = 250
		self.last_shot = pg.time.get_ticks()
		self.lives = 3
		self.power_timer = 5000
		self.power_time = pg.time.get_ticks()
		self.power = 1


	def update(self):
		if self.power >= 2 and pg.time.get_ticks() - self.power_time > self.power_timer:
			self.power -= 1
			self.power_timer = pg.time.get_ticks()
		if self.power >= 2:
			self.reload = 75
		if self.power <= 1:
			self.reload = 250
		self.speedx = 0
		keystate = pg.key.get_pressed()
		if keystate[pg.K_LEFT]:
			self.speedx = -self.max_speed
		if keystate[pg.K_RIGHT]:
			self.speedx = self.max_speed
		if keystate[pg.K_LEFT] and keystate[pg.K_RIGHT]:
			self.speedx = 0
		if keystate[pg.K_SPACE]:
			self.Shoot()
		if self.rect.right > WIDTH:
			self.rect.right = WIDTH
		if self.rect.left < 0:
			self.rect.left = 0
		self.rect.centerx += self.speedx

	def Shoot(self):
		now = pg.time.get_ticks()
		if now - self.last_shot > self.reload:
			self.last_shot = now
			player_bulllet_snd.play()
			bullet = Bullet(self.rect.centerx, self.rect.top)
			all_sprites.add(bullet)
			bullets.add(bullet)

	def powerup(self):
		self.power += 1
		self.power_time = pg.time.get_ticks()

class Bullet(pg.sprite.Sprite):
	def __init__(self, x, y):
		pg.sprite.Sprite.__init__(self)
		self.image = player_lazer
		self.rect = self.image.get_rect()
		self.rect.centerx = x
		self.rect.bottom = y
		self.speedy = -10

	def update(self):
		self.rect.y += self.speedy
		if self.rect.bottom < -10:
			self.kill()

class Mob(pg.sprite.Sprite):
	def __init__(self, x, y):
		pg.sprite.Sprite.__init__(self)
		self.image = random.choice(enemies_img)
		self.rect = self.image.get_rect()
		self.radius = 22
		#pg.draw.circle(self.image, RED, self.rect.center, self.radius)
		self.rect.x = x
		self.rect.y = y
		self.speedx = 2
		self.first = False
		self.last_update = pg.time.get_ticks()
		self.moved = True
		self.speed_limit = 30
		self.num_mobs = len(mobs.sprites())

	def update(self):
		global turn, round2


		if round2:
			if not self.first:
				self.speedx = -self.speedx
				self.rect.x += self.speedx
				self.rect.y += self.rect.height + 10
			if self.first:
				self.rect.y += self.rect.height + 10
				self.first = False
		else:

			if self.rect.right + self.speedx > WIDTH - 50 or self.rect.left + self.speedx < 50:
				turn = True

			if turn:
				self.speedx = -self.speedx
				self.first = True

			if self.num_mobs //16 >= len(mobs.sprites()):
				self.speed_limit = 1
			elif self.num_mobs //8 >= len(mobs.sprites()):
				self.speed_limit = 10
			elif self.num_mobs //4 >= len(mobs.sprites()):
				self.speed_limit = 15
			elif self.num_mobs//2 >= len(mobs.sprites()):
				self.speed_limit = 20



			if not turn and pg.time.get_ticks() - self.last_update >= self.speed_limit:
				self.last_update = pg.time.get_ticks()
				self.rect.x += self.speedx

		if random.random() > 0.9995:
			self.shoot()

	def shoot(self):
		mob_bulllet_snd.play()
		bullet = MobBullet(self.rect.centerx, self.rect.bottom)
		all_sprites.add(bullet)
		mob_bullets.add(bullet)

class MobBullet(pg.sprite.Sprite):
	def __init__(self, x, y):
		pg.sprite.Sprite.__init__(self)
		self.image = mob_lazer
		self.rect = self.image.get_rect()
		self.rect.centerx = x
		self.rect.bottom = y
		self.speedy = 10

	def update(self):
		self.rect.y += self.speedy
		if self.rect.top > HEIGHT + 10:
			self.kill()

class Base(pg.sprite.Sprite):
	def __init__(self,x, y):
		pg.sprite.Sprite.__init__(self)
		self.image = pg.Surface((100,25))
		self.image.fill(BLACK)
		self.rect = self.image.get_rect()
		self.rect.midtop = (x, y)
		self.original_location = self.rect.midtop
		self.lives = 3
		self.hidden = False

	def update(self):
		if self.lives <= 0:
			self.hidden = True
		if self.lives >= 1:
			self.hidden = False
			self.rect.midtop = self.original_location
		if self.hidden:
			self.rect.center = (-1000,-10000)

class Pow(pg.sprite.Sprite):
	def __init__(self, center):
		pg.sprite.Sprite.__init__(self)
		self.type = random.choice(powerups_list)
		self.image = powerups_img[self.type]
		self.rect = self.image.get_rect()
		self.rect.center = center
		self.speedy = 5

	def update(self):
		self.rect.y += self.speedy
		if self.rect.top > HEIGHT + 10:
			self.kill()

class Explosion(pg.sprite.Sprite):
	def __init__(self, center, size):
		pg.sprite.Sprite.__init__(self)
		self.size = size
		self.image = explosions_anim[self.size][0]
		self.rect = self.image.get_rect()
		self.rect.center = center
		self.frame = 0
		self.framerate = 75
		self.last_update = pg.time.get_ticks()

	def update(self):
		if pg.time.get_ticks() - self.last_update >= self.framerate:
			self.last_update = pg.time.get_ticks()
			self.frame += 1
			if self.frame == len(explosions_anim[self.size]):
				self.kill()
			else:
				center = self.rect.center
				self.image = explosions_anim[self.size][self.frame]
				self.rect = self.image.get_rect()
				self.rect.center = center

#load graphics
bg = pg.image.load(path.join(img_folder, 'bg_space_seamless.png')).convert()
bg = pg.transform.scale(bg, (WIDTH,675))
bg_rect = bg.get_rect()
player_img = pg.image.load(path.join(img_folder, 'playerShip3_blue.png')).convert()
smol_player = pg.transform.scale(player_img, (30,23))
smol_player.set_colorkey(BLACK)
enemies_img = []
enemies_list = ['enemyBlack3.png', 'enemyBlue4.png', 'enemyGreen2.png']
for img in enemies_list:
	loaded_img = pg.image.load(path.join(img_folder, img)).convert()
	loaded_img = pg.transform.scale(loaded_img, (50,41))
	loaded_img.set_colorkey(BLACK)
	enemies_img.append(loaded_img)

player_lazer = pg.image.load(path.join(img_folder, 'laserGreen09.png')).convert()
mob_lazer = pg.image.load(path.join(img_folder, 'laserRed06.png')).convert()
mob_lazer = pg.transform.rotate(mob_lazer, 180)

powerups_img = {}
powerups_list = ['pill_red.png', 'gun.png', 'pill_blue.png']
for img in powerups_list:
	loaded_img =  pg.image.load(path.join(img_folder, img)).convert()
	loaded_img.set_colorkey(BLACK)
	powerups_img[img] = loaded_img

explosions_anim = {}
explosions_anim['smol'] = []
explosions_anim['big'] = []
explosions_anim['player'] = []
for i in range(9):
	filename = f'regularExplosion0{i}.png'
	img = pg.image.load(path.join(img_folder, filename)).convert()
	img_large = pg.transform.scale(img, (50,50))
	img_large.set_colorkey(BLACK)
	explosions_anim['big'].append(img_large)

	img_smol = pg.transform.scale(img,(40,40))
	img_smol.set_colorkey(BLACK)
	explosions_anim['smol'].append(img_smol)

	filename = f'sonicExplosion0{i}.png'
	img = pg.image.load(path.join(img_folder, filename)).convert()
	img.set_colorkey(BLACK)
	explosions_anim['player'].append(img)

#load sounds
explosion_snd = []
for snd in range(1,4):
	filename = f'Explosion{snd}.wav'
	explosion_snd.append(pg.mixer.Sound(path.join(snd_folder, filename)))
mob_bulllet_snd = pg.mixer.Sound(path.join(snd_folder, 'Laser_Shoot2.wav'))
player_bulllet_snd = pg.mixer.Sound(path.join(snd_folder, 'Laser_Shoot.wav'))
blue_pill_snd = pg.mixer.Sound(path.join(snd_folder, 'Powerup.wav'))
red_pill_snd = pg.mixer.Sound(path.join(snd_folder, 'Powerup4.wav'))
gun_snd = pg.mixer.Sound(path.join(snd_folder, 'Powerup2.wav'))
player_death_snd = pg.mixer.Sound(path.join(snd_folder, 'rumble1.ogg'))
base_hit_snd = pg.mixer.Sound(path.join(snd_folder, 'Explosion8.wav'))
player_hit_snd = pg.mixer.Sound(path.join(snd_folder, 'Hit_Hurt.wav'))
bullet_bullet_snd = pg.mixer.Sound(path.join(snd_folder, 'Laser_Shoot3.wav'))

pg.mixer.music.load(path.join(snd_folder, 'StarMusic.ogg'))
pg.mixer.music.set_volume(0.4)
pg.mixer.music.play(loops=-1)

music_on = True
died = False
bases_alive = False
game_over = True
running = True
while running:
	if game_over:
		show_go_screen()
		all_sprites = pg.sprite.Group()
		bullets = pg.sprite.Group()
		mob_bullets = pg.sprite.Group()
		mobs = pg.sprite.Group()
		bases = pg.sprite.Group()
		powerups = pg.sprite.Group()
		if not music_on:
			pg.mixer.music.stop()
			pg.mixer.music.load(path.join(snd_folder, 'StarMusic.ogg'))
			pg.mixer.music.set_volume(0.4)
			pg.mixer.music.play(loops=-1)
			music_on = True
		player = Player()
		all_sprites.add(player)
		for i in range(6):
			for j in range(11):
				mob = Mob(75*j + 200, 75*i-150)
				all_sprites.add(mob)
				mobs.add(mob)

		for i in range(1,4):
			for j in range(1,4):
				base = Base(WIDTH*i//4, HEIGHT - 150 - 25*j)
				all_sprites.add(base)
				bases.add(base)

		score = 0
		game_over = False
		died = False
		bases_alive = False

	#running at right speed
	clock.tick(FPS)

	#process input(event)
	for event in pg.event.get():	
		if event.type == pg.QUIT:
			running = False 


			
	#check if player has lives
	if player.lives <= 0 and not died:
		player_death_snd.play()
		expl_death = Explosion(player.rect.center, 'player')
		all_sprites.add(expl_death)
		player.kill()
		died = True
	if died and not expl_death.alive():
		game_over = True

	#check if bases are ale
	bases_alive = False
	for base in bases:
		if not base.hidden:
			bases_alive = True
			break

	if not bases_alive:
		game_over = True

	#check if player won:
	if len(mobs.sprites()) <= 0:
		win_screen()
		game_over = True


	#check if mob passed the finish line
	for mob in mobs:
		if mob.rect.top > HEIGHT:
			game_over = True

	#check if bullet hit mob
	hits = pg.sprite.groupcollide(mobs, bullets, True, True)
	for hit in hits:
		score += 100
		random.choice(explosion_snd).play()
		expl = Explosion(hit.rect.center, random.choice(['smol', 'big']))
		all_sprites.add(expl)
		if random.random() > 0.9:
			pow = Pow(hit.rect.center)
			all_sprites.add(pow)
			powerups.add(pow)


	#check enemy hit base
	hits = pg.sprite.groupcollide(bases, mobs, False, True)
	for hit in hits:
		base_hit_snd.play()
		hit.lives -= 1

	#check if player hit base
	hits = pg.sprite.groupcollide(bases, bullets, False, True)
	for hit in hits:
		base_hit_snd.play()
		hit.lives -= 1

	#check if mob bulllet hit base
	hits = pg.sprite.groupcollide(bases, mob_bullets, False, True)
	for hit in hits:
		base_hit_snd.play()
		hit.lives -= 1

	#check if mob bullet hit player
	hits = pg.sprite.spritecollide(player, mob_bullets, True)
	for hit in hits:
		player_hit_snd.play()
		player.lives -= 1

	#check if mob hits player
	hits = pg.sprite.spritecollide(player, mobs, True)
	for hit in hits:
		player_hit_snd.play()
		player.lives -= 1

	#check if player hit powerup
	hits = pg.sprite.spritecollide(player, powerups, True)
	for hit in hits:
		if hit.type == 'pill_red.png':
			red_pill_snd.play()
			player.lives = 3
		if hit.type == 'gun.png':
			gun_snd.play()
			player.powerup()
		if hit.type == 'pill_blue.png':
			blue_pill_snd.play()
			for base in bases:
				base.lives = 3
	#update
	all_sprites.update()
	if turn:
		round2 = True
		all_sprites.update()
		turn = False
		round2 = False

	#draw/render
	window.fill(BLUE)
	window.blit(bg, bg_rect)
	all_sprites.draw(window)
	draw_lives(window, 25, HEIGHT - 35, player.lives, smol_player)
	draw_text(window, WIDTH - 50, HEIGHT - 40, str(score), 25, WHITE)
	#after drawing everything
	pg.display.flip()

pg.quit()
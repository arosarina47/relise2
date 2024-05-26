from random import randint

from pygame import*
from time import time as timer

win_width = 700
win_height = 500
display.set_caption("Catgame")
window = display.set_mode((win_width, win_height))

img_back = "background.jpg"
img_hero = "catcool1.png"
#img_bullet = "bullet.png"
img_bomb = "pixelbomb.png"
img_cookie = "pixelcookie.png"
score = 0
lost = 0
max_lost = 3

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image),(size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self): #щоб вивести на екран персонажів
        window.blit(self.image,(self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width -80:
            self.rect.x += self.speed


#class Bullet(GameSprite):
    #def update(self):
      #self.rect.y += self.speed
      #if self.rect.y < 0:
         # self.kill()

class Bomb(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width -80)
            self.rect.y = -50
            # lost += 1
cat = Player(img_hero, 5, win_height - 109,100,110,10)
bullets = sprite.Group()
bombs = sprite.Group()

for i in range(1,4):
    bomb = Bomb(img_bomb, randint(50, win_width -80), -60, 80, 50,randint(1,5))
    bombs.add(bomb)

cookies = sprite.Group()

for i in range(1,6):
    cookie = Bomb(img_cookie, randint(50, win_width -80), -60, 80, 50,randint(1,5))
    cookies.add(cookie)

mixer.init()


#mixer.init()
#mixer.music.load("spacesound.mp3")
#mixer.music.play()
#fire_sound = mixer.Sound("fire.mp3")

font.init()
font1 = font.SysFont('Arial', 80)
font2 = font.Font(None,36)
win = font1.render('You win!' , True, (255,255,255))
lose = font1.render('You lose!', True, (255,0,0))


background = transform.scale(image.load(img_back),(win_width,win_height))

finish = False
run = True
goal = 11
life = 3
max_fire = 5
real_time = False
num_fire = 0

show_menu = True
show_game = False
def draft_text(text,font,color,surface, x, y): #для того ,щоб текст показувався
    text_object = font.render(text, True, color) #зберігається текст,його колір
    text_rect = text_object.get_rect()#текст рект-щоб отримати координати ,де знаходиться текст
    text_rect.center = (x, y)
    surface.blit(text_object, text_rect)#вивести на екран текст



while run:
    if show_menu:
        for e in event.get():
            if e.type == QUIT:
                run = False
            elif e.type == MOUSEBUTTONDOWN and e.button == 1:
                if 260 <= mouse_pos[0] <= 380 and 160 <= mouse_pos[1] <= 200:
                    background = background
                    show_menu = False
                    show_game = True
                if 260 <= mouse_pos[0] <= 380 and 220 <= mouse_pos[1] <= 270:
                    run = False
                    show_menu = False

        mouse_pos = mouse.get_pos()
        font3 = font.Font(None, 50)
        window.blit(background, (0,0))
        if 260 <= mouse_pos[0] <= 400 and 160 <= mouse_pos[1] <= 210:
            draw_text("Play", font3,(255,0,0), window, 330, 200)
            if mouse.get_pressed()[0]:
                selected = 'Play'
            else:
                draw_text('Play',font3,(255,255,255), window, 330,200)
        if 260 <= mouse_pos[0] <= 380 and 220 <= mouse_pos[1] <=270:
            draw_text('Exit', font3,(255,0,0), window, 330,250)
            if mouse.get_pressed()[0]:
                selected = "Exit"
        else:
            draw_text('Exit', font3,(255,255,255),window, 330,250)
    if show_game:
        for e in event.get():
            if e.type == QUIT:
                run = False
                real_time = True
        if not finish:
            window.blit(background,(0,0))
            cat.update()
            bombs.update()
            cookies.update()
            text = font2.render('Рахунок:' + str(score), True, (255,255,255))
            window.blit(text, (10,20))
            text_lose = font2.render('Пропущено: '+ str(lost), True, (255,255,255))
            window.blit(text_lose, (10,50))
            cat.reset()

            bombs.draw(window)
            cookies.draw(window)
            collides = sprite.spritecollide(cat, bombs, True)
            for c in collides:
                life -= 1
                # score += 1
                bomb = Bomb(img_bomb, randint(50, win_width-80), -60,80,50, randint(1,5))
                bombs.add(bomb)
            collides2 = sprite.spritecollide(cat, cookies, True)
            for c in collides2:
                score += 1
                cookie = Bomb(img_cookie, randint(50, win_width - 80), -60, 80, 50, randint(1, 5))
                cookies.add(cookie)

            if life == 3:
                life_color = (0,150,0)
            if life == 2:
                life_color = (150,0,0)
            if life == 1:
                life_color = (150,0,0)
            text_life = font1.render(str(life), True, life_color)
            window.blit(text_life, (650,10))
            if sprite.spritecollide(cat, bombs, False):
                sprite.spritecollide(cat, bombs, True)
                life -=1
                collides = sprite.spritecollide(cat, bombs, True)
                for c in collides:
                    # score += 1
                    bomb = Bomb(img_bomb, randint(50, win_width - 80), -60, 80, 50, randint(1, 5))
                    bombs.add(bomb)
            if sprite.spritecollide(cat, cookies, False):
                sprite.spritecollide(cat, cookies, True)
                score += 1
                collides = sprite.spritecollide(cat, cookies, True)
                for c in collides:
                    # score += 1
                    cookie = Bomb(img_cookie, randint(50, win_width - 80), -60, 80, 50, randint(1, 5))
                    cookies.add(cookie)
            if life == 0 or lost >= max_lost:
                finish = True
                window.blit(lose, (200,200))
            if score >= goal: #умова виграшу
                finish = True
                window.blit(win, (200,200))
        else:
            time.delay(3000)
            score = 0
            lost = 0
            life = 3
            num_fire = 0
            finish = False
            for b in bullets:
                b.kill()
            for m in bombs:
                m.kill()
            for i in range(1,6):
                bombs = Bomb(img_bomb, randint(50, win_width -80), -60,80,50, randint(1,5))
                bombs.add(bomb)
    display.update()
    time.delay(50) #цикл оновлюється кожні 50 мілісекунд



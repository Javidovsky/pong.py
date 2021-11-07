import pygame
from pygame import mixer

# initialise
pygame.init()

# screen
screen = pygame.display.set_mode((800, 600))

# sound
hitnoise = mixer.Sound("./assets/hit.mp3")

# title background logo stuff
pygame.display.set_caption("pong")


# collision

def checkcollision(object1xpos, object1ypos, object1xlength, object1ylength, object2xpos, object2ypos, object2xlength, object2ylength):
    rect1 = pygame.Rect(object1xpos, object1ypos, object1xlength, object1ylength)
    rect2 = pygame.Rect(object2xpos, object2ypos, object2xlength, object2ylength)
    if rect1.colliderect(rect2):
        return True
    else:
        return False

# objects
player1x = 20
player1y = 250
newplayer1x = 0
newplayer1y = 0

def player1(x, y):
    screen.blit(pygame.image.load("./assets/pongplayer.png"), (x, y))

player2x = 770
player2y = 250
newplayer2x = 0
newplayer2y = 0

def player2(x, y):
    screen.blit(pygame.image.load("./assets/pongplayer.png"), (x, y))

ballx = 500
bally = 250
newballx = -0.5
newbally = -0.5

def ball(x, y):
    screen.blit(pygame.image.load("./assets/pongball.png"), (x, y))

# score
player1score = 0
player2score = 0
num = 0

def showscore(x, y):
    score = pygame.font.Font("./assets/freesansbold.ttf",32).render("Score: " + str(player1score) + " - " + str(player2score), True, (255,255,255))
    screen.blit(score, (x,y))

def showlastscore(x, y):
    score = pygame.font.Font("./assets/freesansbold.ttf",32).render("Last score: " + str(player1score) + " - " + str(player2score), True, (255,255,255))
    screen.blit(score, (x,y))

def player1winscreen(x, y):
    screen.blit(pygame.image.load("./assets/player1win.png"), (x, y))

def player2winscreen(x, y):
    screen.blit(pygame.image.load("./assets/player2win.png"), (x, y))

# misc
def putonscreen(image, x, y):
    screen.blit(pygame.image.load(image), (x, y))

def puttextonscreen(string, x, y):
    text = pygame.font.Font("./assets/freesansbold.ttf",32).render(string, True, (255,255,255))
    screen.blit(text, (x,y))

start_ticks = pygame.time.get_ticks()
lastsec = 0
framenum = 0
fps = 0
running = True
menu = True
game = True
while running:
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                menu = False
                game = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game = True
                    menu = False
        # rgb
        screen.fill((0, 0, 0))
        # text
        putonscreen("./assets/menuscreen.png", 0, 0)
        # update
        pygame.display.update()
    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                menu = False
                game = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu = True
                    game = False
                if event.key == pygame.K_w:
                    newplayer1y -= 0.8
                if event.key == pygame.K_s:
                    newplayer1y += 0.8
                if event.key == pygame.K_UP:
                    newplayer2y -= 0.8
                if event.key == pygame.K_DOWN:
                    newplayer2y += 0.8
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    newplayer1y = 0
                if event.key == pygame.K_s:
                    newplayer1y = 0
                if event.key == pygame.K_UP:
                    newplayer2y = 0
                if event.key == pygame.K_DOWN:
                    newplayer2y = 0

        # rgb
        screen.fill((0, 0, 0))
        # players
        player1y += newplayer1y
        player1(player1x,player1y)
        player2y += newplayer2y
        player2(player2x,player2y)
        # ball
        ballx += newballx
        bally += newbally
        ball(ballx,bally)
        # border
        if player1y <= 0:
            player1y = 0
        if player1y >= 500:
            player1y = 500
        if player2y <= 0:
            player2y = 0
        if player2y >= 500:
            player2y = 500
        if bally <= 0:
            newbally *= -1
        if bally >= 580:
            newbally *= -1
        if ballx <= 0:
            ballx = 390
            newballx = 0.5
            player2score += 1
        if ballx >= 780:
            ballx = 390
            newballx = -0.5
            player1score += 1
        if checkcollision(ballx,bally,20,20,player1x,player1y,10,100):
            hitnoise.play()
            newballx *= -1.1
        if checkcollision(ballx,bally,20,20,player2x,player2y,10,100):
            hitnoise.play()
            newballx *= -1.1
        # score
        showscore(10, 10)
        if player1score == 3:
            player1winscreen(0, 0)
            num += 1
            if num >= 10:
                menu = True
                num = 0
                player2score = 0
                player1score = 0
                game = False
        if player2score == 3:
            player2winscreen(0, 0)
            num += 1
            if num >= 100:
                menu = True
                num = 0
                player2score = 0
                player1score = 0
                game = False
        # fps
        seconds = (pygame.time.get_ticks() - start_ticks) / 1000
        if seconds - lastsec >= 1:
            lastsec += 1
            fps = framenum
            framenum = 0
        framenum += 1
        puttextonscreen(str(fps), 720, 10)
        # update
        pygame.display.update()

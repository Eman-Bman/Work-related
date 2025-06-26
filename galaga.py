import pygame
import time 
import math as m
import random as r

pygame.init()
screen=pygame.display.set_mode((240,320))
clock=pygame.time.Clock()
BLACK=(0,0,0)
WHITE=(255,255,255)
RED=(255,0,0)
GREEN=(0,255,0)
YELLOW=(255,255,0)
TEAL=(0,255,255)
# Set color key for transparency (remove black background)
sprite_sheet = pygame.image.load("sprites.png").convert_alpha()
sprite_sheet.set_colorkey(BLACK)   
player_rect = pygame.Rect(109,1,16,16)
player = pygame.Surface((player_rect.width, player_rect.height), pygame.SRCALPHA)
player.blit(sprite_sheet, (0,0), player_rect)
laser_rect = pygame.Rect(307,118,16,16)
laser = pygame.Surface((laser_rect.width, laser_rect.height), pygame.SRCALPHA)
laser.blit(sprite_sheet, (0,0), laser_rect)
enemyShot_rect = pygame.Rect(307,136,16,16)
enemyShot = pygame.Surface((enemyShot_rect.width, enemyShot_rect.height), pygame.SRCALPHA)
enemyShot.blit(sprite_sheet, (0,0), enemyShot_rect)
zako_rect = pygame.Rect(109,91,16,16)
zako = pygame.Surface((zako_rect.width, zako_rect.height), pygame.SRCALPHA)
zako.blit(sprite_sheet, (0,0), zako_rect)
goei_rect = pygame.Rect(109,73,16,16)
goei = pygame.Surface((goei_rect.width, goei_rect.height), pygame.SRCALPHA)
goei.blit(sprite_sheet, (0,0), goei_rect)
bossFull_rect = pygame.Rect(109,37,16,16)
bossFull = pygame.Surface((bossFull_rect.width, bossFull_rect.height), pygame.SRCALPHA)
bossFull.blit(sprite_sheet, (0,0), bossFull_rect)
bossHalf_rect = pygame.Rect(109,55,16,16)
bossHalf = pygame.Surface((bossHalf_rect.width, bossHalf_rect.height), pygame.SRCALPHA)
bossHalf.blit(sprite_sheet, (0,0), bossHalf_rect)
explosions_rects = [
    pygame.Rect(289, 1, 32, 32),  # Frame 1
    pygame.Rect(323, 1, 32, 32), # Frame 2
    pygame.Rect(357, 1, 32, 32), # Frame 3
    pygame.Rect(391, 1, 32, 32)  # Frame 4
]
explosions = [pygame.Surface((rect.width, rect.height), pygame.SRCALPHA) for rect in explosions_rects]
for i, rect in enumerate(explosions_rects):
    explosions[i].blit(sprite_sheet, (0, 0), rect)
playerExplosions_rects = [
    pygame.Rect(145, 1, 32, 32),  # Frame 1
    pygame.Rect(179, 1, 32, 32), # Frame 2
    pygame.Rect(213, 1, 32, 32), # Frame 3
    pygame.Rect(247, 1, 32, 32)  # Frame 4
]
playerExplosions = [pygame.Surface((rect.width, rect.height), pygame.SRCALPHA) for rect in playerExplosions_rects]
for i, rect in enumerate(playerExplosions_rects):
    playerExplosions[i].blit(sprite_sheet, (0, 0), rect)

text_sheet = pygame.image.load("Text.png").convert_alpha()
text_sheet.set_colorkey(BLACK)
fonts_rects = [pygame.Rect(453+i*9,443,8,8) for i in range(25)] + [pygame.Rect(453+i*9,452,8,8) for i in range(17)]
letteridx = ["0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","*","-","%",".","!","@"]
lives = 3
speed = 2
score = 0
stage = 1
Ups = 1
shots=[]
enemyShots=[]
playerHits=[]
rem=[]
hits=[]
active=[]

# enemy setup [posX, posY, HP, AI, angle]
zakoPos=[]
for i in range(20):
    zakoPos.append([120,0,1,0,0])
goeiPos=[]
for i in range(16):
    goeiPos.append([120,0,1,0,0])
bossPos=[]
for i in range(4):
    bossPos.append([120,0,2,0,0])
playerPos=[120,280]

# functions
def reset_enemies():
    global zakoPos, goeiPos, bossPos
    zakoPos = [[120, 0, 1, 0, 0] for _ in range(20)]
    goeiPos = [[120, 0, 1, 0, 0] for _ in range(16)]
    bossPos = [[120, 0, 2, 0, 0] for _ in range(4)]
def write(text, x, y, color):
    for i in range(len(text)):
        if text[i] in letteridx:
            idx = letteridx.index(text[i])
            rect = fonts_rects[idx]
            char_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            char_surface.blit(text_sheet, (0, 0), rect)
            arr = pygame.surfarray.pixels3d(char_surface)
            alpha = pygame.surfarray.pixels_alpha(char_surface)
            mask = alpha > 0
            arr[mask] = color
            del arr
            del alpha
            screen.blit(char_surface, (x + (i - len(text)/2) * 8, y - 4))

fid=open("storage.txt","w+")
highscore=fid.read()
if highscore=="":
    highscore=0
# game loop
running=True
tick=0
while running:
    tick+=1
    clock.tick(60)
    keys=pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type==pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if len(shots)<2:
                    shots.append(playerPos.copy())
            if event.key == pygame.K_ESCAPE:
                running = False
    if len(playerHits)==0:
        if keys[pygame.K_LEFT]:
            playerPos[0]-=speed
        if keys[pygame.K_RIGHT]:
            playerPos[0]+=speed
    else:
        if playerHits[0][3]<0 and playerHits[0][3]<=0:
            if keys[pygame.K_LEFT]:
                playerPos[0]-=speed
            if keys[pygame.K_RIGHT]:
                playerPos[0]+=speed
    clear=True
    living=[0,0,0]
    for i in range(len(zakoPos)):
        if zakoPos[i][2]>0:
            living[0]+=1
            clear=False
    for i in range(len(goeiPos)):
        if goeiPos[i][2]>0:
            living[1]+=1
            clear=False
    for i in range(len(bossPos)):
        if bossPos[i][2]>0:
            living[2]+=1
            clear=False
    if tick % 60 == 0 and clear:
        reset_enemies()
        stage+=1
        score += stage * 1000
    if lives == 0:
        break
    if score >= Ups * 20000:
        Ups += 1
        lives += 1
        if lives > 5:
            lives = 5
    screen.fill(BLACK)
    for i in range(lives-1):
        screen.blit(player,(2+18*i,302))
    if len(playerHits)==0:
        screen.blit(player,(playerPos[0]-8,playerPos[1]-8))
    else:
        if (playerHits[0][3]<0 and playerHits[0][3]%20>10):
            screen.blit(player,(playerPos[0]-8,playerPos[1]-8))
    rem=[]
    for i in range(len(shots)):
        shots[i][1]-=8
        if shots[i][1]<0:
            rem.append(i)
    rem.reverse()
    for i in rem:
        shots.pop(i)
    rem=[]
    for i in range(len(enemyShots)):
        enemyShots[i][1]+=4
        if enemyShots[i][1]>320:
            rem.append(i)
    rem.reverse()
    for i in rem:
        enemyShots.pop(i)
    for i in range(len(shots)):
        screen.blit(laser,(shots[i][0]-8,shots[i][1]-8))
    for i in range(len(enemyShots)):
        screen.blit(enemyShot,(enemyShots[i][0]-8,enemyShots[i][1]-8))
    for i in range(20):
        if zakoPos[i][2]>0:
            if zakoPos[i][3]==0:
                corPos=[i%10*18+39,m.floor(i/10)*18+88]
                deltPos=[corPos[0]-zakoPos[i][0],corPos[1]-zakoPos[i][1]]
                if m.sqrt(deltPos[0]**2+deltPos[1]**2)<4:
                    zakoPos[i][0]=corPos[0]
                    zakoPos[i][1]=corPos[1]
                else:
                    angle=m.atan2(deltPos[1],deltPos[0])
                    zakoPos[i][0]+=m.cos(angle)*4
                    zakoPos[i][1]+=m.sin(angle)*4
                if tick%4==0 and r.random()<0.01:
                    enemyShots.append([zakoPos[i][0],zakoPos[i][1]])
            if zakoPos[i][3]==1:
                for j in active:
                    if j[0]=="zako" and j[1]==i:
                        if zakoPos[i][4]==0:
                            if j[2]<zakoPos[i][0]:
                                zakoPos[i][4]+=15  # increase angle clockwise
                                zakoPos[i][0] += m.sin(m.radians(zakoPos[i][4])) * 2  # x increases right
                                zakoPos[i][1] += m.cos(m.radians(zakoPos[i][4])) * 2  # y increases down
                            elif j[2]>zakoPos[i][0]:
                                zakoPos[i][4]-=15
                                zakoPos[i][0]-=m.sin(m.radians(zakoPos[i][4]))*2
                                zakoPos[i][1]-=m.cos(m.radians(zakoPos[i][4]))*2
                        elif zakoPos[i][0]<j[2]:
                            zakoPos[i][4]+=15 # increase angle to the right
                            zakoPos[i][0]+=m.sin(m.radians(zakoPos[i][4]))*2
                            zakoPos[i][1]-=m.cos(m.radians(zakoPos[i][4]))*2
                        elif zakoPos[i][0]>j[2]:
                            zakoPos[i][4]-=15
                            zakoPos[i][0]-=m.sin(m.radians(zakoPos[i][4]))*2
                            zakoPos[i][1]-=m.cos(m.radians(zakoPos[i][4]))*2
            for j in range(len(shots)):
                if m.sqrt((shots[j][0]-zakoPos[i][0])**2+(shots[j][1]-zakoPos[i][1])**2)<8:
                    zakoPos[i][2]-=1
                    shots[j][1]=-10
                    if zakoPos[i][3]==0:
                        hits.append([zakoPos[i][0],zakoPos[i][1],50,60])
                        score+=50
                        zakoPos[i][2]-=1
                    else:
                        hits.append([zakoPos[i][0],zakoPos[i][1],100,60])
                        score+=100
                        zakoPos[i][2]-=1
            if zakoPos[i][2]>0:
                screen.blit(zako,(zakoPos[i][0]-8,zakoPos[i][1]-8))
    for i in range(16):
        if goeiPos[i][2]>0:
            if goeiPos[i][3]==0:
                corPos=[i%8*18+57,m.floor(i/8)*18+55]
                deltPos=[corPos[0]-goeiPos[i][0],corPos[1]-goeiPos[i][1]]
                if m.sqrt(deltPos[0]**2+deltPos[1]**2)<4:
                    goeiPos[i][0]=corPos[0]
                    goeiPos[i][1]=corPos[1]
                else:
                    angle=m.atan2(deltPos[1],deltPos[0])
                    goeiPos[i][0]+=m.cos(angle)*4
                    goeiPos[i][1]+=m.sin(angle)*4
                if tick%4==0 and r.random()<0.01:
                    enemyShots.append([goeiPos[i][0],goeiPos[i][1]])
            else:
                goeiPos[i][3]=0
                for j in active:
                    if j[0]=="goei" and j[1]==i:
                        active.pop(active.index(j))
            for j in range(len(shots)):
                if m.sqrt((shots[j][0]-goeiPos[i][0])**2+(shots[j][1]-goeiPos[i][1])**2)<8:
                    goeiPos[i][2]-=1
                    shots[j][1]=-10
                    if goeiPos[i][3]==0:
                        hits.append([goeiPos[i][0],goeiPos[i][1],80,60])
                        score+=80
                        goeiPos[i][2]-=1
                    else:
                        hits.append([goeiPos[i][0],goeiPos[i][1],160,60])
                        score+=160
                        goeiPos[i][2]-=1
            if goeiPos[i][2]>0:
                screen.blit(goei,(goeiPos[i][0]-8,goeiPos[i][1]-8))
    for i in range(4):
        if bossPos[i][2]>0:
            if bossPos[i][3]==0:
                corPos=[i*18+93,34]
                deltPos=[corPos[0]-bossPos[i][0],corPos[1]-bossPos[i][1]]
                if m.sqrt(deltPos[0]**2+deltPos[1]**2)<4:
                    bossPos[i][0]=corPos[0]
                    bossPos[i][1]=corPos[1]
                else:
                    angle=m.atan2(deltPos[1],deltPos[0])
                    bossPos[i][0]+=m.cos(angle)*4
                    bossPos[i][1]+=m.sin(angle)*4
            else:
                bossPos[i][3]=0
                active.pop(active.index(["boss", i, playerPos[0]]))
            for j in range(len(shots)):
                if m.sqrt((shots[j][0]-bossPos[i][0])**2+(shots[j][1]-bossPos[i][1])**2)<8:
                    bossPos[i][2]-=1
                    shots[j][1]=-10
                    if bossPos[i][2]==0:
                        if bossPos[i][3]==0:
                            hits.append([bossPos[i][0],bossPos[i][1],150,60])
                            score+=150
                        else:
                            hits.append([bossPos[i][0],bossPos[i][1],400,60])
                            score+=400
            if bossPos[i][2]==2:
                screen.blit(bossFull,(bossPos[i][0]-8,bossPos[i][1]-8))
            elif bossPos[i][2]==1:
                screen.blit(bossHalf,(bossPos[i][0]-8,bossPos[i][1]-8))
    rem=[]
    for i in range(len(hits)):
        if hits[i][3]<=0:
            rem.append(i)
    rem.reverse()
    for i in rem:
        hits.pop(i)
    for i in range(len(hits)):
        hits[i][3]-=1
        if hits[i][3]/60>.75:
            screen.blit(explosions[0], (hits[i][0]-16, hits[i][1]-16))
        elif hits[i][3]/60>.5:
            screen.blit(explosions[1], (hits[i][0]-16, hits[i][1]-16))
        elif hits[i][3]/60>.25:
            screen.blit(explosions[2], (hits[i][0]-16, hits[i][1]-16))
        elif hits[i][3]/60>0:
            screen.blit(explosions[3], (hits[i][0]-16, hits[i][1]-16))
    for i in range(len(enemyShots)):
        if m.sqrt((enemyShots[i][0]-playerPos[0])**2+(enemyShots[i][1]-playerPos[1])**2)<8 and len(playerHits)<1:
            lives-=1
            enemyShots[i][1]=-10
            playerHits.append([playerPos[0],playerPos[1],0,60])
    for i in range(len(playerHits)):
        if playerHits[i][3]<=-100:
            playerHits.pop(i)
    for i in range(len(playerHits)):
        playerHits[i][3]-=1
        if playerHits[i][3]/60>.75:
            screen.blit(playerExplosions[0], (playerHits[i][0]-16, playerHits[i][1]-16))
        elif playerHits[i][3]/60>.5:
            screen.blit(playerExplosions[1], (playerHits[i][0]-16, playerHits[i][1]-16))
        elif playerHits[i][3]/60>.25:
            screen.blit(playerExplosions[2], (playerHits[i][0]-16, playerHits[i][1]-16))
        elif playerHits[i][3]/60>0:
            screen.blit(playerExplosions[3], (playerHits[i][0]-16, playerHits[i][1]-16))
    scorestr = str(score)
    if len(active)<3 and tick % 30 == 0 and len(active)<living[0]+living[1]+living[2]:
        nextActive= r.randint(0, living[0] + living[1] + living[2] - 1)
        for i in range(len(zakoPos)):
            if zakoPos[i][2]>0:
                if nextActive==0:
                    active.append(["zako", i, playerPos[0]])
                    zakoPos[i][3]=1
                    break
                nextActive-=1
        for i in range(len(goeiPos)):
            if goeiPos[i][2]>0:
                if nextActive==0:
                    active.append(["goei", i, playerPos[0]])
                    goeiPos[i][3]=1
                    break
                nextActive-=1
        for i in range(len(bossPos)):
            if bossPos[i][2]>0:
                if nextActive==0:
                    active.append(["boss", i, playerPos[0]])
                    bossPos[i][3]=1
                    break
                nextActive-=1

    while len(scorestr) < 6:
        scorestr = "0" + scorestr
    write(f"{scorestr}", 24, 12, WHITE)
    write("1UP", 28, 4, RED)
    write("HIGH SCORE", 120, 4, RED)
    write(f"{highscore}", 120, 12, WHITE)
    pygame.display.flip()

if highscore == "" or score > int(highscore):
    highscore = score
    fid.seek(0)
    fid.write(str(highscore))
fid.close()

pygame.quit()
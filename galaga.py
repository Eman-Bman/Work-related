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
tractor_rects = [
    pygame.Rect(289, 36, 48, 80), # Frame 1
    pygame.Rect(339, 36, 48, 80), # Frame 2
    pygame.Rect(389, 36, 48, 80) # Frame 3
]
tractor = [pygame.Surface((rect.width, rect.height), pygame.SRCALPHA) for rect in tractor_rects]
for i, rect in enumerate(tractor_rects):
    tractor[i].blit(sprite_sheet, (0, 0), rect)

text_sheet = pygame.image.load("Text.png").convert_alpha()
text_sheet.set_colorkey(BLACK)
fonts_rects = [pygame.Rect(453+i*9,443,8,8) for i in range(25)] + [pygame.Rect(453+i*9,452,8,8) for i in range(17)]
letteridx = ["0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","*","-","%",".","!","@"]
lives = 3
speed = 2
score = 0
stage = 1
Ups = 1
turnAng = 5 
shots=[]
enemyShots=[]
playerHits=[]
rem=[]
hits=[]
active=[]
powerup=[]

# enemy setup [posX, posY, HP, AI, angle, targetX, extra]
zakoData=[]
for i in range(20):
    zakoData.append([120,0,1,0,0,0,0])
goeiData=[]
for i in range(16):
    goeiData.append([120,0,1,0,0,0,0])
bossData=[]
for i in range(4):
    bossData.append([120,0,2,0,0,0,0])
playerData=[120,280,0,0,0,0] # px, py, powerup1, powerup2, powerup3, powerup4]

# functions
def reset_enemies():
    global zakoData, goeiData, bossData
    zakoData = [[120, 0, 1, 0, 0,0,0] for _ in range(20)]
    goeiData = [[120, 0, 1, 0, 0,0,0] for _ in range(16)]
    bossData = [[120, 0, 2, 0, 0,0,0] for _ in range(4)]
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
                    shots.append(playerData.copy())
            if event.key == pygame.K_ESCAPE:
                running = False
    if len(playerHits)==0:
        if keys[pygame.K_LEFT]:
            playerData[0]-=speed
        if keys[pygame.K_RIGHT]:
            playerData[0]+=speed
        if playerData[0]<8:
            playerData[0]=8
        if playerData[0]>232:
            playerData[0]=232
    else:
        if playerHits[0][3]<0 and playerHits[0][3]<=0:
            if keys[pygame.K_LEFT]:
                playerData[0]-=speed
            if keys[pygame.K_RIGHT]:
                playerData[0]+=speed
    clear=True
    living=[0,0,0]
    for i in range(len(zakoData)):
        if zakoData[i][2]>0:
            living[0]+=1
            clear=False
    for i in range(len(goeiData)):
        if goeiData[i][2]>0 and goeiData[i][3]==0:
            living[1]+=1
            clear=False
    for i in range(len(bossData)):
        if bossData[i][2]>0 and bossData[i][3]==0:
            living[2]+=1
            clear=False
    if tick % 60 == 0 and clear:
        reset_enemies()
        stage+=1
        score += stage * 1000
    if lives == 0:
        break
    if score >= Ups * 50000 - 30000:
        Ups += 1
        lives += 1
        if lives > 5:
            lives = 5
    screen.fill(BLACK)
    for i in range(lives-1):
        screen.blit(player,(2+18*i,302))
    if len(playerHits)==0:
        screen.blit(player,(playerData[0]-8,playerData[1]-8))
    else:
        if (playerHits[0][3]<0 and playerHits[0][3]%20>10):
            screen.blit(player,(playerData[0]-8,playerData[1]-8))
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
        if zakoData[i][2]>0:
            if zakoData[i][3]!=1:
                corPos=[i%10*18+39,m.floor(i/10)*18+88]
                deltPos=[corPos[0]-zakoData[i][0],corPos[1]-zakoData[i][1]]
                if m.sqrt(deltPos[0]**2+deltPos[1]**2)<4:
                    if zakoData[i][3]==2:
                        zakoData[i][3]=0
                        active[:] = [a for a in active if not (a[0]=="zako" and a[1]==i)]
                    zakoData[i][0]=corPos[0]
                    zakoData[i][1]=corPos[1]
                else:
                    angle=m.atan2(deltPos[1],deltPos[0])
                    zakoData[i][0]+=m.cos(angle)*4
                    zakoData[i][1]+=m.sin(angle)*4
                if tick%4==0 and r.random()<0.005:
                    enemyShots.append([zakoData[i][0],zakoData[i][1]])
            if zakoData[i][3]==1:
                if tick%4==0 and r.random()<0.015:
                    enemyShots.append([zakoData[i][0],zakoData[i][1]])
                if abs(zakoData[i][4])>=215 and abs(zakoData[i][4])<=500:
                    if abs(zakoData[i][0]-zakoData[i][5])<4:
                        zakoData[i][4]=540
                    else:
                        zakoData[i][0]+=m.sin(m.radians(zakoData[i][4]))*2
                        zakoData[i][1]-=m.cos(m.radians(zakoData[i][4]))*2
                        if zakoData[i][1]>320:
                            zakoData[i][3]=2
                            zakoData[i][4]=0
                            zakoData[i][5]=0
                elif zakoData[i][4]==540:
                    if zakoData[i][1]>320:
                        zakoData[i][3]=2
                        zakoData[i][4]=0
                        zakoData[i][5]=0
                    else:
                        zakoData[i][1]+=4
                elif zakoData[i][4]==0:
                    if zakoData[i][5]<zakoData[i][0]:
                        zakoData[i][4]+=turnAng*2  # increase angle clockwise
                        zakoData[i][0] += m.sin(m.radians(zakoData[i][4])) * 2  # x increases right
                        zakoData[i][1] += m.cos(m.radians(zakoData[i][4])) * 2  # y increases down
                    elif zakoData[i][5]>zakoData[i][0]:
                        zakoData[i][4]-=turnAng*2
                        zakoData[i][0]-=m.sin(m.radians(zakoData[i][4]))*2
                        zakoData[i][1]-=m.cos(m.radians(zakoData[i][4]))*2
                elif 0<zakoData[i][4]:
                    zakoData[i][4]+=turnAng
                    zakoData[i][0]+=m.sin(m.radians(zakoData[i][4]))*2
                    zakoData[i][1]-=m.cos(m.radians(zakoData[i][4]))*2
                elif 0>zakoData[i][4]:
                    zakoData[i][4]-=turnAng
                    zakoData[i][0]-=m.sin(m.radians(zakoData[i][4]))*2
                    zakoData[i][1]-=m.cos(m.radians(zakoData[i][4]))*2
            for j in range(len(shots)):
                if m.sqrt((shots[j][0]-zakoData[i][0])**2+(shots[j][1]-zakoData[i][1])**2)<8:
                    zakoData[i][2]-=1
                    shots[j][1]=-10
                    if zakoData[i][3]==0:
                        hits.append([zakoData[i][0],zakoData[i][1],50,60])
                        score+=50
                        zakoData[i][2]-=1
                    else:
                        hits.append([zakoData[i][0],zakoData[i][1],100,60])
                        score+=100
                        zakoData[i][2]-=1
                    active[:] = [a for a in active if not (a[0]=="zako" and a[1]==i)]
            if zakoData[i][2]>0:
                screen.blit(zako,(zakoData[i][0]-8,zakoData[i][1]-8))
    for i in range(16):
        if goeiData[i][2]>0:
            if goeiData[i][3]==0:
                corPos=[i%8*18+57,m.floor(i/8)*18+55]
                deltPos=[corPos[0]-goeiData[i][0],corPos[1]-goeiData[i][1]]
                if m.sqrt(deltPos[0]**2+deltPos[1]**2)<4:
                    goeiData[i][0]=corPos[0]
                    goeiData[i][1]=corPos[1]
                else:
                    angle=m.atan2(deltPos[1],deltPos[0])
                    goeiData[i][0]+=m.cos(angle)*4
                    goeiData[i][1]+=m.sin(angle)*4
                if tick%4==0 and r.random()<0.005:
                    enemyShots.append([goeiData[i][0],goeiData[i][1]])
            if goeiData[i][3]==1:
                if tick%4==0 and r.random()<0.015:
                    enemyShots.append([goeiData[i][0],goeiData[i][1]])
                if abs(goeiData[i][4])>=215 and abs(goeiData[i][4])<=500:
                    if abs(goeiData[i][0]-goeiData[i][5])<4:
                        goeiData[i][4]=540
                    else:
                        goeiData[i][0]+=m.sin(m.radians(goeiData[i][4]))*2
                        goeiData[i][1]-=m.cos(m.radians(goeiData[i][4]))*2
                        if goeiData[i][6]==0 and r.random()<0.1:
                            goeiData[i][6]=r.randint(-5,5)
                        if goeiData[i][6]<0:
                            goeiData[i][6]+=1
                        elif goeiData[i][6]>0:
                            goeiData[i][6]-=1
                        goeiData[i][0]+=goeiData[i][6]
                        if goeiData[i][1]>320:
                            goeiData[i][1]=0
                            goeiData[i][3]=0
                            goeiData[i][4]=0
                            goeiData[i][5]=0
                            goeiData[i][6]=0
                            active[:] = [a for a in active if not (a[0]=="goei" and a[1]==i)]
                elif goeiData[i][4]==540:
                    if goeiData[i][1]>320:
                        goeiData[i][1]=0
                        goeiData[i][3]=0
                        goeiData[i][4]=0
                        goeiData[i][5]=0
                        goeiData[i][6]=0
                        active[:] = [a for a in active if not (a[0]=="goei" and a[1]==i)]
                    else:
                        goeiData[i][1]+=4
                elif goeiData[i][4]==0:
                    if goeiData[i][5]<goeiData[i][0]:
                        goeiData[i][4]+=turnAng*2  # increase angle clockwise
                        goeiData[i][0] += m.sin(m.radians(goeiData[i][4])) * 2  # x increases right
                        goeiData[i][1] += m.cos(m.radians(goeiData[i][4])) * 2  # y increases down
                    elif goeiData[i][5]>goeiData[i][0]:
                        goeiData[i][4]-=turnAng*2
                        goeiData[i][0]-=m.sin(m.radians(goeiData[i][4]))*2
                        goeiData[i][1]-=m.cos(m.radians(goeiData[i][4]))*2
                elif 0<goeiData[i][4]:
                    goeiData[i][4]+=turnAng
                    goeiData[i][0]+=m.sin(m.radians(goeiData[i][4]))*2
                    goeiData[i][1]-=m.cos(m.radians(goeiData[i][4]))*2
                elif 0>goeiData[i][4]:
                    goeiData[i][4]-=turnAng
                    goeiData[i][0]-=m.sin(m.radians(goeiData[i][4]))*2
                    goeiData[i][1]-=m.cos(m.radians(goeiData[i][4]))*2
            for j in range(len(shots)):
                if m.sqrt((shots[j][0]-goeiData[i][0])**2+(shots[j][1]-goeiData[i][1])**2)<8:
                    goeiData[i][2]-=1
                    shots[j][1]=-10
                    if goeiData[i][3]==0:
                        hits.append([goeiData[i][0],goeiData[i][1],80,60])
                        score+=80
                        goeiData[i][2]-=1
                    else:
                        hits.append([goeiData[i][0],goeiData[i][1],160,60])
                        score+=160
                        goeiData[i][2]-=1
                    active[:] = [a for a in active if not (a[0]=="goei" and a[1]==i)]
            if goeiData[i][2]>0:
                screen.blit(goei,(goeiData[i][0]-8,goeiData[i][1]-8))
    for i in range(4):
        if bossData[i][2]!=0:
            if bossData[i][3]==0 or bossData[i][3]==3:
                corPos=[i*18+93,34]
                deltPos=[corPos[0]-bossData[i][0],corPos[1]-bossData[i][1]]
                if m.sqrt(deltPos[0]**2+deltPos[1]**2)<4:
                    bossData[i][0]=corPos[0]
                    bossData[i][1]=corPos[1]
                    if bossData[i][3]==3:
                        bossData[i][3]=0
                        bossData[i][4]=0
                        bossData[i][5]=0
                        bossData[i][6]=0
                        active[:] = [a for a in active if not (a[0]=="boss" and a[1]==i)]
                else:
                    angle=m.atan2(deltPos[1],deltPos[0])
                    bossData[i][0]+=m.cos(angle)*4
                    bossData[i][1]+=m.sin(angle)*4
            elif bossData[i][3]==1:
                if bossData[i][1]>196:
                    if bossData[i][0]<bossData[i][5]:
                        bossData[i][4]=810
                    else:
                        bossData[i][4]=630
                if abs(bossData[i][4])>=215 and abs(bossData[i][4])<=500:
                    if abs(bossData[i][0]-bossData[i][5])<4:
                        bossData[i][4]=540
                    else:
                        bossData[i][0]+=m.sin(m.radians(bossData[i][4]))*2
                        bossData[i][1]-=m.cos(m.radians(bossData[i][4]))*2
                elif bossData[i][4]==810 or bossData[i][4]==630:
                        bossData[i][0]+=m.sin(m.radians(bossData[i][4]))*2
                        bossData[i][1]-=m.cos(m.radians(bossData[i][4]))*2
                        if bossData[i][0]-bossData[i][5]<4 and bossData[i][1]>196:
                            bossData[i][3]=2
                            bossData[i][4]=0
                            bossData[i][5]=0
                            bossData[i][6]=120
                elif bossData[i][4]==540:
                    if bossData[i][1]>320:
                        bossData[i][3]=2
                        bossData[i][4]=0
                        bossData[i][5]=0
                        active[:] = [a for a in active if not (a[0]=="boss" and a[1]==i)]
                    else:
                        bossData[i][1]+=4
                elif bossData[i][4]==0:
                    if bossData[i][5]<bossData[i][0]:
                        bossData[i][4]+=turnAng*2  # increase angle clockwise
                        bossData[i][0] += m.sin(m.radians(bossData[i][4])) * 2  # x increases right
                        bossData[i][1] += m.cos(m.radians(bossData[i][4])) * 2  # y increases down
                    elif bossData[i][5]>bossData[i][0]:
                        bossData[i][4]-=turnAng*2
                        bossData[i][0]-=m.sin(m.radians(bossData[i][4]))*2
                        bossData[i][1]-=m.cos(m.radians(bossData[i][4]))*2
                elif 0<bossData[i][4]:
                    bossData[i][4]+=turnAng
                    bossData[i][0]+=m.sin(m.radians(bossData[i][4]))*2
                    bossData[i][1]-=m.cos(m.radians(bossData[i][4]))*2
                elif 0>bossData[i][4]:
                    bossData[i][4]-=turnAng
                    bossData[i][0]-=m.sin(m.radians(bossData[i][4]))*2
                    bossData[i][1]-=m.cos(m.radians(bossData[i][4]))*2
            elif bossData[i][3]==2:
                if bossData[i][6]>0:
                    bossData[i][6]-=1
                if bossData[i][6]==0:
                    bossData[i][3]=3
                    active[:] = [a for a in active if not (a[0]=="boss" and a[1]==i)]
            for j in range(len(shots)):
                if m.sqrt((shots[j][0]-bossData[i][0])**2+(shots[j][1]-bossData[i][1])**2)<8:
                    bossData[i][2]-=1
                    shots[j][1]=-10
                    if bossData[i][2]==0:
                        if bossData[i][3]==0:
                            hits.append([bossData[i][0],bossData[i][1],150,60])
                            score+=150
                        else:
                            hits.append([bossData[i][0],bossData[i][1],400,60])
                            score+=400
                        active[:] = [a for a in active if not (a[0]=="boss" and a[1]==i)]
            if bossData[i][2]==2:
                screen.blit(bossFull,(bossData[i][0]-8,bossData[i][1]-8))
            elif bossData[i][2]==1:
                screen.blit(bossHalf,(bossData[i][0]-8,bossData[i][1]-8))
            if bossData[i][3]==2:
                if bossData[i][6]>0:
                    screen.blit(tractor[m.floor(bossData[i][6]/5)%3], (bossData[i][0]-24, bossData[i][1]+8))
    #check for collisions
    for i in range(len(zakoData)):
        if m.sqrt((zakoData[i][0]-playerData[0])**2+(zakoData[i][1]-playerData[1])**2)<8 and len(playerHits)<1 and zakoData[i][2]>0:
            lives-=1
            zakoData[i][2]=0
            playerHits.append([playerData[0],playerData[1],0,60])
    for i in range(len(goeiData)):
        if m.sqrt((goeiData[i][0]-playerData[0])**2+(goeiData[i][1]-playerData[1])**2)<8 and len(playerHits)<1 and goeiData[i][2]>0:
            lives-=1
            goeiData[i][2]=0
            playerHits.append([playerData[0],playerData[1],0,60])
    for i in range(len(bossData)):
        if bossData[i][1]>196 and bossData[i][2]>0:
            if m.sqrt((bossData[i][0]-playerData[0])**2)<8 and len(playerHits)<1:
                lives-=1
                playerHits.append([playerData[0],playerData[1],0,60])

    rem=[]
    for i in range(len(hits)):
        if hits[i][3]<=0:
            rem.append(i)
    rem.reverse()
    for i in rem:
        hits.pop(i)
    for i in range(len(hits)):
        if hits[i][3]==90 and r.random()<1:
            powerup.append([hits[i][0], hits[i][1], r.randint(1, 4)])
        hits[i][3]-=1
        if hits[i][3]/60>.75:
            screen.blit(explosions[0], (hits[i][0]-16, hits[i][1]-16))
        elif hits[i][3]/60>.5:
            screen.blit(explosions[1], (hits[i][0]-16, hits[i][1]-16))
        elif hits[i][3]/60>.25:
            screen.blit(explosions[2], (hits[i][0]-16, hits[i][1]-16))
        elif hits[i][3]/60>0:
            screen.blit(explosions[3], (hits[i][0]-16, hits[i][1]-16))
    rem=[]
    for i in range(len(powerup)):
        if powerup[i][1]>320:
            rem.append(i)
    for i in range(len(powerup)):
        if m.sqrt((powerup[i][0]-playerData[0])**2+(powerup[i][1]-playerData[1])**2)<8 and len(playerHits)<1:
            if powerup[i][2]==1:
                playerData[2]+=1
            elif powerup[i][2]==2:
                playerData[3]+=1
            elif powerup[i][2]==3:
                playerData[4]+=1
            elif powerup[i][2]==4:
                playerData[5]+=1
            rem.append(i)
        else:
            powerup[i][1]+=4
            screen.blit(laser,(powerup[i][0]-8,powerup[i][1]-8))
    rem.reverse()
    for i in rem:
        powerup.pop(i)
    for i in range(len(enemyShots)):
        if m.sqrt((enemyShots[i][0]-playerData[0])**2+(enemyShots[i][1]-playerData[1])**2)<8 and len(playerHits)<1:
            lives-=1
            enemyShots[i][1]=-10
            playerHits.append([playerData[0],playerData[1],0,60])
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
        for i in range(len(bossData)):
            if bossData[i][2]>0:
                if nextActive==0:
                    active.append(["boss", i])
                    bossData[i][3]=1
                    bossData[i][5]=playerData[0]
                    break
                nextActive-=1
        for i in range(len(zakoData)):
            if zakoData[i][2]>0:
                if nextActive==0:
                    active.append(["zako", i])
                    zakoData[i][3]=1
                    zakoData[i][5]=playerData[0]
                    break
                nextActive-=1
        for i in range(len(goeiData)):
            if goeiData[i][2]>0:
                if nextActive==0:
                    active.append(["goei", i])
                    goeiData[i][3]=1
                    goeiData[i][5]=playerData[0]
                    break
                nextActive-=1
    if len(active)>3:
        active.pop(3)

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

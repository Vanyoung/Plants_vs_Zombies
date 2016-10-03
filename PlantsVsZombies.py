# coding:utf-8
#
#file PlantsVsZombies.py

import pygame, random, sys, time
from pygame.locals import *

UI_Width = 800                                     #游戏窗口高度
UI_Height = 600                                     #游戏窗口宽度
FPS = 60                                            #帧数

MAX_Into = 10                                       #最大僵尸通过数
Zombie_Width = 50                                   #僵尸宽度
Zombie_Height = 90                                  #僵尸高度

Zombie_Total = 50                                   #僵尸总数

Zombie_Add_Rate = 50                                #僵尸增加频率,循环50次增加1个

Zombie1_Speed = 2                                   #僵尸1移动速度
Zombie2_Speed = Zombie1_Speed / 2                   #僵尸2移动速度

Emitter_Move_Dist = 10                              #发射器每次移动距离
Bullet_Speed = 10                                   #子弹速度
Bullet_Add_Rate = 15                                #子弹列表中添加子弹的频率

Zombies1_List = []                                  #保存僵尸1的列表
Zombies2_List = []                                  #保存僵尸2的列表
Bullets_List = []                                   #子弹列表

Into_Base_Zombies = 0                               #通过的僵尸数量
Score = 0                                           #积分

Add_Zombie_Total = 0                                #添加的僵尸总数

Zombie1_Rate_Counter = 0                            #僵尸1的频率计数器
Zombie2_Rate_Counter = 0                            #僵尸2的频率计数器
Bullet_Rate_Counter = 40                            #子弹频率计数器

TEXTCOLOR = (255,255,255)                           #文本颜色

#上下左右移动标志
To_Left = False
To_Right = False
To_Up = False
To_Down = False

#射击标志
Shoot = False

pygame.init()                                                   #初始化pygame
mainClock = pygame.time.Clock()
GameWin = pygame.display.set_mode((UI_Width, UI_Height))        #设置场地大小
pygame.display.set_caption('佟大为大战比利王')                  #设置窗口标题
pygame.mouse.set_visible(True)                                  #显示鼠标指针
font = pygame.font.SysFont("simsunnsimsun",32)                  #设置字体

#gameOverSound = pygame.mixer.Sound('gameover.wav')              #游戏结束声音
gameStartSound = pygame.mixer.Sound('gamestart.wav')
gameWinSound = pygame.mixer.Sound('winmusic.wav')               #游戏胜利声音
gameLoseSound = pygame.mixer.Sound('losemusic.wav')             #游戏失败声音
gameHitEmiSound = pygame.mixer.Sound('hitemi.wav')              #僵尸击中发射器声音
gameHitZombie1Sound = pygame.mixer.Sound('hitzom1.wav')         #子弹击中僵尸1声音
gameHitZombie2Sound = pygame.mixer.Sound('hitzom2.wav')
pygame.mixer.music.load('background.wav')                       #背景音乐

EmitterImage = pygame.image.load('Emitter.gif')                #设置发射器图片
EmitterRect = EmitterImage.get_rect()

BulletImage = pygame.image.load('Bullet.gif')                   #设置子弹图片
BulletRect = BulletImage.get_rect()

Zombie1Image = pygame.image.load('Zombie1.png')                 #僵尸1图片
Zombie2Image = pygame.image.load('Zombie2.png')                 #僵尸2图片
BackgroundImage = pygame.image.load('background.png')           #背景图片

#将背景图缩放到游戏窗口大小
rescaledBackground = pygame.transform.scale(BackgroundImage, (UI_Width, UI_Height))

GameWin.blit(rescaledBackground, (0, 0))                        #将背景画到游戏窗口
GameWin.blit(EmitterImage, (UI_Width / 2, UI_Height - 120))      #把游戏者的子弹发射器画到屏幕对应位置

#显示字符串
def DisplayStr(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect = topleft = (x, y)
    surface.blit(textobj, textrect)

DisplayStr('Enter to start', font, GameWin, UI_Width / 2 - 95, 300)

#初始化游戏
def init():
    global Zombies1_List, Zombies2_List, Bullets_List, Into_Base_Zombies,Score, Add_Zombie_Total
    global To_Left, To_Right, To_Up, To_Down, Shoot
    Zombies1_List = []                                          #保存僵尸1的列表
    Zombies2_List = []                                          #保存僵尸2的列表
    Bullets_List = []                                           #子弹列表
    Into_Base_Zombies = 0                                       #进入基地的僵尸数量
    Score = 0                                                   
    Add_Zombie_Total = 0                                        #添加的僵尸数量
    To_Left = To_Right = To_Up = To_Down = Shoot = False        #清空操作状态

#退出游戏
def quit():
    pygame.quit()
    sys.exit()

#开始界面时等待游戏者按键
def waitPressKey():
    global Zombie1_List, Zombie2_List, Bullets_List, Into_Base_Zombies, Score, Add_Zombie_Total
    while  True:                                                #死循环
        for event in pygame.event.get():                        #获取事件
            if event.type == QUIT:                              #退出事件
                quit()                                          #退出游戏
            if event.type == KEYDOWN:                           #按键事件
                if event.key == K_ESCAPE:                       #ESC
                    quit()
                if event.key == K_RETURN:                       #回车
                    init()
                    return                                      #退出死循环

#处理各类事件
def ProcEvent():
    global To_Up, To_Down, Shoot

    for event in pygame.event.get():
        if event.type == QUIT:
            quit()

        if event.type == KEYDOWN:
            if event.key == K_UP or event.key == ord('w'):      #按下W
                To_Down = False
                To_Up = True
            if event.key == K_DOWN or event.key == ord('s'):    #按下S
                To_Up = False
                To_Down = True
            if event.key == K_SPACE:                            #按下空格
                Shoot = True
        if event.type == KEYUP:                                 #键盘放开事件
            if event.key == K_ESCAPE:                           #松开ESC
                quit()
            if event.key == K_UP or event.key == ord('w'):
                To_Up == False
            if event.key == K_DOWN or event.key == ord('s'):
                To_Down == False
            if event.key == K_SPACE:
                Shoot = False
        if event.type == MOUSEBUTTONDOWN:                      #鼠标按下    
            Shoot = True
        if event.type == MOUSEBUTTONUP:                         #鼠标松开
            Shoot = False

#向游戏中增加角色
def AddRoles():
    #增加僵尸
    global Add_Zombie_Total, Zombie1_Rate_Counter, Zombie1_Rate_Counter
    global Zombie2_Rate_Counter, Bullet_Rate_Counter, Bullet_Rate_Counter
    if Add_Zombie_Total < Zombie_Total:                         #如果僵尸数量少于总数
        #增加僵尸1
        Zombie1_Rate_Counter += 1
        if Zombie1_Rate_Counter == Zombie_Add_Rate:              #计满数,增加僵尸
            Zombie1_Rate_Counter = 0
            ZombieSize_X = Zombie_Width
            ZombieSize_Y = Zombie_Height
            newZombie1 = {'rect':pygame.Rect(UI_Width,random.randint(10,UI_Height-ZombieSize_Y-10),ZombieSize_X,ZombieSize_Y),'surface':pygame.transform.scale(Zombie1Image,(ZombieSize_X,ZombieSize_Y)),}
            Zombies1_List.append(newZombie1)                     #添加到僵尸1列表
            Add_Zombie_Total += 1
        #增加僵尸2
        Zombie2_Rate_Counter += 1
        if Zombie2_Rate_Counter == Zombie_Add_Rate:              #计满数,增加僵尸
            Zombie2_Rate_Counter = 0
            ZombieSize_X = Zombie_Width
            ZombieSize_Y = Zombie_Height
            newZombie2 = {'rect':pygame.Rect(UI_Width,random.randint(10,UI_Height-ZombieSize_Y-10),ZombieSize_X,ZombieSize_Y),'surface':pygame.transform.scale(Zombie2Image,(ZombieSize_X,ZombieSize_Y)),}
            Zombies2_List.append(newZombie2)                     #添加到僵尸2列表
            Add_Zombie_Total += 1

    #增加子弹
    Bullet_Rate_Counter += 1
    if Bullet_Rate_Counter >= Bullet_Add_Rate and Shoot == True:
        Bullet_Rate_Counter = 0
        newBullet = {'rect':pygame.Rect(EmitterRect.centerx+10,EmitterRect.centery-25,BulletRect.width,BulletRect.height),'surface':pygame.transform.scale(BulletImage,(BulletRect.width,BulletRect.height)),}
        Bullets_List.append(newBullet)

#判断僵尸是否击中发射器
def EmitterWasHit(EmitterRect, z):
    for z in Zombies1_List:
        if EmitterRect.colliderect(z['rect']):
            gameHitEmiSound.play()
            return True
    for z in Zombies2_List:
        if EmitterRect.colliderect(z['rect']):
            gameHitEmiSound.play()
            return True
    return False
#判断僵尸1是否被击中
def Zombie1WasHit(BulletRect, z):
    for b in Bullets_List:
        if b['rect'].colliderect(z['rect']):
            Bullets_List.remove(b)                              #删除子弹
            gameHitZombie1Sound.play()
            return True
    return False
#判断僵尸2是否被击中
def Zombie2WasHit(BulletRect, c):
    for b in Bullets_List:
        if b['rect'].colliderect(c['rect']):
            Bullets_List.remove(b)                              #删除子弹
            gameHitZombie2Sound.play()
            return True
    return False

#更新角色状态
def RolesStatus():
    global Score, Into_Base_Zombies
    #移动发射器
    if To_Up and EmitterRect.top > 30:                          #向上且有向上的空间
        EmitterRect.move_ip(0,-1 * Emitter_Move_Dist)
    if To_Down and EmitterRect.bottom < UI_Height - 10:         #向下移动
    #移动僵尸1(列表中每个僵尸移动一次)
        EmitterRect.move_ip(0,Emitter_Move_Dist)

    for z in Zombies1_List:
        z['rect'].move_ip(-1*Zombie1_Speed, 0)
    #移动僵尸2
    for c in Zombies2_List:
        c['rect'].move_ip(-1*Zombie2_Speed, 0)

    #移动子弹
    for b in Bullets_List:
        b['rect'].move_ip(1*Bullet_Speed, 0)

    #删除已移到左边的僵尸1
    for z in Zombies1_List[:]:
        if z['rect'].left < 0:
            Zombies1_List.remove(z)                              #从列表中删除
            Into_Base_Zombies += 1
    #删除已移到左边的僵尸2
    for c in Zombies2_List[:]:
        if c['rect'].left < 0:
            Zombies2_List.remove(c)                              #从列表中删除
            Into_Base_Zombies += 1

    #删除已到右边界的子弹
    for b in Bullets_List[:]:
        if b['rect'].right > UI_Width:
            Bullets_List.remove(b)

    #检查子弹是否击中了僵尸1
    for z in Zombies1_List:
        if Zombie1WasHit(Bullets_List, z):
            Score += 1
            Zombies1_List.remove(z)
    #检查子弹是否击中了僵尸2
    for c in Zombies2_List:
        if Zombie2WasHit(Bullets_List, c):
            Score += 1
            Zombies2_List.remove(c)

#重新绘制
def ReDraw():
    GameWin.blit(rescaledBackground, (0, 0))
    #绘制发射器
    GameWin.blit(EmitterImage, EmitterRect)
    #绘制僵尸
    for z in Zombies1_List: 
        GameWin.blit(z['surface'], z['rect'])
    for c in Zombies2_List:
        GameWin.blit(c['surface'], c['rect'])
    #绘制子弹
    for b in Bullets_List:
        GameWin.blit(b['surface'], b['rect'])
    #显示得分和通过僵尸数量
    DisplayStr('Pass: %s' % (Into_Base_Zombies), font, GameWin, 10, 20)
    DisplayStr('death: %s' % (Score), font, GameWin, 10, 50)
    pygame.display.update()                                     #刷新画面


#检查胜负
def CheckWinOrLose():
    pygame.mixer.music.stop()                                   #停止音乐
#    gameOverSound.play()                                        #播放游戏结束音乐
#    time.sleep(4)                                               #延时/s
#    gameOverSound.stop()
    GameWin.blit(rescaledBackground, (0, 0))                    #绘制背景
    GameWin.blit(EmitterImage, (UI_Width / 2, UI_Height- 120))
    DisplayStr('Pass', font, GameWin, 10, 30)
    DisplayStr('Game Over', font, GameWin, UI_Width/2-75, UI_Height/3)
    DisplayStr('Enter to replay', font, GameWin, UI_Width/2-120, UI_Height/3+150)
    if Into_Base_Zombies >= MAX_Into:
        DisplayStr('LOSE', font, GameWin, UI_Width/2-40, UI_Height/3+100)
        gameLoseSound.play()
    if EmitterWasHit(EmitterRect, Zombies1_List):
        DisplayStr('LOSE', font, GameWin, UI_Width/2-40, UI_Height/3+100)
        gameLoseSound.play()
    if Score + Into_Base_Zombies >= Zombie_Total:
        DisplayStr('WIN', font, GameWin, UI_Width/2-30, UI_Height/3+100)
        gameWinSound.play()


while True:
    EmitterRect.topleft = (30, UI_Height / 2)                   #发射器置于左侧30, 垂直居中
    pygame.mixer.music.play(-1)                                 #循环播放音乐
    gameStartSound.play()
    while True:
        ProcEvent()                                             #处理事件
        AddRoles()                                              #添加角色到游戏
        RolesStatus()                                           #更新角色状态(移动,删除,检查边界)   
        ReDraw()                                                #重新绘制

        #检查僵尸是否击中发射器，若击中,则游戏结束
        if EmitterWasHit(EmitterRect, Zombies1_List):
            break
        if EmitterWasHit(EmitterRect, Zombies2_List):
            break

        #检查通过僵尸数量是否达到最大值,若是,则游戏结束
        if Into_Base_Zombies >= MAX_Into:
            break
        if Score +Into_Base_Zombies >= Zombie_Total:
            break

        mainClock.tick(FPS)                                     #设置最大帧率
    #跳出循环,则停止游戏
    CheckWinOrLose()                                            #检查胜负
    pygame.display.update()                                     #刷新屏幕
    waitPressKey()                                              #等待按键
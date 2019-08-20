import pygame
from pygame.locals import *
import os
from properties import *
from Bg_Sprite import *
import proper
import random


class Fight_Window(object):
    ''' 战斗窗口 '''
    def __init__(self):
        pygame.init()
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 0)
        self.screen = pygame.display.set_mode(BG_SIZE, RESIZABLE, 32)
        self.clock = pygame.time.Clock()
        # 判断是否退出循环
        self.is_exit = True
        # 判断切换图片
        self.flag = 2
        # 用于延迟
        self.delay = 100
        self.Sprite_Group()

    def Sprite_Group(self):
        ''' 精灵组 '''
        # 背景精灵
        self.bg = Bg_Sprite("img/bg.png")
        self.bg_group = pygame.sprite.Group(self.bg)
        # 人物精灵
        self.role = Role_Sprite()
        self.role_group = pygame.sprite.Group(self.role)
        # 英雄精灵
        self.hero = Hero_Sprite()
        self.hero_group = pygame.sprite.Group(self.hero)
        # NPC精灵
        self.npc = NPC_Sprite()
        self.npc_group = pygame.sprite.Group(self.npc)

    def change_direction(self,dire,key, SPEED):
        ''' 监听方向 '''
        eval("self.hero.Move_"+dire+"("+str(SPEED)+")")
        self.hero.key = key  # 人物方向
        self.hero.flag = self.flag  # 人物切换图片


    def control_keyboard(self):
        ''' 监听事件 '''
        if proper.blood == 0 or proper.npc_blood == 0:
            self.is_exit = False


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    self.is_exit = False

                if event.key == K_q:
                    # 飞镖
                    if proper.is_q:
                        proper.key = self.hero.key
                        self.hero.Create_Skill()
                        if proper.w_skill:
                            self.hero.Create_Shadow_Skill(proper.w_skill.rect)
                        proper.is_q = False

                if event.key == K_w:
                    # 影子
                    if proper.is_w:
                        proper.w_key = self.hero.key
                        proper.w_skill = self.hero.Create_Skill_W()
                        proper.is_w = False
                        proper.is_w_false = False
                    elif not proper.is_w_true and not proper.is_w_false:
                        self.hero.rect.topleft, proper.w_skill.rect.topleft = proper.w_skill.rect.topleft, self.hero.rect.topleft
                        proper.is_w_false = True

                # if event.key == K_e:
                #     # 飞镖
                #     if proper.is_e:
                #         proper.key = self.hero.key
                #         self.hero.Create_Skill_E()
                #         proper.is_e = False

            # 切换图片
            if event.type == pygame.KEYUP:
                # 松开按键时停下
                if self.role.key == "U":
                    self.role.flag = 3
                    self.npc.flag = 3
                elif self.role.key == "D":
                    self.role.flag = 3
                    self.npc.flag = 3
                elif self.role.key == "L":
                    self.role.flag = 3
                    self.npc.flag = 3
                elif self.role.key == "R":
                    self.role.flag = 3
                    self.npc.flag = 3
        if not (self.delay % 5):
            self.flag -= 1
        if self.flag == 0:
            self.flag = 2

        # 延迟
        self.delay -= 1
        if not self.delay:
            self.delay = 100

        # 控制按键
        if pygame.key.get_pressed()[pygame.K_UP]:
            self.change_direction("Up", "U", -SPEED)
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            self.change_direction("Down", "D", SPEED)
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            self.change_direction("Left", "L", -SPEED)
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.change_direction("Right", "R", SPEED)
        if pygame.key.get_pressed()[pygame.K_UP] and pygame.key.get_pressed()[pygame.K_LEFT]:
            self.change_direction("Empty", "UL", SPEED)
        if pygame.key.get_pressed()[pygame.K_UP] and pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.change_direction("Empty", "UR", SPEED)
        if pygame.key.get_pressed()[pygame.K_DOWN] and pygame.key.get_pressed()[pygame.K_LEFT]:
            self.change_direction("Empty", "DL", SPEED)
        if pygame.key.get_pressed()[pygame.K_DOWN] and pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.change_direction("Empty", "DR", SPEED)

    def change_direction_npc(self,dire,key, SPEED):
        ''' 监听npc方向 '''
        eval("self.npc.Move_" + dire + "(" + str(SPEED) + ")")
        self.npc.key = key  # npc方向
        self.npc.flag = self.flag  # 人物切换图片

    def random_npc(self):
        '''npc随机定时'''
        for i in range(60):
            if i % 10 == 0:
                proper.times += 1
        if proper.times >= 90:
            proper.n = random.randint(0, 7)
            proper.times = 0

    def collide_group(self, sp1, sp2, role):
        ''' 主角与物品组检测碰撞，如果碰撞就动不了'''
        self.contact = pygame.sprite.groupcollide(sp1, sp2, False, False)
        if role == "hero":
            if self.contact and proper.skill_and_role:
                proper.blood -= 10
                proper.skill_and_role = False

        if role == "npc":
            for key,value in self.contact.items():
                for skill in value:
                    if self.contact and skill.skill_and_npc:
                        if skill.flag == "q":
                            proper.npc_blood -= 10
                        elif skill.flag == "wq":
                            proper.npc_blood -= 10
                        skill.skill_and_npc = False


    def blood(self, role, blood, power):
        '''血条'''
        pygame.draw.rect(self.screen, (220, 220, 220),pygame.Rect(role.rect.x - 10, role.rect.top - 15, 50, 5))
        if blood > 0:
            pygame.draw.rect(self.screen, (255, 0, 0),pygame.Rect(role.rect.x - 10, role.rect.top - 15, blood, 5), 0)
        pygame.draw.rect(self.screen, (112, 128, 144),pygame.Rect(role.rect.x - 10, role.rect.top - 10, 50, 5))
        if power > 0:
            pygame.draw.rect(self.screen, (0, 0, 255),pygame.Rect(role.rect.x - 10, role.rect.top - 10, power, 5), 0)


    def Sprite_Group_Draw(self):
        ''' 显示精灵 '''
        self.collide_group(self.hero_group, self.npc.skill_group, "hero")
        self.collide_group(self.npc_group, self.hero.skill_group, "npc")
        self.bg_group.draw(self.screen)

        self.hero.skill_group.update()
        self.hero.skill_group.draw(self.screen)
        self.hero_group.update()
        self.hero_group.draw(self.screen)

        self.npc.skill_group.draw(self.screen)
        self.npc_group.update(self.delay, self.flag)
        self.npc_group.draw(self.screen)
        self.npc.skill_group.update()

        self.blood(self.hero, proper.blood, proper.power) # 英雄血槽
        self.blood(self.npc, proper.npc_blood, proper.npc_power) # npc血槽

    def main(self):
        while self.is_exit:
            self.clock.tick(60)
            # npc移动监听
            self.random_npc()
            # 事件监听
            self.control_keyboard()
            # 显示精灵
            self.Sprite_Group_Draw()
            pygame.display.update()
        else:
            proper.is_q = True  # 技能Q施放间隔判断
            proper.is_w = True  # 技能W施放间隔判断
            proper.key = ""  # 技能判断key
            proper.times = 0  # npc随机时间值
            proper.n = 1  # 判断npc随机值
            proper.hero_x = 0  # 英雄的x坐标
            proper.hero_y = 0  # 英雄的y坐标
            proper.hero_right = 0  # 英雄的右边x坐标
            proper.hero_bottom = 0  # 英雄的下边y坐标
            proper.is_npc_skill = True  # 判断npc飞镖次数
            proper.npc_key = ""  # npc技能判断key
            proper.skill_and_role = True  # 判断技能和人是否碰撞
            proper.skill_and_npc = True  # 判断技能和npc是否碰撞
            proper.blood = 50  # 血条
            proper.power = 50  # 蓝条
            proper.npc_blood = 50  # 血条
            proper.npc_power = 50  # 蓝条
            proper.skill_speed = 20
            proper.is_w_true = True  # 控制技能类的update函数中的线程次数
            proper.is_w_false = False  # 用来判断瞬身还是施放影子
            proper.w_key = ""  # w技能判断key
            proper.w_skill = False  # 接受w技能对象
            proper.shadow = ""  # 影子施放Q位置判断
            proper.npc_x = 0  # npc的x坐标
            proper.npc_y = 0  # npc的y坐标
            proper.npc_right = 0  # npc的右边x坐标
            proper.npc_bottom = 0  # npc的下边y坐标

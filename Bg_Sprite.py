import pygame
from properties import *
from win32api import GetSystemMetrics
import proper
import threading
import time

class Base_Sprite(pygame.sprite.Sprite):
    ''' 精灵基类 '''
    def __init__(self, image):
        super().__init__()
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.width, self.height = self.rect.width - BG_SIZE[0], self.rect.height - BG_SIZE[1]
        self.mask = pygame.mask.from_surface(self.image)

    def Move_Up(self,SPEED):
        if self.rect.y >= self.y or proper.is_fight_main:
            self.rect.y += 0
        else:
            self.rect.y += SPEED

    def Move_Down(self,SPEED):
        if self.rect.y < -(self.height-self.y) or proper.is_fight_main:
            self.rect.y += 0
        else:
            self.rect.y += SPEED

    def Move_Left(self,SPEED):
        if self.rect.x >= self.x or proper.is_fight_main:
            self.rect.x += 0
        else:
            self.rect.x += SPEED

    def Move_Right(self,SPEED):
        if self.rect.x < -(self.width-self.x) or proper.is_fight_main:
            self.rect.x += 0
        else:
            self.rect.x += SPEED

class Bg_Sprite(Base_Sprite):
    ''' 背景 '''
    def __init__(self, img):
        super().__init__(img)
        global BG_WIDTH,BG_HEIGHT
        BG_WIDTH = self.width
        BG_HEIGHT = self.height
        self.x = self.rect.x
        self.y = self.rect.y


class Grass_Sprite(Base_Sprite):
    ''' 草地 '''
    def __init__(self, x, y, img):
        super().__init__(img)
        global BG_WIDTH,BG_HEIGHT
        self.width = BG_WIDTH
        self.height = BG_HEIGHT
        self.rect.topleft = x, y
        self.x = self.rect.x
        self.y = self.rect.y

class Build_Sprite(Base_Sprite):
    ''' 所有建筑 '''
    def __init__(self, x, y, img):
        super().__init__(img)
        global BG_WIDTH,BG_HEIGHT
        self.width = BG_WIDTH
        self.height = BG_HEIGHT
        self.rect.topleft = x,y
        self.x = self.rect.x
        self.y = self.rect.y

class Player(Base_Sprite):
    ''' 玩家 '''
    def __init__(self, x, y, img, flag):
        super().__init__(img)
        global BG_WIDTH,BG_HEIGHT
        self.width = BG_WIDTH
        self.height = BG_HEIGHT
        self.rect.topleft = x,y
        self.x = self.rect.x
        self.y = self.rect.y
        self.flag = flag
        self.dialog_group = pygame.sprite.Group()

    def Create_dialog(self):
        if self.flag == "mingren":
            self.dialog = Dialog_Sprite(DIALOG_IMG)
        elif self.flag == "woailuo":
            self.dialog = Dialog_Sprite(DIALOG_IMG2)
        self.dialog_group.add(self.dialog)
        return self.dialog_group

class Role_Sprite(pygame.sprite.Sprite):
    ''' 主人公类 '''
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(D_IMG)
        self.rect = self.image.get_rect()
        self.rect.topleft = (BG_SIZE[0] - self.rect.width) // 2, (BG_SIZE[1] - self.rect.height) // 2
        self.mask = pygame.mask.from_surface(self.image)
        self.key = ""
        self.flag = ""

    def change_action(self, img, l_img, r_img):
        # 角色动态
        # 2换左脚，1换右脚，否则停下
        self.image = pygame.image.load(img)
        if self.flag == 2:
            self.image = pygame.image.load(l_img)
        elif self.flag == 1:
            self.image = pygame.image.load(r_img)
        elif self.flag:
            self.image = pygame.image.load(img)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, *args):
        ''' 改变人物方向'''
        if self.key == "U" and not proper.is_fight_main:
            self.change_action(U_IMG,UL_IMG,UR_IMG)
        if self.key == "D" and not proper.is_fight_main:
            self.change_action(D_IMG, DL_IMG, DR_IMG)
        if self.key == "L" and not proper.is_fight_main:
            self.change_action(L_IMG, LL_IMG, LR_IMG)
        if self.key == "R" and not proper.is_fight_main:
            self.change_action(R_IMG, RL_IMG, RR_IMG)

class Hero_Sprite(pygame.sprite.Sprite):
    ''' 英雄类 '''
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(HERO_IMG)
        self.rect = self.image.get_rect()
        self.rect.topleft = 0, GetSystemMetrics(1) - self.rect.height
        self.mask = pygame.mask.from_surface(self.image)
        self.key = ""
        self.flag = ""
        # 创建技能的精灵组
        self.skill_group = pygame.sprite.Group()


    def change_action(self, img, l_img, r_img):
        # 角色动态
        # 2换左脚，1换右脚，否则停下
        self.image = pygame.image.load(img)
        if self.flag == 2:
            self.image = pygame.image.load(l_img)
        elif self.flag == 1:
            self.image = pygame.image.load(r_img)
        elif self.flag:
            self.image = pygame.image.load(img)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, *args):
        ''' 改变人物方向'''
        if self.key == "U":
            self.change_action(U_IMG,UL_IMG,UR_IMG)
        if self.key == "D":
            self.change_action(D_IMG, DL_IMG, DR_IMG)
        if self.key == "L":
            self.change_action(L_IMG, LL_IMG, LR_IMG)
        if self.key == "R":
            self.change_action(R_IMG, RL_IMG, RR_IMG)
        if self.key == "UL":
            self.change_action(L_IMG, LL_IMG, LR_IMG)
        if self.key == "UR":
            self.change_action(L_IMG, LL_IMG, LR_IMG)
        if self.key == "DL":
            self.change_action(L_IMG, LL_IMG, LR_IMG)
        if self.key == "DR":
            self.change_action(L_IMG, LL_IMG, LR_IMG)

        proper.hero_x = self.rect.x
        proper.hero_y = self.rect.y
        proper.hero_right = self.rect.right
        proper.hero_bottom = self.rect.bottom

    def Move_Up(self,SPEED):
        if self.rect.y <= 0:
            self.rect.y += 0
        else:
            self.rect.y += SPEED

    def Move_Down(self,SPEED):
        if self.rect.y >= GetSystemMetrics(1) - self.rect.height:
            self.rect.y += 0
        else:
            self.rect.y += SPEED

    def Move_Left(self,SPEED):
        if self.rect.x <= 0:
            self.rect.x += 0
        else:
            self.rect.x += SPEED

    def Move_Right(self,SPEED):
        if self.rect.x >= GetSystemMetrics(0) - self.rect.width:
            self.rect.x += 0
        else:
            self.rect.x += SPEED

    def Move_Empty(self, SPEED):
        pass

    def Create_Skill(self):
        '''创建飞镖技能'''
        # 蓝条减少
        proper.power -= 5
        # 创建技能
        skill = Skill()
        # 技能方向默认向右
        skill.rect.x = self.rect.x
        skill.rect.y = self.rect.y
        if proper.key== "":
            skill.rect.x = self.rect.x + self.rect.width
        if proper.key == "U":
            skill.rect.y = self.rect.y - skill.rect.height
        if proper.key == "D":
            skill.rect.y = self.rect.y + self.rect.height
        if proper.key == "L":
            skill.rect.x = self.rect.x - self.rect.width
        if proper.key == "R":
            skill.rect.x = self.rect.x + self.rect.width
        if proper.key == "UL":
            skill.rect.x = self.rect.x - self.rect.width
            skill.rect.y = self.rect.y - skill.rect.height
        if proper.key == "UR":
            skill.rect.x = self.rect.x + self.rect.width
            skill.rect.y = self.rect.y - skill.rect.height
        if proper.key == "DL":
            skill.rect.x = self.rect.x - self.rect.width
            skill.rect.y = self.rect.y + skill.rect.height
        if proper.key == "DR":
            skill.rect.x = self.rect.x + self.rect.width
            skill.rect.y = self.rect.y + skill.rect.height

        self.skill_group.add(skill)

    def Create_Shadow_Skill(self, rect):
        '''影子施放Q技能精灵类'''
        proper.npc_skill_and_role = True
        skill = Shadow_Skill()
        skill.rect.x = rect.x
        skill.rect.y = rect.y
        self.flag = ""
        if rect.y < proper.npc_bottom and rect.bottom > proper.npc_y:  # 左右
            if rect.x > proper.npc_x:
                proper.shadow_flag = 2
                skill.rect.x = rect.x - rect.width
            elif rect.x < proper.npc_x:
                proper.shadow_flag = 3
                skill.rect.x = rect.x + rect.width
        elif rect.x < proper.npc_right and rect.right > proper.npc_x:  # 上下
            if rect.y > proper.npc_y:
                proper.shadow_flag = 0
                skill.rect.y = rect.y - skill.rect.height
            elif rect.bottom < proper.npc_bottom:
                proper.shadow_flag = 1
                skill.rect.y = rect.y + rect.height
        elif rect.x > proper.npc_x and rect.bottom > proper.npc_bottom:  # 上左
            proper.shadow_flag = 4
            skill.rect.x = rect.x - rect.width
            skill.rect.y = rect.y - skill.rect.height
        elif rect.right < proper.npc_x and rect.bottom > proper.npc_bottom:  # 上右
            proper.shadow_flag = 5
            skill.rect.x = rect.x + rect.width
            skill.rect.y = rect.y - skill.rect.height
        elif rect.x > proper.npc_right and rect.bottom < proper.npc_bottom:  # 下左
            proper.shadow_flag = 6
            skill.rect.x = rect.x - rect.width
            skill.rect.y = rect.y + skill.rect.height
        elif rect.right < proper.npc_x and rect.bottom < proper.npc_bottom:  # 下右
            proper.shadow_flag = 7
            skill.rect.x = rect.x + rect.width
            skill.rect.y = rect.y + skill.rect.height
        self.skill_group.add(skill)

    def Create_Skill_W(self):
        '''创建影子技能'''
        # 蓝条减少
        proper.power -= 5
        # 创建技能
        skill = Skill_W()
        # 技能方向默认向右
        skill.rect.x = self.rect.x
        skill.rect.y = self.rect.y
        if proper.w_key== "":
            skill.rect.x = skill.rect.x + skill.rect.width
        if proper.w_key == "U":
            skill.rect.y = skill.rect.y - skill.rect.height
        if proper.w_key == "D":
            skill.rect.y = skill.rect.y + skill.rect.height
        if proper.w_key == "L":
            skill.rect.x = skill.rect.x - skill.rect.width
        if proper.w_key == "R":
            skill.rect.x = skill.rect.x + skill.rect.width
        if proper.w_key == "UL":
            skill.rect.x = skill.rect.x - skill.rect.width
            skill.rect.y = skill.rect.y - skill.rect.height
        if proper.w_key == "UR":
            skill.rect.x = skill.rect.x + skill.rect.width
            skill.rect.y = skill.rect.y - skill.rect.height
        if proper.w_key == "DL":
            skill.rect.x = skill.rect.x - skill.rect.width
            skill.rect.y = skill.rect.y + skill.rect.height
        if proper.w_key == "DR":
            skill.rect.x = skill.rect.x + skill.rect.width
            skill.rect.y = skill.rect.y + skill.rect.height

        self.skill_group.add(skill)
        return skill

    # def Create_Skill_E(self):
    #     '''创建鬼斩技能'''
    #     # 蓝条减少
    #     proper.power -= 5
    #     # 创建技能
    #     skill = Skill_E()
    #     # 技能方向默认向右
    #     skill.rect.x = self.rect.x
    #     skill.rect.y = self.rect.y
    #     self.skill_group.add(skill)

class Shadow_Skill(Base_Sprite):
    '''影子创建Q技能精灵类'''

    def __init__(self):
        super().__init__(SKILL_IMG)
        self.skill_width = self.rect.width * 6
        self.i = 0
        self.flag = "wq"
        self.skill_and_npc = True

    def update(self):
        if proper.npc_dict[proper.shadow_flag] == "U":
            self.rect.y -= SPEED
            self.is_alives()

        if proper.npc_dict[proper.shadow_flag] == "D":
            self.rect.y += SPEED
            self.is_alives()

        if proper.npc_dict[proper.shadow_flag] == "L":
            self.rect.x -= SPEED
            self.is_alives()

        if proper.npc_dict[proper.shadow_flag] == "R":
            self.rect.x += SPEED
            self.is_alives()

        if proper.npc_dict[proper.shadow_flag] == "UL":
            self.rect.x -= SPEED
            self.rect.y -= SPEED
            self.is_alives()

        if proper.npc_dict[proper.shadow_flag] == "UR":
            self.rect.x += SPEED
            self.rect.y -= SPEED
            self.is_alives()

        if proper.npc_dict[proper.shadow_flag] == "DL":
            self.rect.x -= SPEED
            self.rect.y += SPEED
            self.is_alives()

        if proper.npc_dict[proper.shadow_flag] == "DR":
            self.rect.x += SPEED
            self.rect.y += SPEED
            self.is_alives()

    def is_alives(self):
        self.i += SPEED
        if self.i >= self.skill_width:
            self.kill()


class Skill(Base_Sprite):
    '''飞镖技能精灵类'''
    def __init__(self):
        super().__init__(SKILL_IMG)
        self.x = self.rect.width * 6
        self.i = 0
        self.flag = "q"
        self.skill_and_npc = True

    def update(self):
        if proper.key == "":
            self.rect.x += SKILL_SPEED
            self.is_alives()

        if proper.key == "U":
            self.rect.y -= SKILL_SPEED
            self.is_alives()

        if proper.key == "D":
            self.rect.y += SKILL_SPEED
            self.is_alives()

        if proper.key == "L":
            self.rect.x -= SKILL_SPEED
            self.is_alives()

        if proper.key == "R":
            self.rect.x += SKILL_SPEED
            self.is_alives()

        if proper.key == "UL":
            self.rect.x -= SKILL_SPEED
            self.rect.y -= SKILL_SPEED
            self.is_alives()

        if proper.key == "UR":
            self.rect.x += SKILL_SPEED
            self.rect.y -= SKILL_SPEED
            self.is_alives()

        if proper.key == "DL":
            self.rect.x -= SKILL_SPEED
            self.rect.y += SKILL_SPEED
            self.is_alives()

        if proper.key == "DR":
            self.rect.x += SKILL_SPEED
            self.rect.y += SKILL_SPEED
            self.is_alives()

    def is_alives(self):
        self.i += SPEED
        if self.i >= self.x:
            self.kill()
            proper.is_q = True
            if proper.power <= 0:
                proper.is_q = False



class Skill_W(Base_Sprite):
    '''影子技能精灵类'''
    def __init__(self):
        super().__init__(SKILL_W2_IMG)
        self.x = self.rect.width * 4
        self.i = 0
        self.flag = ""
        self.skill_and_npc = False

    def update(self):
        if proper.w_key == "":
            self.rect.x += proper.skill_speed
            self.is_alives()

        if proper.w_key == "U":
            if self.rect.y <= 0:
                self.rect.y -= 0
            else:
                self.rect.y -= proper.skill_speed
            self.is_alives()

        if proper.w_key == "D":
            if self.rect.bottom >= GetSystemMetrics(1):
                self.rect.y += 0
            else:
                self.rect.y += proper.skill_speed
            self.is_alives()

        if proper.w_key == "L":
            if self.rect.x <= 0:
                self.rect.x -= 0
            else:
                self.rect.x -= proper.skill_speed
            self.is_alives()

        if proper.w_key == "R":
            if self.rect.right >= GetSystemMetrics(0):
                self.rect.x += 0
            else:
                self.rect.x += proper.skill_speed
            self.is_alives()

        if proper.w_key == "UL":
            if self.rect.y <= 0 or self.rect.x <= 0:
                self.rect.x -= 0
                self.rect.y -= 0
            else:
                self.rect.x -= proper.skill_speed
                self.rect.y -= proper.skill_speed
            self.is_alives()

        if proper.w_key == "UR":
            if self.rect.y <= 0 or self.rect.right >= GetSystemMetrics(0):
                self.rect.x += 0
                self.rect.y -= 0
            else:
                self.rect.x += proper.skill_speed
                self.rect.y -= proper.skill_speed
            self.is_alives()

        if proper.w_key == "DL":
            if self.rect.bottom >= GetSystemMetrics(1) or self.rect.x <= 0:
                self.rect.x -= 0
                self.rect.y += 0
            else:
                self.rect.x -= proper.skill_speed
                self.rect.y += proper.skill_speed
            self.is_alives()

        if proper.w_key == "DR":
            if self.rect.bottom >= GetSystemMetrics(1) or self.rect.right >= GetSystemMetrics(0):
                self.rect.x += 0
                self.rect.y -= 0
            else:
                self.rect.x += proper.skill_speed
                self.rect.y += proper.skill_speed
            self.is_alives()

    def is_alives(self):
        self.i += SPEED
        if self.i >= self.x:
            proper.skill_speed = 0
            self.image = pygame.image.load(SKILL_W_IMG)
            if proper.is_w_true:
                t = threading.Thread(target=self.timing, args=())
                t.start()
            if proper.power <= 0:
                proper.is_w = False

    def timing(self):
        proper.is_w_true = False
        print("线程开启了")
        while not proper.is_w_true:
            time.sleep(4)
            proper.skill_speed = 20
            self.kill()
            proper.is_w = True
            proper.is_w_true = True
            proper.w_skill = False


# class Skill_E(Base_Sprite):
#     '''鬼斩技能精灵类'''
#     def __init__(self):
#         super().__init__(SKILL_E_IMG)
#         self.flag = "e"
#         self.skill_and_npc = True
#
#     def update(self, *args):
#         self.rect.x = proper.hero_x
#         self.rect.y = proper.hero_y
#         t = threading.Thread(target=self.timing, args=())
#         t.start()
#
#     def timing(self):
#         proper.is_e = False
#         while not proper.is_e:
#             print("E线程开启了")
#             time.sleep(0.1)
#             self.kill()
#             proper.is_e = True


class NPC_Skill(Base_Sprite):
    '''NPC技能精灵类'''

    def __init__(self):
        super().__init__(SKILL_IMG)
        self.x = self.rect.width * 6
        self.i = 0

    def update(self):

        if proper.npc_dict[proper.npc_key] == "U":
            self.rect.y -= SKILL_SPEED
            self.is_alives()

        if proper.npc_dict[proper.npc_key] == "D":
            self.rect.y += SKILL_SPEED
            self.is_alives()

        if proper.npc_dict[proper.npc_key] == "L":
            self.rect.x -= SKILL_SPEED
            self.is_alives()

        if proper.npc_dict[proper.npc_key] == "R":
            self.rect.x += SKILL_SPEED
            self.is_alives()

        if proper.npc_dict[proper.npc_key] == "UL":
            self.rect.x -= SKILL_SPEED
            self.rect.y -= SKILL_SPEED
            self.is_alives()

        if proper.npc_dict[proper.npc_key] == "UR":
            self.rect.x += SKILL_SPEED
            self.rect.y -= SKILL_SPEED
            self.is_alives()

        if proper.npc_dict[proper.npc_key] == "DL":
            self.rect.x -= SKILL_SPEED
            self.rect.y += SKILL_SPEED
            self.is_alives()

        if proper.npc_dict[proper.npc_key] == "DR":
            self.rect.x += SKILL_SPEED
            self.rect.y += SKILL_SPEED
            self.is_alives()

    def is_alives(self):
        self.i += SPEED
        if self.i >= self.x:
            self.kill()

class NPC_Sprite(pygame.sprite.Sprite):
    ''' NPC类 '''
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(L_IMG)
        self.rect = self.image.get_rect()
        self.rect.topleft  = GetSystemMetrics(0)-self.rect.width,0
        self.mask = pygame.mask.from_surface(self.image)
        self.key = ""
        self.skill_group = pygame.sprite.Group()
        self.move_list = [self.Move_Up,self.Move_Down,self.Move_Left,self.Move_Right,self.Move_TopLeft,self.Move_TopRight,self.Move_DownLeft,self.Move_DownRight]

    def Move_Up(self, SPEED):
        if self.rect.top <= 0:
            self.rect.y += 0
        else:
            self.rect.y -= SPEED

    def Move_Down(self, SPEED):
        if self.rect.y >= GetSystemMetrics(1)-self.rect.height:
            self.rect.y += 0
        else:
            self.rect.y += SPEED

    def Move_Left(self, SPEED):
        if self.rect.x <= 0:
            self.rect.x += 0
        else:
            self.rect.x -= SPEED

    def Move_Right(self, SPEED):
        if self.rect.x >= GetSystemMetrics(0)-self.rect.width:
            self.rect.x += 0
        else:
            self.rect.x += SPEED

    def Move_TopLeft(self, SPEED):
        if self.rect.x <= 0 and self.rect.y <= 0:
            self.rect.x += 0
            self.rect.y += 0
        elif self.rect.x <= 0:
            self.rect.x += 0
            self.rect.y -= SPEED
        elif self.rect.y <= 0:
            self.rect.x -= SPEED
            self.rect.y += 0
        else:
            self.rect.x -= SPEED
            self.rect.y -= SPEED

    def Move_TopRight(self, SPEED):
        if self.rect.x >= GetSystemMetrics(0) - self.rect.width and self.rect.y <= 0:
            self.rect.x += 0
            self.rect.y += 0
        elif self.rect.x >= GetSystemMetrics(0) - self.rect.width:
            self.rect.x += 0
            self.rect.y -= SPEED
        elif self.rect.y <= 0:
            self.rect.x += SPEED
            self.rect.y += 0
        else:
            self.rect.x += SPEED
            self.rect.y -= SPEED

    def Move_DownLeft(self, SPEED):
        if self.rect.x <= 0 and self.rect.y >= GetSystemMetrics(1)-self.rect.height:
            self.rect.x += 0
            self.rect.y += 0
        elif self.rect.x <= 0:
            self.rect.x += 0
            self.rect.y += SPEED
        elif self.rect.y >= GetSystemMetrics(1)-self.rect.height:
            self.rect.x -= SPEED
            self.rect.y += 0
        else:
            self.rect.x -= SPEED
            self.rect.y += SPEED

    def Move_DownRight(self, SPEED):
        if self.rect.x >= GetSystemMetrics(0)-self.rect.width and self.rect.y >= GetSystemMetrics(1)-self.rect.height:
            self.rect.x += 0
            self.rect.y += 0
        elif self.rect.x >= GetSystemMetrics(0)-self.rect.width:
            self.rect.x += 0
            self.rect.y += SPEED
        elif self.rect.y >= GetSystemMetrics(1)-self.rect.height:
            self.rect.x += SPEED
            self.rect.y += 0
        else:
            self.rect.x += SPEED
            self.rect.y += SPEED

    def Move_Empty(self, SPEED):
        pass

    def change_action(self, img, l_img, r_img, flag):
        # 角色动态
        # 2换左脚，1换右脚，否则停下
        self.image = pygame.image.load(img)
        if flag == 2:
            self.image = pygame.image.load(l_img)
        elif flag == 1:
            self.image = pygame.image.load(r_img)
        elif flag:
            self.image = pygame.image.load(img)
        self.mask = pygame.mask.from_surface(self.image)

    def Create_Skill(self):
        # 技能
        # 蓝条减少
        proper.npc_power -= 5
        self.skill = NPC_Skill()
        self.skill.rect.x = self.rect.x
        self.skill.rect.y = self.rect.y

        if proper.npc_dict[proper.npc_key] == "U":
            self.skill.rect.y = self.rect.y - self.skill.rect.height
        if proper.npc_dict[proper.npc_key] == "D":
            self.skill.rect.y = self.rect.y + self.rect.height
        if proper.npc_dict[proper.npc_key] == "L":
            self.skill.rect.x = self.rect.x - self.rect.width
        if proper.npc_dict[proper.npc_key] == "R":
            self.skill.rect.x = self.rect.x + self.rect.width
        if proper.npc_dict[proper.npc_key] == "UL":
            self.skill.rect.x = self.rect.x - self.rect.width
            self.skill.rect.y = self.rect.y - self.skill.rect.height
        if proper.npc_dict[proper.npc_key] == "UR":
            self.skill.rect.x = self.rect.x + self.rect.width
            self.skill.rect.y = self.rect.y - self.skill.rect.height
        if proper.npc_dict[proper.npc_key] == "DL":
            self.skill.rect.x = self.rect.x - self.rect.width
            self.skill.rect.y = self.rect.y + self.skill.rect.height
        if proper.npc_dict[proper.npc_key] == "DR":
            self.skill.rect.x = self.rect.x + self.rect.width
            self.skill.rect.y = self.rect.y + self.skill.rect.height
        self.skill_group.add(self.skill)

    def update(self,delay,flag):
        if self.rect.y < proper.hero_bottom and self.rect.bottom > proper.hero_y:  # 左右
            if self.rect.x > proper.hero_x:
                proper.n = 2
                self.move_list[proper.n](NPC_SPEED)
                if self.rect.x - proper.hero_x < self.rect.width * 6:
                    self.is_skill()
            elif self.rect.x < proper.hero_x:
                proper.n = 3
                self.move_list[proper.n](NPC_SPEED)
                if proper.hero_x - self.rect.x < self.rect.width * 6:
                    self.is_skill()
        elif self.rect.x < proper.hero_right and self.rect.right > proper.hero_x:  # 上下
            if self.rect.y > proper.hero_y:
                proper.n = 0
                self.move_list[proper.n](NPC_SPEED)
                if self.rect.y - proper.hero_y < self.rect.width * 6:
                    self.is_skill()
            elif self.rect.bottom < proper.hero_bottom:
                proper.n = 1
                self.move_list[proper.n](NPC_SPEED)
                if proper.hero_bottom - self.rect.bottom < self.rect.width * 6:
                    self.is_skill()
        elif self.rect.x > proper.hero_x and self.rect.bottom > proper.hero_bottom: # 上左
            proper.n = 4
            self.move_list[proper.n](NPC_SPEED)
            if self.rect.x - proper.hero_x < self.rect.width * 6 and self.rect.bottom - proper.hero_bottom < self.rect.width * 6:
                self.is_skill()

        elif self.rect.right < proper.hero_x and self.rect.bottom > proper.hero_bottom: # 上右
            proper.n = 5
            self.move_list[proper.n](NPC_SPEED)
            if proper.hero_x - self.rect.right < self.rect.width * 6 and self.rect.bottom  - proper.hero_bottom < self.rect.width * 6:
                self.is_skill()

        elif self.rect.x > proper.hero_right and self.rect.bottom < proper.hero_bottom: # 下左
            proper.n = 6
            self.move_list[proper.n](NPC_SPEED)
            if self.rect.x - proper.hero_right < self.rect.width * 6 and proper.hero_bottom - self.rect.bottom < self.rect.width * 6:
                self.is_skill()
        elif self.rect.right < proper.hero_x and self.rect.bottom < proper.hero_bottom: # 下右
            proper.n = 7
            self.move_list[proper.n](NPC_SPEED)
            if proper.hero_x - self.rect.right < self.rect.width * 6 and proper.hero_bottom - self.rect.bottom < self.rect.width * 6:
                self.is_skill()

        ''' 改变人物方向 0、上 1、下 2、左 3、右 4、上左 5、上右 6、下左 7、下右'''
        if proper.n == 0:
            self.change_action(U_IMG,UL_IMG,UR_IMG,flag)
        if proper.n == 1:
            self.change_action(D_IMG, DL_IMG, DR_IMG,flag)
        if proper.n == 2:
            self.change_action(L_IMG, LL_IMG, LR_IMG,flag)
        if proper.n == 3:
            self.change_action(R_IMG, RL_IMG, RR_IMG,flag)
        if proper.n == 4:
            self.change_action(L_IMG, ULL_IMG, ULR_IMG,flag)
        if proper.n == 5:
            self.change_action(R_IMG, URL_IMG, URR_IMG,flag)
        if proper.n == 6:
            self.change_action(L_IMG, DLL_IMG, DLR_IMG,flag)
        if proper.n == 7:
            self.change_action(R_IMG, DRL_IMG, DRR_IMG,flag)

        proper.npc_x = self.rect.x
        proper.npc_y = self.rect.y
        proper.npc_right = self.rect.right
        proper.npc_bottom = self.rect.bottom

    def timing(self):
        while not proper.is_npc_skill:
            time.sleep(2)
            proper.is_npc_skill = True
            if proper.npc_power <= 0:
                proper.is_npc_skill = False
            proper.skill_and_role = True

    def is_skill(self):
        '''判断是否施放技能'''
        if proper.is_npc_skill:
            proper.npc_key = proper.n
            self.Create_Skill()
            proper.is_npc_skill = False
            t = threading.Thread(target=self.timing, args=())
            t.start()



class Dialog_Sprite(pygame.sprite.Sprite):
    '''对话框'''

    def __init__(self, img):
        super().__init__()
        self.image = pygame.image.load(img).convert()
        self.rect = self.image.get_rect()
        self.rect.y = GetSystemMetrics(1) - self.rect.height
        pygame.Surface.set_alpha(self.image, 180)

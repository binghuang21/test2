# -- coding: utf-8 --
from utils import normalization
import pygame
from numpy import random
import numpy as np
from math import sqrt, sin, cos, pi


def count_distance_fast(a1, a2, b1, b2):
    return sqrt((a1 - b1) ** 2 + (a2 - b2) ** 2)

class Agent(pygame.sprite.Sprite):
    '''
    #定义半径、速度、屏幕长宽、墙、类型
    def __init__(self, id, radius, speed, screen_width, screen_height, walls, type):
        pygame.sprite.Sprite.__init__(self)
        self.SCREEN_WIDTH = screen_width
        self.SCREEN_HEIGHT = screen_height
        self.speed = speed
        self.radius = radius
        self.velocity = [0, 0]    #速度
        self.image = None
        self.rect = None
        self.pos = [0, 0]
        self.id = id
        self.init_pos = None
        self.init_dir = None
        self.walls = walls
        self.type = type
    '''
        
    #定义半径、速度、屏幕长宽、墙、类型
    #def __init__(self, id, radius, speed, screen_width, screen_height, walls, blood type):
    def __init__(self, id, radius, speed, screen_width, screen_height, blood, swim_angle, type):
        pygame.sprite.Sprite.__init__(self)
        self.SCREEN_WIDTH = screen_width
        self.SCREEN_HEIGHT = screen_height
        self.speed = speed
        self.radius = radius
        self.velocity = [0, 0]    #速度
        self.image = None
        self.rect = None
        self.pos = [0, 0]
        self.id = id
        self.init_pos = None
        self.init_dir = None
        #self.walls = walls
        self.blood = blood
        self.type = type
        #self.swim_angle = 0    #！新加入swim_angle的定义


#定义位置
    def init_positon(self, pos):
        self.init_pos = [pos[0], pos[1]]

#定义方向
    def init_direction(self, velocity):
        self.init_dir = [velocity[0], velocity[1]]

#重置位置
    def reset_pos(self):
        self.pos[0] = self.init_pos[0]
        self.pos[1] = self.init_pos[1]

#重置方向
    def reset_orientation(self):
        self.velocity[0] = self.init_dir[0]
        self.velocity[1] = self.init_dir[1]

#随机位置
    def rand_pos(self):
        self.pos[0] = random.uniform(self.radius, self.SCREEN_WIDTH - self.radius)
        self.pos[1] = random.uniform(self.radius, self.SCREEN_HEIGHT - self.radius)

#随机方向
    def rand_orientation(self):
        self.velocity[0] = random.random() - 0.5
        self.velocity[1] = random.random() - 0.5
        self.velocity = normalization(self.velocity)    #归一化函数

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect.center)


class PAgent(pygame.sprite.Sprite):
        
    #定义半径、速度、屏幕长宽、墙、类型
    #def __init__(self, id, radius, speed, screen_width, screen_height, walls, blood type):
    def __init__(self, id, radius, speed, screen_width, screen_height, blood, type):
        pygame.sprite.Sprite.__init__(self)
        self.SCREEN_WIDTH = screen_width
        self.SCREEN_HEIGHT = screen_height
        self.speed = speed
        self.radius = radius
        self.velocity = [0, 0]    #速度
        self.image = None
        self.rect = None
        self.pos = [0, 0]
        self.id = id
        self.init_pos = None
        self.init_dir = None
        #self.walls = walls
        self.blood = blood
        self.type = type


#定义位置
    def init_positon(self, pos):
        self.init_pos = [pos[0], pos[1]]

#定义方向
    def init_direction(self, velocity):
        self.init_dir = [velocity[0], velocity[1]]

#重置位置
    def reset_pos(self):
        self.pos[0] = self.init_pos[0]
        self.pos[1] = self.init_pos[1]

#重置方向
    def reset_orientation(self):
        self.velocity[0] = self.init_dir[0]
        self.velocity[1] = self.init_dir[1]

#随机位置
    def rand_pos(self):
        self.pos[0] = random.uniform(self.radius, self.SCREEN_WIDTH - self.radius)
        self.pos[1] = random.uniform(self.radius, self.SCREEN_HEIGHT - self.radius)

#随机方向
    def rand_orientation(self):
        self.velocity[0] = random.random() - 0.5
        self.velocity[1] = random.random() - 0.5
        self.velocity = normalization(self.velocity)    #归一化函数

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect.center)


#!!尝试把other类改成其他三个角色的运动过程
class Other(Agent):
    #def __init__(self, id, radius, color, speed, screen_width, screen_height, walls, type):
        #Agent.__init__(self, id, radius, speed, screen_width, screen_height, walls, type)
    def __init__(self, id, radius, color, speed, screen_width, screen_height, blood, type):
        Agent.__init__(self, id, radius, speed, screen_width, screen_height, blood, type)
        image = pygame.Surface([radius * 2, radius * 2])    #绘制半径^2 半径^2的图像
        image.set_colorkey((0, 0, 0))
        pygame.draw.circle(
            image,
            color,
            (radius, radius),
            radius,
            0
        )
        self.image = image.convert()
        self.rect = self.image.get_rect()

    def update(self, dt):
        new_x = self.pos[0] + self.velocity[0] * self.speed * dt
        #新位置x坐标=上一位置x坐标+当前x方向归一化分速度*物体速度*dt
        new_y = self.pos[1] + self.velocity[1] * self.speed * dt

        flag = True
        '''
        #！此处要考虑flag为真假时的区别，wall和screen的区别？？
        for wall in self.walls:
            #如果 墙_左<new_x<墙_右,new_y出界的状态，y坐标为边界加减半径，速度变为相反方向速度（应该是）
            if wall.rect.left < new_x < wall.rect.right:
                if wall.rect.top < new_y - self.radius < wall.rect.bottom:
                    self.pos[1] = wall.rect.bottom + self.radius
                    self.velocity[1] = -self.velocity[1]
                    flag = False
                elif wall.rect.top < new_y + self.radius < wall.rect.bottom:
                    self.pos[1] = wall.rect.top - self.radius
                    self.velocity[1] = -self.velocity[1]
                    flag = False
            #如果 墙_top<new_y<墙_bottom,new_x出界的状态，x坐标为边界加减半径，速度变为相反方向速度（应该是）
            if wall.rect.top < new_y < wall.rect.bottom:
                if wall.rect.left < new_x - self.radius < wall.rect.right:
                    self.pos[0] = wall.rect.right + self.radius
                    self.velocity[0] = -self.velocity[0]
                    flag = False
                elif wall.rect.left < new_x + self.radius < wall.rect.right:
                    self.pos[0] = wall.rect.left - self.radius
                    self.velocity[0] = -self.velocity[0]
                    flag = False
        '''

        if flag:
        #如果碰到screen边，位置为边界-半径，速度相反
            if new_x >= self.SCREEN_WIDTH - self.radius:
                self.pos[0] = self.SCREEN_WIDTH - self.radius
                self.velocity[0] = -self.velocity[0]
                
            elif new_x < self.radius:
                self.pos[0] = self.radius
                self.velocity[0] = -self.velocity[0]
            else:
                self.pos[0] = new_x

            if new_y >= self.SCREEN_HEIGHT - self.radius:
                self.pos[1] = self.SCREEN_HEIGHT - self.radius
                self.velocity[1] = -self.velocity[1]
            elif new_y < self.radius:
                self.pos[1] = self.radius
                self.velocity[1] = -self.velocity[1]
            else:
                self.pos[1] = new_y

        self.rect.center = (self.pos[0], self.pos[1])
        
        
#考虑要不要初设Rook的参数，运动轨迹已编写，需添加扫描和射击
#红色
class Rook(Agent):
    #def __init__(self, id, radius, color, speed, screen_width, screen_height, walls, type):
        #Agent.__init__(self, id, radius, speed, screen_width, screen_height, walls, type)
    def __init__(self, id, radius, color, speed, screen_width, screen_height, blood, swim_angle, type):
        #flag量有swim_angle游泳方向, scan扫描, cannnon射击，这三个要用函数表示，同时添加角度变量
        #删掉swim，让它处于运动中，每次都要计算xy方向上的分速度
        Agent.__init__(self, id, radius, speed, screen_width, screen_height, blood, swim_angle, type)
        image = pygame.Surface([radius * 2, radius * 2])    #绘制半径^2 半径^2的图像
        image.set_colorkey((0, 0, 0))
        pygame.draw.circle(
            image,
            color,
            (radius, radius),
            radius,
            0
        )
        self.image = image.convert()
        self.rect = self.image.get_rect()
        #self.speed = speed
        self.speed = 100
        self.radius = radius
        self.swim_angle = swim_angle
        #self.dx = 1
        #self.dy = 0
        
        '''
    def scan(self, angle, scan_num):
        flag = 0
        if count_distance_fast(self.pos[0], self.pos[1], Counter.pos[0], Counter.pos[1]) <= 70 && (math.abs(Counter.pos[1]-self.pos[1]) <= 2 || math.abs(Counter.pos[0]-self.pos[0]) <= 2):
            self.distance = count_distance_fast(self.pos[0], self.pos[1], Counter.pos[0], Counter.pos[1])
            flag = 1
            return self.distance
        elif count_distance_fast(self.pos[0], self.pos[1], Player.pos[0], Player.pos[1]) <= 70 && (math.abs(Counter.pos[1]-self.pos[1]) <= 2 || math.abs(Counter.pos[0]-self.pos[0]) <= 2):
            self.distance = count_distance_fast(self.pos[0], self.pos[1], Player.pos[0], Player.pos[1])
            flag = 1
            return self.distance
        else
            self.distance = 100
            return 100
         '''
         
    def update(self, dt):
        sin_swim_angle = sin(self.swim_angle)
        cos_swim_angle = cos(self.swim_angle)
        #self.velocity[0] = np.clip(self.speed * cos_swim_angle, a_min=0, a_max= 100)
        #self.velocity[1] = np.clip(self.speed * sin_swim_angle, a_min=0, a_max= 100)

        new_x = self.pos[0] + self.velocity[0] * dt
        new_y = self.pos[1] + self.velocity[1] * dt

        flag = True
        #self.velocity[0] = -20

        if flag:
        #如果碰到screen边，掉头
            '''
            if new_x >= self.SCREEN_WIDTH - self.radius:
                self.pos[0] = self.SCREEN_WIDTH - self.radius
                self.velocity[0] = -self.velocity[0]    #掉头
                self.swim_angle = (self.swim_angle + pi)%(2*pi)   #!掉头之后更改角度
            elif new_x < self.radius:
                self.pos[0] = self.radius    #如果智能体坐标小于半径，即碰到左壁
                self.velocity[0] = -self.velocity[0]    #掉头
                self.swim_angle = (self.swim_angle + pi)%(2*pi)    #!掉头之后更改角度
            else:
                self.pos[0] = new_x
            '''
            '''
            #如果不在y=50处，朝y=50处游
            if new_y >= 251:
                #self.velocity[0] = 0
                self.swim_angle = pi + pi/2
                self.pos[1] = new_y
            elif new_y < 249:
                #self.velocity[0] = 0
                self.swim_angle = pi/2
                self.pos[1] = new_y
            else:
                self.swim_angle = pi
                self.pos[1] = 250
                if new_x >= self.SCREEN_WIDTH - 10:
                    self.pos[0] = self.SCREEN_WIDTH - 10
                    self.velocity[0] = -self.velocity[0]    #掉头
                    self.swim_angle = (self.swim_angle + pi)%(2*pi)   #!掉头之后更改角度
                #elif new_x < self.radius:
                elif new_x < 10:
                    self.pos[0] = 10    #如果智能体坐标小于半径，即碰到左壁
                    self.velocity[0] = -self.velocity[0]    #掉头
                    self.swim_angle = (self.swim_angle + pi)%(2*pi)    #!掉头之后更改角度
                else:
                    self.velocity[0] = 100
                    self.pos[0] = new_x
            
            #下面的是最开始的
            '''
            #如果不在y=50处，朝y=50处游,本趴有效
            if new_y >= 151:
                #self.velocity[0] = 0
                self.velocity[1] = np.clip(self.velocity[1] - 0.1, a_min=-self.SCREEN_WIDTH * 0.3,
                                       a_max=self.SCREEN_WIDTH * 0.3)
                self.velocity[0] = np.clip(self.velocity[1] + 0.5, a_min=-self.SCREEN_WIDTH * 0.3,
                                       a_max=self.SCREEN_WIDTH * 0.3)
                self.swim_angle = pi + pi/2
                self.pos[1] = new_y
            elif new_y < 149:
                #self.velocity[0] = 0
                self.swim_angle = pi/2
                self.velocity[1] = np.clip(self.velocity[1] + 0.1, a_min=-self.SCREEN_WIDTH * 0.3,
                                       a_max=self.SCREEN_WIDTH * 0.3)
                self.velocity[0] = np.clip(self.velocity[0] - 0.5, a_min=-self.SCREEN_WIDTH * 0.3,
                                       a_max=self.SCREEN_WIDTH * 0.3)
                self.pos[1] = new_y
            else:
                self.swim_angle = pi
                self.pos[1] = 150
            
            #self.velocity[0] = -20
            #self.velocity[0] = np.clip(self.velocity[0], a_min=-self.SCREEN_WIDTH * 0.3, a_max=self.SCREEN_WIDTH * 0.3)
            #self.velocity[1] = np.clip(self.velocity[1], a_min=-self.SCREEN_WIDTH * 0.3,a_max=self.SCREEN_WIDTH * 0.3)
            
            if new_x >= self.SCREEN_WIDTH - 10:
                self.pos[0] = self.SCREEN_WIDTH - 10
                #self.velocity[0] = np.clip(self.velocity[0] + 100, a_min=-self.SCREEN_WIDTH * 3, a_max=self.SCREEN_WIDTH * 3)
                #self.velocity[0] = -self.velocity[0]    #掉头
                self.velocity[0] = -40    #掉头
                self.swim_angle = (self.swim_angle + pi)%(2*pi)   #!掉头之后更改角度
            #elif new_x < self.radius:
            elif new_x < 10:
                self.pos[0] = 10    #如果智能体坐标小于半径，即碰到左壁
                #self.velocity[0] = np.clip(self.velocity[0] - 100, a_min=-self.SCREEN_WIDTH * 3, a_max=self.SCREEN_WIDTH * 3)
                #self.velocity[0] = -self.velocity[0]    #掉头
                self.velocity[0] = 40    #掉头
                self.swim_angle = (self.swim_angle + pi)%(2*pi)    #!掉头之后更改角度
            else:
                self.pos[0] = new_x
                #self.velocity[0] = self.velocity[0]
            
            
            
            
        self.rect.center = (self.pos[0], self.pos[1])
        
        #if 

#灰色
class Counter(Agent):
    #def __init__(self, id, radius, color, speed, screen_width, screen_height, walls, type):
        #Agent.__init__(self, id, radius, speed, screen_width, screen_height, walls, type)
    def __init__(self, id, radius, color, speed, screen_width, screen_height, blood, swim_angle, type):
        #flag量有swim_angle游泳方向, scan扫描, cannnon射击，last_dir上次位置，这三个要用函数表示，同时添加角度变量
        #删掉swim，让它处于运动中，每次都要计算xy方向上的分速度
        Agent.__init__(self, id, radius, speed, screen_width, screen_height, blood, swim_angle, type)
        image = pygame.Surface([radius * 2, radius * 2])    #绘制半径^2 半径^2的图像
        image.set_colorkey((0, 0, 0))
        pygame.draw.circle(
            image,
            color,
            (radius, radius),
            radius,
            0
        )
        self.image = image.convert()
        self.rect = self.image.get_rect()
        #self.speed = speed
        self.last_dir = 0
        self.swim_angle = swim_angle
        
    def update(self, dt):
        sin_swim_angle = sin(self.swim_angle)
        cos_swim_angle = cos(self.swim_angle)
        self.velocity[0] = np.clip(self.speed * cos_swim_angle, a_min=0, a_max= 100)
        self.velocity[1] = np.clip(self.speed * sin_swim_angle, a_min=0, a_max= 100)
        new_x = self.pos[0] + self.velocity[0] * dt
        new_y = self.pos[1] + self.velocity[1] * dt

        flag = True
        self.last_dir = 0

        if flag:
            #防止撞墙
            if new_x >= self.SCREEN_WIDTH - 10:
                self.pos[0] = self.SCREEN_WIDTH - 10
                self.velocity[0] = -self.velocity[0]    #掉头
                self.swim_angle = (self.swim_angle + pi)%(2*pi)   #!掉头之后更改角度
            #elif new_x < self.radius:
            elif new_x < 10:
                self.pos[0] = 10    #如果智能体坐标小于半径，即碰到左壁
                self.velocity[0] = -self.velocity[0]    #掉头
                self.swim_angle = (self.swim_angle + pi)%(2*pi)    #!掉头之后更改角度
            else:
                self.pos[0] = new_x
                
            '''
            if new_y >= self.SCREEN_HEIGHT - 10:
                self.pos[1] = self.SCREEN_HEIGHT - 10
                self.velocity[0] = 0.0
                self.velocity[1] = 0.0
                self.blood = self.blood - self.speed * 0.03    #血减速度*0.03
            elif new_y < 10:
                self.pos[1] = 10
                self.velocity[0] = 0.0
                self.velocity[1] = 0.0    #xy速度都为0
                self.blood = self.blood - self.speed * 0.03    #血减速度*0.03
            else:
                self.pos[1] = new_y
            '''
            
            #在40-60范围游
            if self.last_dir == 0:
                self.last_dir = 1
                if new_y > 60:
                    self.swim_angle = -(pi/2)
                    self.pos[1] = new_y
                elif new_y < 40:
                    self.swim_angle = pi/2
                    self.pos[1] = new_y
                else:
                    self.pos[1] = new_y
            else:
                self.last_dir = 0
                if new_x > 60:
                    self.swim_angle = pi
                    self.pos[0] = new_x
                elif new_x < 40:
                    self.swim_angle = 0
                    self.pos[0] = new_x
                else:
                    self.pos[0] = new_x

        self.rect.center = (self.pos[0], self.pos[1])

#未完全编好
class Sniper(Agent):
    #def __init__(self, id, radius, color, speed, screen_width, screen_height, walls, type):
        #Agent.__init__(self, id, radius, speed, screen_width, screen_height, walls, type)
    def __init__(self, id, radius, color, speed, screen_width, screen_height, blood, swim_angle, type):
        #flag量有swim_angle游泳方向, scan扫描, cannnon射击，last_dir上次位置，这三个要用函数表示，同时添加角度变量
        #删掉swim，让它处于运动中，每次都要计算xy方向上的分速度
        Agent.__init__(self, id, radius, speed, screen_width, screen_height, blood, swim_angle,type)
        image = pygame.Surface([radius * 2, radius * 2])    #绘制半径^2 半径^2的图像
        image.set_colorkey((0, 0, 0))
        pygame.draw.circle(
            image,
            color,
            (radius, radius),
            radius,
            0
        )
        self.image = image.convert()
        self.rect = self.image.get_rect()
        self.speed = 100
        
    def update(self, dt):
        sin_swim_angle = sin(self.swim_angle)
        cos_swim_angle = cos(self.swim_angle)
        self.velocity[0] = np.clip(self.speed * cos_swim_angle, a_min=0, a_max= 100)
        self.velocity[1] = np.clip(self.speed * sin_swim_angle, a_min=0, a_max= 100)
        new_x = self.pos[0] + self.velocity[0] * dt
        new_y = self.pos[1] + self.velocity[1] * dt

        flag = True
        '''
        #！此处要考虑flag为真假时的区别，wall和screen的区别？？
        for wall in self.walls:
            #如果 墙_左<new_x<墙_右,new_y出界的状态，y坐标为边界加减半径，速度变为相反方向速度（应该是）
            if wall.rect.left < new_x < wall.rect.right:
                if wall.rect.top < new_y - self.radius < wall.rect.bottom:
                    self.pos[1] = wall.rect.bottom + self.radius
                    self.velocity[1] = -self.velocity[1]
                    flag = False
                elif wall.rect.top < new_y + self.radius < wall.rect.bottom:
                    self.pos[1] = wall.rect.top - self.radius
                    self.velocity[1] = -self.velocity[1]
                    flag = False
            #如果 墙_top<new_y<墙_bottom,new_x出界的状态，x坐标为边界加减半径，速度变为相反方向速度（应该是）
            if wall.rect.top < new_y < wall.rect.bottom:
                if wall.rect.left < new_x - self.radius < wall.rect.right:
                    self.pos[0] = wall.rect.right + self.radius
                    self.velocity[0] = -self.velocity[0]
                    flag = False
                elif wall.rect.left < new_x + self.radius < wall.rect.right:
                    self.pos[0] = wall.rect.left - self.radius
                    self.velocity[0] = -self.velocity[0]
                    flag = False
        '''

        if flag:
            #在40-60范围游
            if self.last_dir == 0:
                self.last_dir = 1
                if new_y > 60:
                    self.swim_angle = 270
                    self.pos[1] = new_y
                elif new_y < 40:
                    self.swim_angle = 90
                    self.pos[1] = new_y
                else:
                    self.pos[1] = new_y
            else:
                self.last_dir = 0
                if new_x > 60:
                    self.swim_angle = 180
                    self.pos[0] = new_x
                elif new_x < 40:
                    self.swim_angle = 0
                    self.pos[0] = new_x
                else:
                    self.pos[0] = new_x

        self.rect.center = (self.pos[0], self.pos[1])


class OPlayer(Agent):
    #def __init__(self, id, radius, color, speed, screen_width, screen_height, walls, type):
        #Agent.__init__(self, id, radius, speed, screen_width, screen_height, walls, type)
    def __init__(self, id, radius, color, speed, screen_width, screen_height, blood, swim_angle, type):
        #flag量有swim_angle游泳方向, scan扫描, cannnon射击，这三个要用函数表示，同时添加角度变量
        #删掉swim，让它处于运动中，每次都要计算xy方向上的分速度
        Agent.__init__(self, id, radius, speed, screen_width, screen_height, blood, swim_angle, type)

        #self.out_radius = radius * 8    #！半径需要修改
        self.radius = radius    #！半径需要修改
        self.out_radius = 70    #！半径需要修改
        self.speed = speed
        #self.range = radius * 5    #!原代码中有一句距离小于hunter.range - prey.radius，即捕获
        self.blood = blood
        image = pygame.Surface([self.radius * 2, self.radius * 2])
        image.set_colorkey((0, 0, 0))
        image.set_alpha(int(255 * 0.75))

        pygame.draw.circle(
            image,
            color,
            (self.radius, self.radius),
            radius,
            0
        )
        #self.dx = 0
        #self.dy = 0
        #self.accelerate = True
        #self.swim = True
        self.swim_angle = swim_angle
        #self.scan = True
        #self.scan_angle = 0   #先单独定义游泳方向
        #self.cannon = True
        #self.cannon_angle = 0
        #游泳，瞄准，射击都定义为真
        self.image = image.convert()
        self.rect = self.image.get_rect()
        
    def update(self, dt):
        
        '''
        #加速情况，x方向速度为当前x方向速度+dx，大小在±screen_width*0.3之间
        if self.accelerate:
            self.velocity[0] = np.clip(self.velocity[0] + self.dx, a_min=-self.SCREEN_WIDTH * 0.3,
                                       a_max=self.SCREEN_WIDTH * 0.3)
            self.velocity[1] = np.clip(self.velocity[1] + self.dy, a_min=-self.SCREEN_WIDTH * 0.3,
                                       a_max=self.SCREEN_WIDTH * 0.3)
            self.accelerate = False
            #加速的话设置accelerate flag为false
            
        if self.swim:
            sin_swim_angle = sin(swim_angle)
            cos_swim_angle = cos(swim_angle)
            #计算分速度
            self.velocity[0] = np.clip(self.velocity[0] * cos_swim_angle, a_min=0, a_max= 100)
            self.velocity[1] = np.clip(self.velocity[1] * sin_swim_angle, a_min=0, a_max= 100)
            self.accelerate = False
            #加速的话设置accelerate flag为false
        '''


        # print self.velocity[0]
        sin_swim_angle = sin(self.swim_angle)
        cos_swim_angle = cos(self.swim_angle)
        self.velocity[0] = np.clip(self.speed * cos_swim_angle, a_min=0, a_max= 100)
        self.velocity[1] = np.clip(self.speed * sin_swim_angle, a_min=0, a_max= 100)
        new_x = self.pos[0] + self.velocity[0] * dt
        new_y = self.pos[1] + self.velocity[1] * dt

        flag = True


        '''
        for wall in self.walls:
            #如果 墙_左<new_x<墙_右,new_y出界的状态，y坐标为边界加减半径，速度变为0（应该是）
            if wall.rect.left < new_x < wall.rect.right:
                if wall.rect.top < new_y - self.radius < wall.rect.bottom:
                    self.pos[1] = wall.rect.bottom + self.radius
                    self.velocity[1] = 0.0
                    flag = False
                elif wall.rect.top < new_y + self.radius < wall.rect.bottom:
                    self.pos[1] = wall.rect.top - self.radius
                    self.velocity[1] = 0.0
                    flag = False
            #如果 墙_top<new_y<墙_bottom,new_x出界的状态，x坐标为边界加减半径，速度变为0（应该是）
            if wall.rect.top < new_y < wall.rect.bottom:
                if wall.rect.left < new_x - self.radius < wall.rect.right:
                    self.pos[0] = wall.rect.right + self.radius
                    self.velocity[0] = 0.0
                    flag = False
                elif wall.rect.left < new_x + self.radius < wall.rect.right:
                    self.pos[0] = wall.rect.left - self.radius
                    self.velocity[0] = 0.0
                    flag = False
        '''


        if flag:
        #如果碰到screen边，位置为边界-半径，速度为0

            '''
            if new_x >= self.SCREEN_WIDTH - self.radius:
                self.pos[0] = self.SCREEN_WIDTH - self.radius
                self.velocity[0] = 0.0
                self.velocity[1] = 0.0    #xy速度都为0
                self.blood = self.blood - self.speed * 0.03    #血减速度0.03
            elif new_x < self.radius:
                self.pos[0] = self.radius    #如果智能体坐标小于半径，即碰到左壁
                self.velocity[0] = 0.0
                self.velocity[1] = 0.0    #xy速度都为0
                self.blood = self.blood - self.speed * 0.03    #血减速度*0.03
            else:
                self.pos[0] = new_x
                #self.velocity[0] *= 0.975    x方向速度应该是不变的

            if new_y >= self.SCREEN_HEIGHT - self.radius:
                self.pos[1] = self.SCREEN_HEIGHT - self.radius
                self.velocity[0] = 0.0
                self.velocity[1] = 0.0
                self.blood = self.blood - self.speed * 0.03    #血减速度*0.03
            elif new_y < self.radius:
                self.pos[1] = self.radius
                self.velocity[0] = 0.0
                self.velocity[1] = 0.0    #xy速度都为0
                self.blood = self.blood - self.speed * 0.03    #血减速度*0.03
            else:
                self.pos[1] = new_y
                #self.velocity[1] *= 0.975
             '''
             
            if new_x >= self.SCREEN_WIDTH - 10:
                self.pos[0] = self.SCREEN_WIDTH - 10
                #self.velocity[0] = 0.0
                #self.velocity[1] = 0.0    #xy速度都为0
                self.blood = self.blood - self.speed * 0.03    #血减速度0.03
            elif new_x < 10:
                self.pos[0] = 10    #如果智能体坐标小于半径，即碰到左壁
                #self.velocity[0] = 0.0
                #self.velocity[1] = 0.0    #xy速度都为0
                self.blood = self.blood - self.speed * 0.03    #血减速度*0.03
            else:
                self.pos[0] = new_x
                #self.speed = 100    #!增加了速度
                #self.velocity[0] *= 0.975    x方向速度应该是不变的

            if new_y >= self.SCREEN_HEIGHT - 10:
                self.pos[1] = self.SCREEN_HEIGHT - 10
                #self.velocity[0] = 0.0
                #self.velocity[1] = 0.0
                self.blood = self.blood - self.speed * 0.03    #血减速度*0.03
            elif new_y < 10:
                self.pos[1] = 10
                #self.velocity[0] = 0.0
                #self.velocity[1] = 0.0    #xy速度都为0
                self.blood = self.blood - self.speed * 0.03    #血减速度*0.03
            else:
                self.pos[1] = new_y
                #self.velocity[1] *= 0.975
            
        self.rect.center = (self.pos[0], self.pos[1])

#蓝色
class Player(PAgent):
    #def __init__(self, id, radius, color, speed, screen_width, screen_height, walls, type):
        #Agent.__init__(self, id, radius, speed, screen_width, screen_height, walls, type)
    def __init__(self, id, radius, color, speed, screen_width, screen_height, blood, type):
        #flag量有swim_angle游泳方向, scan扫描, cannnon射击，这三个要用函数表示，同时添加角度变量
        #删掉swim，让它处于运动中，每次都要计算xy方向上的分速度
        PAgent.__init__(self, id, radius, speed, screen_width, screen_height, blood, type)

        #self.out_radius = radius * 8    #！半径需要修改
        self.radius = radius    #！半径需要修改
        self.out_radius = 70    #！半径需要修改
        self.speed = speed
        #self.range = radius * 5    #!原代码中有一句距离小于hunter.range - prey.radius，即捕获
        self.blood = blood
        image = pygame.Surface([self.radius * 2, self.radius * 2])
        image.set_colorkey((0, 0, 0))
        image.set_alpha(int(255 * 0.75))

        pygame.draw.circle(
            image,
            color,
            (self.radius, self.radius),
            radius,
            0
        )
        self.dx = 0
        self.dy = 0
        self.accelerate = True
        #self.swim = True
        #self.swim_angle = swim_angle
        #self.scan = True
        #self.scan_angle = 0   #先单独定义游泳方向
        #self.cannon = True
        #self.cannon_angle = 0
        #游泳，瞄准，射击都定义为真
        self.image = image.convert()
        self.rect = self.image.get_rect()
        
    def update(self, dt):
        # print self.velocity[0]
        if self.accelerate:
            self.velocity[0] = np.clip(self.velocity[0] + self.dx, a_min=-self.SCREEN_WIDTH * 0.3,
                                       a_max=self.SCREEN_WIDTH * 0.3)
            self.velocity[1] = np.clip(self.velocity[1] + self.dy, a_min=-self.SCREEN_WIDTH * 0.3,
                                       a_max=self.SCREEN_WIDTH * 0.3)
            self.accelerate = False
            #加速的话设置accelerate flag为false
        
        #sin_swim_angle = sin(self.swim_angle)
        #cos_swim_angle = cos(self.swim_angle)
        #self.velocity[0] = np.clip(self.speed * cos_swim_angle, a_min=0, a_max= 100)
        #self.velocity[1] = np.clip(self.speed * sin_swim_angle, a_min=0, a_max= 100)
        new_x = self.pos[0] + self.velocity[0] * dt
        new_y = self.pos[1] + self.velocity[1] * dt

        flag = True

        if flag:
        #如果碰到screen边，位置为边界-半径，速度为0
            if new_x >= self.SCREEN_WIDTH - 10:
                self.pos[0] = self.SCREEN_WIDTH - 10
                #self.velocity[0] = 0.0
                #self.velocity[1] = 0.0    #xy速度都为0
                self.blood = self.blood - self.speed * 0.03    #血减速度0.03
            elif new_x < 10:
                self.pos[0] = 10    #如果智能体坐标小于半径，即碰到左壁
                #self.velocity[0] = 0.0
                #self.velocity[1] = 0.0    #xy速度都为0
                self.blood = self.blood - self.speed * 0.03    #血减速度*0.03
            else:
                self.pos[0] = new_x
                #self.speed = 100    #!增加了速度
                #self.velocity[0] *= 0.975    x方向速度应该是不变的

            if new_y >= self.SCREEN_HEIGHT - 10:
                self.pos[1] = self.SCREEN_HEIGHT - 10
                #self.velocity[0] = 0.0
                #self.velocity[1] = 0.0
                self.blood = self.blood - self.speed * 0.03    #血减速度*0.03
            elif new_y < 10:
                self.pos[1] = 10
                #self.velocity[0] = 0.0
                #self.velocity[1] = 0.0    #xy速度都为0
                self.blood = self.blood - self.speed * 0.03    #血减速度*0.03
            else:
                self.pos[1] = new_y
                #self.velocity[1] *= 0.975
            
        self.rect.center = (self.pos[0], self.pos[1])


'''
class Wall(object):
    def __init__(self, pos, width, height):
        self.rect = pygame.Rect(pos[0], pos[1], width, height)
'''
# -- coding: utf-8 --
from utils import normalization
import pygame
from numpy import random
import numpy as np



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


class Other(Agent):
    def __init__(self, id, radius, color, speed, screen_width, screen_height, walls, type):
        Agent.__init__(self, id, radius, speed, screen_width, screen_height, walls, type)
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


class Hunter(Agent):
    def __init__(self, id, radius, color, speed, screen_width, screen_height, walls, type):
        Agent.__init__(self, id, radius, speed, screen_width, screen_height, walls, type)

        self.out_radius = radius * 8
        self.range = radius * 5
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
        self.image = image.convert()
        self.rect = self.image.get_rect()

    def update(self, dt):
        #加速情况，x方向速度为当前x方向速度+dx，大小在±screen_width*0.3之间
        if self.accelerate:
            self.velocity[0] = np.clip(self.velocity[0] + self.dx, a_min=-self.SCREEN_WIDTH * 0.3,
                                       a_max=self.SCREEN_WIDTH * 0.3)
            self.velocity[1] = np.clip(self.velocity[1] + self.dy, a_min=-self.SCREEN_WIDTH * 0.3,
                                       a_max=self.SCREEN_WIDTH * 0.3)
            self.accelerate = False
            #加速的话设置accelerate flag为false

        # print self.velocity[0]
        new_x = self.pos[0] + self.velocity[0] * dt
        new_y = self.pos[1] + self.velocity[1] * dt

        flag = True
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

        if flag:
        #如果碰到screen边，位置为边界-半径，速度为0
            if new_x >= self.SCREEN_WIDTH - self.radius:
                self.pos[0] = self.SCREEN_WIDTH - self.radius
                self.velocity[0] = 0.0
            elif new_x < self.radius:
                self.pos[0] = self.radius    #！考虑这是啥意思？
                self.velocity[0] = 0.0
            else:
                self.pos[0] = new_x
                self.velocity[0] *= 0.975

            if new_y >= self.SCREEN_HEIGHT - self.radius:
                self.pos[1] = self.SCREEN_HEIGHT - self.radius
                self.velocity[1] = 0.0
            elif new_y < self.radius:
                self.pos[1] = self.radius
                self.velocity[1] = 0.0
            else:
                self.pos[1] = new_y
                self.velocity[1] *= 0.975

        self.rect.center = (self.pos[0], self.pos[1])


class Wall(object):
    def __init__(self, pos, width, height):
        self.rect = pygame.Rect(pos[0], pos[1], width, height)

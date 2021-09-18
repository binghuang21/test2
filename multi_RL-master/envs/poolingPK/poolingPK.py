# -- coding: utf-8 --
from envs.pygamewrapper import PyGameWrapper
from .agent import *
#from envs.pygamewrapper import PyGameWrapper
#from .agent import *
from utils import *
from pygame.constants import *
import pygame
from numpy import random
from math import sqrt, sin, cos
import sys
import random
#from hunter_utils import *
#两点之间的距离
def count_distance_fast(a1, a2, b1, b2):
    return sqrt((a1 - b1) ** 2 + (a2 - b2) ** 2)
    
#两条平行线之间的距离
def line_distance_fast(seg_a_0, seg_a_1, seg_v_unit_0, seg_v_unit_1, seg_v_len,
                       circ_pos_0,
                       circ_pos_1, circ_rad):
    pt_v_0 = circ_pos_0 - seg_a_0
    pt_v_1 = circ_pos_1 - seg_a_1

    proj = pt_v_0 * seg_v_unit_0 + pt_v_1 * seg_v_unit_1
    if proj <= 0 or proj >= seg_v_len:
        return False
    proj_v_0 = seg_v_unit_0 * proj
    proj_v_1 = seg_v_unit_1 * proj

    closest_0 = proj_v_0 + seg_a_0
    closest_1 = proj_v_1 + seg_a_1

    dist_v_0 = circ_pos_0 - closest_0
    dist_v_1 = circ_pos_1 - closest_1

    offset = sqrt(dist_v_0 ** 2 + dist_v_1 ** 2)
    if offset >= circ_rad:
        return False

    le = sqrt(circ_rad ** 2 - offset ** 2)
    re_0 = closest_0 - seg_a_0
    re_1 = closest_1 - seg_a_1

    return sqrt(re_0 ** 2 + re_1 ** 2) - le

'''
#白色，捕食者，猎物，毒素，灰色
COLOR_MAP = {"white": (255, 255, 255),
             "hunter": (0, 0, 255),
             "prey": (20, 255, 20),
             "toxin": (255, 20, 20),
             'grey': (144, 144, 144)}
'''

#white-背景 Player-用户编写的智能体-蓝色 Sniper-拐角扫描攻击型-绿色 Rook-水平移动-红色，四方向扫描 Counter-原地扫描攻击范围内攻击，非攻击范围朝目标方向移动-灰色
COLOR_MAP = {"white": (255, 255, 255),
             "Player": (0, 0, 255),
             "Sniper": (20, 255, 20),
             "Rook": (255, 20, 20),
             'Counter': (144, 144, 144)}


Key_mapping = {
    0: {"up": K_UP, "left": K_LEFT, "right": K_RIGHT, "down": K_DOWN},
    1: {"up": K_1, "left": K_2, "right": K_q, "down": K_w},
    2: {"up": K_3, "left": K_4, "right": K_e, "down": K_r},
    3: {"up": K_5, "left": K_6, "right": K_t, "down": K_y},
    4: {"up": K_7, "left": K_8, "right": K_u, "down": K_i},
    5: {"up": K_9, "left": K_0, "right": K_o, "down": K_p},
    6: {"up": K_a, "left": K_s, "right": K_z, "down": K_x},
    7: {"up": K_d, "left": K_f, "right": K_c, "down": K_v},
    8: {"up": K_g, "left": K_h, "right": K_b, "down": K_n},
    9: {"up": K_j, "left": K_k, "right": K_m, "down": K_COMMA}
}


class PoolingPK(PyGameWrapper):
    #def __init__(self, draw=False, width=48, height=48, num_preys=10, num_hunters=3, num_toxins=10):
    #def __init__(self, draw=False, width=100, height=100, num_sniper=0, num_player=1, num_rook=1, num_counter=1, full_blood=100, agent_angle=random.random()*2*pi):
    def __init__(self, draw=False, width=300, height=300, num_sniper=0, num_player=1, num_rook=1, num_counter=1, full_blood=100):
        #key_mapping作用是什么
        self.actions = {k: Key_mapping[k] for k in sorted(Key_mapping.keys())[:num_player]}

        PyGameWrapper.__init__(self, width, height, actions=self.actions)
        self.draw = draw
        self.BG_COLOR = COLOR_MAP['white']
        self.EYES = 360    #eye是什么

        self.MAX_PLAYER_NUM = num_player
        self.PLAYER_NUM = num_player    #捕食者数量
        self.PLAYER_COLOR = COLOR_MAP['Player']
        #self.PLAYER_SPEED = random.randint(1,100)    #玩家速度(0,100)整数
        self.PLAYER_SPEED = 100    #玩家速度(0,100)整数
        #self.HUNTER_RADIUS = percent_round_int(width, 0.015)    #！这个函数在哪？？？
        self.PLAYER_RADIUS = 10
        self.PLAYER_BLOOD = full_blood    #定义血量
        #self.PLAYER_ANGLE = agent_angle    #定义角度,这里定义什么player就会朝哪个方向走
        #self.PLAYER_ANGLE = random.random() * 2 * pi    #定义角度
        self.players = pygame.sprite.Group()    #pygame.sprite.Group 用于保存和管理多个Sprite对象的容器类
        self.players_dic = {}
        
        self.MAX_COUNTER_NUM = num_counter
        self.COUNTER_NUM = num_counter    #捕食者数量
        self.COUNTER_COLOR = COLOR_MAP['Counter']
        #self.COUNTER_SPEED = random.randint(1,100)    #玩家速度(0,100)整数
        self.COUNTER_SPEED = 100
        #self.HUNTER_RADIUS = percent_round_int(width, 0.015)    #！这个函数在哪？？？
        self.COUNTER_RADIUS = 10
        self.COUNTER_BLOOD = full_blood    #定义血量
        #self.COUNTER_ANGLE = agent_angle    #定义角度
        self.COUNTER_ANGLE = random.random() * 2 * pi    #!都改为random试试
        #self.COUNTER_LASTDIR = 0
        self.counters = pygame.sprite.Group()    #pygame.sprite.Group 用于保存和管理多个Sprite对象的容器类
        self.counters_dic = {}

        self.SNIPER_COLOR = COLOR_MAP['Sniper']
        self.SNIPER_SPEED = 100
        self.SNIPER_NUM = num_sniper
        self.SNIPER_RADIUS = 10    #毒物半径
        self.SNIPER_BLOOD = full_blood    #定义血量
        #self.SNIPER_ANGLE = agent_angle    #定义角度!
        self.SNIPER_ANGLE = random.random() * 2 * pi    #!都改为random试试
        self.snipers = pygame.sprite.Group()
        self.snipers_dic = {}

        self.ROOK_NUM = num_rook
        self.ROOK_COLOR = COLOR_MAP['Rook']
        self.ROOK_SPEED = 100
        self.ROOK_RADIUS = 10
        self.ROOK_BLOOD = full_blood    #定义血量
        #self.ROOK_ANGLE = pi    #定义角度
        self.ROOK_ANGLE = random.random() * 2 * pi    #!都改为random试试
        self.rooks = pygame.sprite.Group()
        #self.walls = None
        self.snipers_num = num_sniper
        self.rooks_num = num_rook
        self.all_entities = None

        self.observation = np.zeros((self.MAX_PLAYER_NUM, self.EYES * (num_player + 3) + 2))    #观测？？？
        self.reward = np.zeros(self.PLAYER_NUM)    #reward为一个和hunter_num形状一样的数组
        self.info = np.zeros((self.PLAYER_NUM, self.PLAYER_NUM), dtype=int)    #info为一个hunter_num*hunter_num形状的数组
        self.info2 = np.zeros((self.PLAYER_NUM, self.PLAYER_NUM), dtype=int)
        self.onehot = self.agent_one_hot(self.PLAYER_NUM)    #hunter_num*hunter_num的单位数组

#agent_num*agent_num的单位数组
    def agent_one_hot(self, agent_num):
        tmp = np.zeros((agent_num, agent_num), dtype=int)
        for i in range(agent_num):
            tmp[i][i] = 1
        return tmp

#随机距离，并保证任意两个智能体间的距离大于他们的半径之和
    def _rand_postion(self, agents):
        pos = []
        for agent in agents:
            pos_x = random.uniform(agent.radius, self.width - agent.radius)    #从一个均匀分布[low,high)中随机采样，注意定义域是左闭右开，即包含low，不包含high
            pos_y = random.uniform(agent.radius, self.height - agent.radius)
            pos.append([pos_x, pos_y])
            #随机从长宽范围内确定位置，注意要减去半径

        for i in range(len(agents)):
            for j in range(i + 1, len(agents)):
                dist = math.sqrt((pos[i][0] - pos[j][0]) ** 2 + (pos[i][1] - pos[j][1]) ** 2)
                #计算两个智能体之间的距离
                while dist <= (agents[i].radius + agents[j].radius):
                #如果两个智能体间的距离小于他们的半径和，重新随机i智能体位置，再次计算两智能体之间距离
                    pos[i][0] = random.uniform(agents[i].radius, self.width - agents[i].radius)
                    pos[i][1] = random.uniform(agents[i].radius, self.height - agents[i].radius)
                    dist = math.sqrt((pos[i][0] - pos[j][0]) ** 2 + (pos[i][1] - pos[j][1]) ** 2)
        return pos

#定义位置？？？
    def _init_postions(self):
        pos_list = [list(self.rng.rand(2, )) for _ in range(50)]
        return [[pos_list[i][0] * self.width, pos_list[i][1] * self.height] for i in range(len(pos_list))]

#定义方向？？？
    def _init_directions(self):
        dir_list = [list(self.rng.rand(2, ) - 0.5) for _ in range(50)]
        return [normalization(dir_list[i]) for i in range(len(dir_list))]

#分数
    def get_score(self):
        return self.score

#游戏结束
    def game_over(self):
        return False


    def init(self):

        self.all_entities = []
        #self.walls = []
        self.rooks.empty()
        self.snipers.empty()
        self.players.empty()
        self.counters.empty()
        self.players_dic = {}
        self.font = pygame.font.SysFont("monospace", 18)

        # self.walls.append(
        #     Wall([self.width * 1 / 10, self.height / 2 - self.HUNTER_RADIUS * 8 / 2], self.width * 8 / 10,
        #          self.HUNTER_RADIUS * 8))

        #self.walls = []
        #定义位置和方向
        self.FIX_DIR = self._init_directions()
        self.FIX_POS = self._init_postions()

        id = 0
        for _ in range(self.PLAYER_NUM):
            '''
            player = Player(id, self.PLAYER_RADIUS, self.PLAYER_COLOR,
                            self.PLAYER_SPEED, self.width, self.height, self.PLAYER_BLOOD, self.PLAYER_ANGLE, type='Player')
            '''
            player = Player(id, self.PLAYER_RADIUS, self.PLAYER_COLOR,
                            self.PLAYER_SPEED, self.width, self.height, self.PLAYER_BLOOD, type='Player')
            player.init_direction((0, 0))    #初始捕食者的方向是(0, 0)
            player.init_positon(self.FIX_POS[id])    #定义每个捕食者的初始位置
            self.players.add(player)    #增加捕食者
            self.players_dic[id] = player    #捕食者方向=hunter？？？
            self.all_entities.append(player)    #？？
            id += 1
        for _ in range(self.COUNTER_NUM):
            counter = Counter(id, self.COUNTER_RADIUS, self.COUNTER_COLOR,
                            self.COUNTER_SPEED, self.width, self.height, self.COUNTER_BLOOD, self.COUNTER_ANGLE, type='Counter')
            counter.init_direction((0, 0))    #初始捕食者的方向是(0, 0)
            #self.COUNTER_LASTDIR = counter.init_direction((0, 0))
            counter.init_positon(self.FIX_POS[id])    #定义每个捕食者的初始位置
            self.counters.add(counter)    #增加捕食者
            self.counters_dic[id] = counter    #捕食者方向=hunter？？？
            self.all_entities.append(counter)    #？？
            id += 1
        for _ in range(self.snipers_num):
            sniper = Sniper(id, self.SNIPER_RADIUS, self.SNIPER_COLOR, self.SNIPER_SPEED,
                         self.width, self.height, self.SNIPER_BLOOD, self.SNIPER_ANGLE, type='Sniper')
            sniper.init_direction(self.FIX_DIR[id])
            sniper.init_positon(self.FIX_POS[id])
            self.sniper.add(sniper)
            self.all_entities.append(sniper)
            id += 1
        for _ in range(self.rooks_num):
            rook = Rook(id, self.ROOK_RADIUS, self.ROOK_COLOR, self.ROOK_SPEED,
                          self.width, self.height, self.ROOK_BLOOD, self.ROOK_ANGLE, type='Rook')
            rook.init_direction(self.FIX_DIR[id])
            rook.init_positon(self.FIX_POS[id])
            # rook.pos[0] = 20
            # rook.pos[1] = 80
            self.rooks.add(rook)
            self.all_entities.append(rook)
            id += 1

#重置位置和方向
    def reset(self):
        for agent in self.all_entities:
            agent.reset_pos()
            agent.reset_orientation()

#游戏触发事件
    def _handle_player_events(self):
        for event in pygame.event.get():
            #暂停
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            #按键触发
            if event.type == pygame.KEYDOWN:
                key = event.key

                for idx, actions in self.actions.iteritems():
                    if self.players_dic.has_key(idx):
                        agent = self.players_dic[idx]

                        #向左移动
                        if key == actions["left"]:
                            agent.dx = -agent.speed
                            agent.dy = 0
                            agent.accelerate = True

                        #向右移动
                        if key == actions["right"]:
                            agent.dx = agent.speed
                            agent.dy = 0
                            agent.accelerate = True

                        #向上移动
                        if key == actions["up"]:
                            agent.dy = -agent.speed
                            agent.dx = 0
                            agent.accelerate = True

                        #向下移动
                        if key == actions["down"]:
                            agent.dy = agent.speed
                            agent.dx = 0
                            agent.accelerate = True

    # @profile
    def step(self, dt):

        self.reward[:] = 0.0
        self.info[:] = 0
        self.info2[:] = 0
        #如果游戏结束了，返回reward
        if self.game_over():
            return self.reward

        dt /= 1000.0    #每次更新经过的dt大小（应该是）
        self.screen.fill(self.BG_COLOR)
        self._handle_player_events()
        
        

        for rook in self.rooks:
            for counter in self.counters:
                #player_pair = []    ！考虑下一行代码他俩不碰撞的情况下应该是大于radius还是大于2倍的radius
                if (count_distance_fast(rook.pos[0], rook.pos[1], counter.pos[0], counter.pos[1]) <= 180) and (count_distance_fast(rook.pos[0], rook.pos[1], counter.pos[0], counter.pos[1]) > 20) and (abs(counter.pos[1]-rook.pos[1]) <= 2 or abs(counter.pos[0]-rook.pos[0]) <= 2):
                    self.COUNTER_BLOOD -= 10
                    dis = count_distance_fast(rook.pos[0], rook.pos[1], counter.pos[0], counter.pos[1])
                    self.draw_line(rook.rect.center, 1, 0, rook, dis, COLOR_MAP["Counter"])
                    self.draw_line(rook.rect.center, 0, 1, rook, dis, COLOR_MAP["Counter"])
                    self.draw_line(rook.rect.center, -1, 0, rook, dis, COLOR_MAP["Counter"])
                    self.draw_line(rook.rect.center, 0, -1, rook, dis, COLOR_MAP["Counter"])
                    #self.reward[player.id] += self.rewards["positive"]
                elif count_distance_fast(rook.pos[0], rook.pos[1], counter.pos[0], counter.pos[1]) <= 20:
                    self.COUNTER_BLOOD -= (self.COUNTER_SPEED-self.ROOK_SPEED)*0.03
                    self.ROOK_BLOOD -= (self.COUNTER_SPEED-self.ROOK_SPEED)*0.03
                    #self.reward[player.id] += self.rewards["positive"]
            for player in self.players:
                if count_distance_fast(rook.pos[0], rook.pos[1], player.pos[0], player.pos[1]) <= 180 and (count_distance_fast(rook.pos[0], rook.pos[1], player.pos[0], player.pos[1]) > 20) and (abs(player.pos[1]-rook.pos[1]) <= 2 or abs(player.pos[0]-rook.pos[0]) <= 2):
                    self.PLAYER_BLOOD -= 10
                    dis = count_distance_fast(rook.pos[0], rook.pos[1], player.pos[0], player.pos[1])
                    self.reward[player.id] += self.rewards["negative"]
                    self.draw_line(rook.rect.center, 1, 0, rook, dis, COLOR_MAP["Player"])
                    self.draw_line(rook.rect.center, 0, 1, rook, dis, COLOR_MAP["Player"])
                    self.draw_line(rook.rect.center, -1, 0, rook, dis, COLOR_MAP["Player"])
                    self.draw_line(rook.rect.center, 0, -1, rook, dis, COLOR_MAP["Player"])
                elif count_distance_fast(rook.pos[0], rook.pos[1], player.pos[0], player.pos[1]) <= 20:
                    self.PLAYER_BLOOD -= abs(self.PLAYER_SPEED - self.ROOK_SPEED)*0.03
                    self.ROOK_BLOOD -= abs(self.COUNTER_SPEED - self.ROOK_SPEED)*0.03
                    self.reward[player.id] += self.rewards["negative"]
            #rook.rand_orientation()
            #rook.rand_pos()
                    #捕食者和猎物间的距离小于捕食者半径-猎物半径，增加捕食对
                    #扫描到即射到
            '''
            if rook.pos[0] >= self.width - 12:
                rook.velocity[0] = -rook.velocity[0]    #掉头
                rook.swim_angle = (rook.swim_angle + pi)%(2*pi)   #!掉头之后更改角度
            #elif new_x < self.radius:
            elif rook.pos[0] < 12:
                rook.pos[0] = 12    #如果智能体坐标小于半径，即碰到左壁
                rook.velocity[0] = -rook.velocity[0]    #掉头
                rook.swim_angle = (rook.swim_angle + pi)%(2*pi)    #!掉头之后更改角度
            #else:
                #rook.pos[0] = new_x
            
            #如果不在y=50处，朝y=50处游
            if rook.pos[1] >= 251:
                #self.velocity[0] = 0
                rook.swim_angle = pi + pi/2
                rook.pos[1] = new_y
            elif rook.pos[1] < 249:
                #self.velocity[0] = 0
                self.swim_angle = pi/2
                self.pos[1] = new_y
            else:
                self.pos[1] = 50
            '''
                    

            '''
                
                if count_distance_fast(prey.pos[0], prey.pos[1], hunter.pos[0], hunter.pos[1]) <= (hunter.range - prey.radius):
                    hunter_pair.append(hunter.id)
            if len(hunter_pair) >= 2:
                for hunter_id in hunter_pair:
                    #如果dx,dy不变则继续
                    if self.hunters_dic[hunter_id].dx == 0 and self.hunters_dic[hunter_id].dy == 0: continue
                    #正反馈
                    self.reward[hunter_id] += self.rewards["positive"]

                #更新在捕食对中的捕食者的信息
                for id in hunter_pair:
                    for other_id in hunter_pair:
                        if id == other_id: continue
                        self.info[id][other_id] += 1

                # self.hungrey += self.rewards["positive"]
                #随机猎物方向和位置
                prey.rand_orientation()
                prey.rand_pos()

        for player in self.players:
            for rook in self.rooks:
            #如果捕食者和毒物之间的距离小于它们的半径和，随机毒物方向和位置并负反馈
                if count_distance_fast(.pos[0], toxin.pos[1], hunter.pos[0], hunter.pos[1]) < (hunter.radius + toxin.radius):
                    # self.lives -= 1
                    toxin.rand_orientation()
                    toxin.rand_pos()
                    self.reward[hunter.id] += self.rewards["negative"]
        '''
        #!大小写和math修改
        for player in self.players:
            #player_pair = []
            for counter in self.counters:
                if (count_distance_fast(player.pos[0], player.pos[1], counter.pos[0], counter.pos[1]) <= 130) and (count_distance_fast(player.pos[0], player.pos[1], counter.pos[0], counter.pos[1]) > 10):
                    self.COUNTER_BLOOD -= 10
                    self.reward[player.id] += self.rewards["positive"]
                elif count_distance_fast(player.pos[0], player.pos[1], counter.pos[0], counter.pos[1]) > 130 and (count_distance_fast(player.pos[0], player.pos[1], counter.pos[0], counter.pos[1]) <= 150):
                    self.reward[player.id] += self.rewards["positive"]
                elif count_distance_fast(player.pos[0], player.pos[1], counter.pos[0], counter.pos[1]) <= 10:
                    self.PLAYER_BLOOD -= abs(self.PLAYER_SPEED - self.COUNTER_SPEED)*0.03
                    self.COUNTER_BLOOD -= abs(self.PLAYER_SPEED - self.COUNTER_SPEED)*0.03
                    self.reward[player.id] += self.rewards["negative"]
                #counter.rand_orientation()
                #counter.rand_pos()
            for rook in self.rooks:
                if (count_distance_fast(player.pos[0], player.pos[1], rook.pos[0], rook.pos[1]) <= 130) and (count_distance_fast(player.pos[0], player.pos[1], rook.pos[0], rook.pos[1]) > 20):
                    self.ROOK_BLOOD -= 10
                    self.reward[player.id] += self.rewards["positive"]
                    if self.ROOK_BLOOD <= 0:
                        self.reward[player.id] += self.rewards["win"]
                        self.rooks.remove(rook)
                        self.ROOK_NUM = 0
                #elif count_distance_fast(player.pos[0], player.pos[1], rook.pos[0], rook.pos[1]) > 150 and count_distance_fast(player.pos[0], player.pos[1], rook.pos[0], rook.pos[1]) <= 180:
                    #self.reward[player.id] += self.rewards["positive"]
                elif count_distance_fast(player.pos[0], player.pos[1], rook.pos[0], rook.pos[1]) <= 20:
                    self.PLAYER_BLOOD -= (self.PLAYER_SPEED-self.ROOK_SPEED)*0.03
                    self.ROOK_BLOOD -= (self.PLAYER_SPEED-self.ROOK_SPEED)*0.03
                    self.reward[player.id] += self.rewards["negative"]
                #rook.rand_orientation()
                #rook.rand_pos()
            

        #更新
        self.players.update(dt)
        self.snipers.update(dt)
        self.rooks.update(dt)
        self.counters.update(dt)

        #画图
        if self.draw:
            self.players.draw(self.screen)
            self.snipers.draw(self.screen)
            self.rooks.draw(self.screen)
            self.counters.draw(self.screen)

            for idx in range(self.PLAYER_NUM):
                label = self.font.render(str(idx), 1, (0, 0, 0))
                self.screen.blit(label,
                                 (self.players_dic[idx].rect.center[0] + 5, self.players_dic[idx].rect.center[1] + 5))
            '''
            for wall in self.walls:
                pygame.draw.rect(self.screen, COLOR_MAP['grey'], wall.rect)
            '''
            self.get_game_state()
            
        return self.reward, self.info

    # @profile
    def get_game_state(self):
        self.observation[:] = 0
        self.info2[:] = 0
        for i in range(self.PLAYER_NUM):
            player = self.players_dic[i]
            other_agents = []
            for j in range(len(self.all_entities)):
                agent = self.all_entities[j]
                if agent is player: continue
                else:
                    other_agents.append(agent)
                #如果捕食者和非捕食者的智能体间的距离小于他们的半径和，在other_agents.append中记录
                #if count_distance_fast(agent.pos[0], agent.pos[1], hunter.pos[0], hunter.pos[1]) <= agent.radius + hunter.out_radius:
                    #other_agents.append(agent)
            ob = self.observe1(player, other_agents)
            #存储每个捕食者的相对速度
            state = np.append(ob, [player.velocity[0] / self.width, player.velocity[1] / self.height])
            self.observation[i] = state[:]
        assert self.observation.shape == (self.MAX_PLAYER_NUM, self.EYES * (self.MAX_PLAYER_NUM + 3) + 2)
        '''
        #增加了对于rook来说的other_agents
        for i in range(self.ROOK_NUM):
            #player = self.players_dic[i]
            rook_other_agents = []
            for j in range(len(self.all_entities)):
                agent = self.all_entities[j]
                if agent is rook: continue
                else:
                    rook_other_agents.append(agent)
        '''
        #assert self.observation.shape == (self.MAX_PLAYER_NUM, self.MAX_PLAYER_NUM)
        return self.observation

    # @profile
    def observe1(self, player, others):
        center = list(player.rect.center)
        out_radius = player.out_radius - player.radius
        observation = np.zeros((self.EYES, 3 + self.MAX_PLAYER_NUM))
        angle = 2 * np.pi / self.EYES    #eye是什么
        other_agents = others[:]
        #rook_other_agents =
        for i in range(0, self.EYES):    #eye可能是一个角度
            sin_angle = sin(angle * i)
            cos_angle = cos(angle * i)
            #dis_to_wall = abs(player.pos[1] - player.radius)
            #self.draw_line(center, sin_angle, cos_angle, player, dis_to_wall, COLOR_MAP["Counter"])
            '''
            if i == 0:
                dis_to_wall = abs(hunter.pos[1] - hunter.radius)    #捕食者与墙的距离
                if dis_to_wall < out_radius:
                    observation[i][0] = 1 - dis_to_wall / out_radius
                    self.draw_line(center, sin_angle, cos_angle, hunter, dis_to_wall, COLOR_MAP["grey"])
                else:
                    for wall in self.walls:
                        if wall.rect.left <= hunter.pos[0] <= wall.rect.right:
                            dis_to_wall = abs(hunter.pos[1] - hunter.radius - wall.rect.bottom)
                            if dis_to_wall < out_radius:
                                observation[i][0] = 1 - dis_to_wall / out_radius
                                self.draw_line(center, sin_angle, cos_angle, hunter, dis_to_wall, COLOR_MAP["grey"])
            elif i == 6:
                dis_to_wall = abs(hunter.pos[0] + hunter.radius - self.width)
                if dis_to_wall < out_radius:
                    observation[i][0] = 1 - dis_to_wall / out_radius
                    self.draw_line(center, sin_angle, cos_angle, hunter, dis_to_wall, COLOR_MAP["grey"])
                else:
                    for wall in self.walls:
                        if wall.rect.top <= hunter.pos[1] <= wall.rect.bottom:
                            dis_to_wall = abs(hunter.pos[0] + hunter.radius - wall.rect.left)
                            if dis_to_wall < out_radius:
                                observation[i][0] = 1 - dis_to_wall / out_radius
                                self.draw_line(center, sin_angle, cos_angle, hunter, dis_to_wall, COLOR_MAP["grey"])

            elif i == 12:
                dis_to_wall = abs(hunter.pos[1] + hunter.radius - self.height)
                if dis_to_wall < out_radius:
                    observation[i][0] = 1 - dis_to_wall / out_radius
                    self.draw_line(center, sin_angle, cos_angle, hunter, dis_to_wall, COLOR_MAP["grey"])
                else:
                    for wall in self.walls:
                        if wall.rect.left <= hunter.pos[0] <= wall.rect.right:
                            dis_to_wall = abs(hunter.pos[1] + hunter.radius - wall.rect.top)
                            if dis_to_wall < out_radius:
                                observation[i][0] = 1 - dis_to_wall / out_radius
                                self.draw_line(center, sin_angle, cos_angle, hunter, dis_to_wall, COLOR_MAP["grey"])
            elif i == 18:
                dis_to_wall = abs(hunter.pos[0] - hunter.radius)
                if dis_to_wall < out_radius:
                    observation[i][0] = 1 - dis_to_wall / out_radius
                    self.draw_line(center, sin_angle, cos_angle, hunter, dis_to_wall, COLOR_MAP["grey"])
                else:
                    for wall in self.walls:
                        if wall.rect.top <= hunter.pos[1] <= wall.rect.bottom:
                            dis_to_wall = abs(hunter.pos[0] - hunter.radius - wall.rect.right)
                            if dis_to_wall < out_radius:
                                observation[i][0] = 1 - dis_to_wall / out_radius
                                self.draw_line(center, sin_angle, cos_angle, hunter, dis_to_wall, COLOR_MAP["grey"])
            '''
            for agent in other_agents:
                dis = line_distance_fast(center[0], center[1], sin_angle, -cos_angle, player.out_radius,
                                         agent.rect.center[0], agent.rect.center[1], agent.radius)
                # dis = self.line_distance1(center, [sin_angle, -cos_angle], hunter.out_radius, agent.rect.center, agent.radius)
                #记录两个不同类智能体间的信息？？？
                if dis is not False:
                    dis = max(dis - player.radius, 0)
                    assert 0 <= dis <= out_radius, str(dis)
                    if agent.type == 'Sniper':
                        observation[i][1] = 1.0 - dis / out_radius
                        self.draw_line(center, sin_angle, cos_angle, player, dis, COLOR_MAP["Sniper"])
                    elif agent.type == 'Rook':
                        observation[i][2] = 1.0 - dis / out_radius
                        self.draw_line(center, sin_angle, cos_angle, player, dis, COLOR_MAP["Rook"])
                    elif agent.type == 'Player':
                        self.info2[player.id][agent.id] += 1
                        observation[i][3 + agent.id] = 1.0 - dis / out_radius
                        self.draw_line(center, sin_angle, cos_angle, player, dis, COLOR_MAP["Player"])
                    break
                    
            '''
            for agent in rook_other_agents:
                dis = line_distance_fast(center[0], center[1], 1, 0, 70,
                                         agent.rect.center[0], agent.rect.center[1], agent.radius)
                # dis = self.line_distance1(center, [sin_angle, -cos_angle], hunter.out_radius, agent.rect.center, agent.radius)
                #记录两个不同类智能体间的信息？？？
                if dis is not False:
                    dis = max(dis - rook.radius, 0)
                    assert 0 <= dis <= 70, str(dis)
                    if agent.type == 'Counter':
                        observation[i][1] = 1.0 - dis / 70
                        self.draw_line(center, 1, 0, rook, dis, COLOR_MAP["Counter"])
                    elif agent.type == 'Player':
                        observation[i][2] = 1.0 - dis / out_radius
                        self.draw_line(center, 1, 0, rook, dis, COLOR_MAP["Player"])
                    break
            '''

        return observation

    def draw_line(self, center, sin_angle, cos_angle, player, line, color):
        if self.draw:
            start_pos = [center[0] + sin_angle * player.radius, center[1] - cos_angle * player.radius]
            end_pos = [0, 0]
            end_pos[0] = start_pos[0] + int(sin_angle * line)
            end_pos[1] = start_pos[1] - int(cos_angle * line)
            pygame.draw.line(self.screen, color, start_pos, end_pos, 1)

    # http://doswa.com/2009/07/13/circle-segment-intersectioncollision.html
    def line_distance1(self, seg_a, seg_v_unit, seg_v_len, circ_pos, circ_rad):
        pt_v = [circ_pos[0] - seg_a[0], circ_pos[1] - seg_a[1]]
        proj = pt_v[0] * seg_v_unit[0] + pt_v[1] * seg_v_unit[1]
        if proj <= 0 or proj >= seg_v_len:
            return False
        proj_v = [seg_v_unit[0] * proj, seg_v_unit[1] * proj]
        closest = [int(proj_v[0] + seg_a[0]), int(proj_v[1] + seg_a[1])]
        dist_v = [circ_pos[0] - closest[0], circ_pos[1] - closest[1]]
        offset = sqrt(dist_v[0] ** 2 + dist_v[1] ** 2)
        if offset >= circ_rad:
            return False
        le = sqrt(circ_rad ** 2 - int(offset) ** 2)
        re = [closest[0] - seg_a[0], closest[1] - seg_a[1]]
        # if sqrt(re[0] ** 2 + re[1] ** 2) - le < 0:
        #     a = 1
        #     print a

        return sqrt(re[0] ** 2 + re[1] ** 2) - le


if __name__ == "__main__":
    import numpy as np
    import time

    pygame.init()
    #game = HunterWorld(width=512, height=480, num_preys=20, num_hunters=5, draw=True)
    #game = PoolingPK(width=100, height=100, num_sniper=0, num_player=1, num_rook=1, num_counter=1, full_blood=100, agent_angle=random.random()*2*pi, draw=True)
    game = PoolingPK(width=300, height=300, num_sniper=0, num_player=1, num_rook=1, num_counter=1, full_blood=100, draw=True)
    #！把agent_angle=0改为agent_angle了
    game.screen = pygame.display.set_mode(game.get_screen_dims(), 0, 32)
    game.clock = pygame.time.Clock()
    game.rng = np.random.RandomState(24)
    game.init()
    game.reset()

    while True:
        start = time.time()
        dt = game.clock.tick_busy_loop(30)
        if game.game_over():
            game.init()
        reward = game.step(dt)
        pygame.display.update()
        end = time.time()
        game.get_game_state()

        # print game.cooperative
        print (1 / (end - start))
        # if v3-v0.01.getScore() > 0:
        # print "Score: {:0.3f} ".format(v3-v0.01.getScore())

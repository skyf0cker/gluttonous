# -*- coding: utf-8 -*-
import math
import random
import cocos
from cocos.sprite import Sprite
import numpy as np
import define
from dot import Dot


class Snake(cocos.cocosnode.CocosNode):
    def __init__(self, is_enemy=False):
        super(Snake, self).__init__()
        self.threhold = 200
        self.hunger = 1000
        self.alive = 1000
        self.is_dead = False
        self.angle = random.randrange(360)  # 目前角度
        self.angle_dest = self.angle  # 目标角度
        self.color = random.choice(define.ALL_COLOR)
        if is_enemy:
            self.position = random.randrange(300, 1300), random.randrange(200, 600)
            if 600 < self.x < 1000:
                self.x += 400
        else:
            self.position = random.randrange(700, 900), random.randrange(350, 450)
        self.is_enemy = is_enemy
        self.head = Sprite('circle.png', color=self.color)
        self.scale = 1.5
        eye = Sprite('circle.png')
        eye.y = 5
        eye.scale = 0.5
        eyeball = Sprite('circle.png', color=define.BLACK)
        eyeball.scale = 0.5
        eye.add(eyeball)
        self.head.add(eye)
        eye = Sprite('circle.png')
        eye.y = -5
        eye.scale = 0.5
        eyeball = Sprite('circle.png', color=define.BLACK)
        eyeball.scale = 0.5
        eye.add(eyeball)
        self.head.add(eye)

        self.add(self.head)

        self.speed = 150
        if not is_enemy:
            self.speed = 180
        self.path = [self.position] * 100

        self.schedule(self.update)
        if not self.is_enemy:
            self.schedule(self.my_ai)  # random.random() * 0.1 + 0.05
        else:
            self.schedule_interval(self.ai, random.random() * 0.1 + 0.05)

    def add_body(self):
        b = Sprite('circle.png', color=self.color)
        b.scale = 1.5
        self.body.append(b)
        if self.x == 0:
            print(self.position())

        b.position = self.position
        self.parent.batch.add(b, 9999 - len(self.body))

    def my_ai(self, dt):
        self.angle_dest = (self.angle_dest + 360) % 360
        if (self.x < 100 and 90 < self.angle_dest < 270) or (
                        self.x > define.WIDTH - 100 and (
                                self.angle_dest < 90 or self.angle_dest > 270)
        ):
            self.angle_dest = 180 - self.angle_dest
        elif (self.y < 100 and self.angle_dest > 180) or (
                        self.y > define.HEIGHT - 100 and self.angle_dest < 180
        ):
            self.angle_dest = -self.angle_dest
        else:
            anemey = self._get_nearest_em()
            if anemey != None:
                self.angle_dest = self.select_direction(anemey)

    def _judge_pos(self, enemey):

        em_x, em_y = enemey.position
        m_x, m_y = self.position
        em_angle = enemey.angle
        return math.tan(em_angle) * m_x + (em_y * math.tan(em_angle) * em_x) - m_y > 0

    def _get_nearest_em(self):
        arena = self.parent
        m_x, m_y = self.position

        Min = 100000
        Min_body = -1
        Min_em = -1
        for em in arena.enemies:
            for bd in em.body:
                d_x, d_y = bd.position
                _y = d_y - m_y
                _x = d_x - m_x
                distance = math.sqrt(_y ** 2 + _x ** 2)
                if distance < Min:
                    Min = distance
                    Min_body = bd
                    Min_em = em
        # print(Min)
        Min_em.color = define.BLACK
        if Min > self.threhold:
            return None
        else:
            return Min_em

    def select_direction(self, enemey):
        em_x, em_y = enemey.position
        m_x, m_y = self.position
        em_angle = enemey.angle
        if self._judge_pos(enemey):
            if em_angle > 180:
                angle_round = (em_angle - 360, em_angle - 180)
            else:
                angle_round = (em_angle - 180, em_angle)
        else:
            if em_angle > 180:
                angle_round = (em_angle - 180, em_angle)
            else:
                angle_round = (em_angle, em_angle + 180)

        angle_list = [1] * 180
        arena = self.parent
        for dot in arena.dots:
            d_x, d_y = dot.position
            _y = d_y - m_y
            _x = d_x - m_x
            distance = math.sqrt(_y ** 2 + _x ** 2)
            if distance > self.threhold:
                continue
            if _x == 0:
                theta = 0
            else:
                theta = math.atan(abs(_y) / abs(_x)) * 180 / math.pi
            score = self.hunger / distance
            try:
                if math.tan(em_angle) > 0:
                    if _x < 0:
                        if _y < 0:
                            angle_list[int(-angle_round[0] + theta)] += score
                        else:
                            angle_list[int(-angle_round[0] - theta)] += score
                    else:
                        if _y < 0:
                            angle_list[int(180 - angle_round[0] - theta)] += score
                        else:
                            angle_list[int(180 - angle_round[0] + theta)] += score
                else:
                    if _x < 0:
                        if _y < 0:
                            angle_list[int(180 - angle_round[0] - theta)] += score
                        else:
                            angle_list[int(180 - angle_round[0] + theta)] += score
                    else:
                        if _y < 0:
                            angle_list[int(theta - angle_round[0])] += score
                        else:
                            angle_list[int(-angle_round[0] - theta)] += score
            except:
                continue

        for em in arena.enemies:
            for bd in em.body:
                d_x, d_y = bd.position
                _y = d_y - m_y
                _x = d_x - m_x
                distance = math.sqrt(_y ** 2 + _x ** 2)
                if distance > self.threhold:
                    continue
                if _x != 0:
                    theta = math.atan(abs(_y) / abs(_x)) * 180 / math.pi
                else:
                    theta = 0
                try:
                    score = self.alive / distance
                except:
                    continue
                try:
                    if math.tan(em_angle) > 0:
                        if _x < 0:
                            if _y < 0:
                                angle_list[int(-angle_round[0] + theta)] -= score
                            else:
                                angle_list[int(-angle_round[0] - theta)] -= score
                        else:
                            if _y < 0:
                                angle_list[int(180 - angle_round[0] - theta)] -= score
                            else:
                                angle_list[int(180 - angle_round[0] + theta)] -= score
                    else:
                        if _x < 0:
                            if _y < 0:
                                angle_list[int(180 - angle_round[0] - theta)] -= score
                            else:
                                angle_list[int(180 - angle_round[0] + theta)] -= score
                        else:
                            if _y < 0:
                                angle_list[int(theta - angle_round[0])] -= score
                            else:
                                angle_list[int(-angle_round[0] - theta)] -= score
                except:
                    continue

        score_array = np.array(angle_list, dtype=float)
        min_score = np.min(score_array)
        score_array = score_array + abs(min_score)
        score_sum = np.sum(score_array)
        p_array = score_array / score_sum
        try:
            angle = np.random.choice(a=180, p=p_array)
        except:
            print(score_array)
            print(score_sum)
            print(p_array)
        # print angle
        return (angle_round[0] + angle + 360) % 360

    def init_body(self):
        self.score = 30
        self.length = 4
        self.body = []
        for i in range(self.length):
            self.add_body()

    def update(self, dt):
        self.angle = (self.angle + 360) % 360

        arena = self.parent
        if self.is_enemy:
            self.check_crash(arena.snake)
        for s in arena.enemies:
            if s != self and not s.is_dead:
                self.check_crash(s)
        if self.is_dead:
            return

        if abs(self.angle - self.angle_dest) < 2:
            self.angle = self.angle_dest
        else:
            if (0 < self.angle - self.angle_dest < 180) or (
                            self.angle - self.angle_dest < -180):
                self.angle -= 500 * dt
            else:
                self.angle += 500 * dt
        self.head.rotation = -self.angle

        self.x += math.cos(self.angle * math.pi / 180) * dt * self.speed
        self.y += math.sin(self.angle * math.pi / 180) * dt * self.speed
        self.path.append(self.position)

        lag = int(round(1100.0 / self.speed))
        for i in range(int(self.length)):
            idx = (i + 1) * lag + 1
            self.body[i].position = self.path[-min(idx, len(self.path))]
            if self.body[i].x == 0:
                print(self.body[i].position)
        m_l = max(self.length * lag * 2, 60)
        if len(self.path) > m_l:
            self.path = self.path[int(-m_l * 2):]

    def update_angle(self, keys):
        x, y = 0, 0
        if 65361 in keys:  # 左
            x -= 1
        if 65362 in keys:  # 上
            y += 1
        if 65363 in keys:  # 右
            x += 1
        if 65364 in keys:  # 下
            y -= 1
        directs = ((225, 180, 135), (270, None, 90), (315, 0, 45))
        direct = directs[x + 1][y + 1]
        if direct is None:
            self.angle_dest = self.angle
        else:
            self.angle_dest = direct

    def add_score(self, s=1):
        if self.is_dead:
            return
        self.score += s
        l = (self.score - 6) / 6
        if l > self.length:
            self.length = l
            self.add_body()

    def ai(self, dt):

        self.angle_dest = (self.angle_dest + 360) % 360
        if (self.x < 100 and 90 < self.angle_dest < 270) or (
                        self.x > define.WIDTH - 100 and (
                                self.angle_dest < 90 or self.angle_dest > 270)
        ):
            self.angle_dest = 180 - self.angle_dest
        elif (self.y < 100 and self.angle_dest > 180) or (
                        self.y > define.HEIGHT - 100 and self.angle_dest < 180
        ):
            self.angle_dest = -self.angle_dest
        else:
            arena = self.parent
            self.collision_detect(arena.snake)
            for s in arena.enemies:
                if s != self:
                    self.collision_detect(s)

    def collision_detect(self, other):
        if self.is_dead or other.is_dead:
            return
        for b in other.body:
            d_y = b.y - self.y
            d_x = b.x - self.x
            if abs(d_x) > 200 or abs(d_y) > 200:
                return
            if d_x == 0:
                if d_y > 0:
                    angle = 90
                else:
                    angle = -90
            else:
                angle = math.atan(d_y / d_x) * 180 / math.pi
                if d_x < 0:
                    angle += 180
            angle = (angle + 360) % 360
            if abs(angle - self.angle_dest) < 5:
                self.angle_dest += random.randrange(90, 270)

    def check_crash(self, other):
        if self.is_dead or other.is_dead:
            return
        if (self.x < 0 or self.x > define.WIDTH) or (
                        self.y < 0 or self.y > define.HEIGHT
        ):
            self.crash()
            return
        for b in other.body:
            dis = math.sqrt((b.x - self.x) ** 2 + (b.y - self.y) ** 2)
            if dis < 24:
                self.crash()
                return

    def crash(self):
        if not self.is_dead:
            self.is_dead = True
            self.unschedule(self.update)
            self.unschedule(self.ai)
            arena = self.parent
            for b in self.body:
                dot = Dot(b.position, b.color)
                arena.batch.add(dot)
                arena.batch.add(dot)
                arena.dots.append(dot)
                arena.batch.remove(b)

            arena.remove(self)
            arena.add_enemy()
            del self.path
            if self.is_enemy:
                arena.enemies.remove(self)
                del self.body
                del self
            else:
                arena.parent.end_game()

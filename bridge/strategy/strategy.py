# !v DEBUG ONLY
import math  # type: ignore  # noqa: F401
from time import time  # type: ignore  # noqa: F401
from typing import Optional

from bridge import const
from bridge.auxiliary import aux, fld, rbt  # type: ignore  # noqa: F401
from bridge.const import State as GameStates
from bridge.router.actions import (  # type: ignore  # noqa: F401
    Action,
    Actions,
    KickActions,
    StrategyActions,
)


class Strategy:
    """Main class of strategy"""

    def __init__(self) -> None:
        self.we_active = False
        self.step = 0
        self.ball_pos_old = aux.Point(0, 0)   # ← новое поле

        self.last_positions = None
        self.stable_count = 0

        self.ready_to_start = False  # ← Флаг для старта

        # Память для позиций врагов
        self.enemy1_old = aux.Point(0, 0)
        self.enemy3_old = aux.Point(0, 0)


    def process(self, field: fld.Field) -> list[Optional[Action]]:
        """Game State Management"""
        if field.game_state not in [GameStates.KICKOFF, GameStates.PENALTY]:
            if field.active_team in [const.Color.ALL, field.ally_color]:
                self.we_active = True
            else:
                self.we_active = False

        actions: list[Optional[Action]] = []
        for _ in range(const.TEAM_ROBOTS_MAX_COUNT):
            actions.append(None)

        match field.game_state:
            case GameStates.RUN:
                self.run(field, actions)
            case GameStates.TIMEOUT:
                pass
            case GameStates.HALT:
                return [None] * const.TEAM_ROBOTS_MAX_COUNT
            case GameStates.PREPARE_PENALTY:
                pass
            case GameStates.PENALTY:
                pass
            case GameStates.PREPARE_KICKOFF:
                pass
            case GameStates.KICKOFF:
                pass
            case GameStates.FREE_KICK:
                pass
            case GameStates.STOP:
                # The router will automatically prevent robots from getting too close to the ball
                self.run(field, actions)
            case GameStates.BALL_PLACEMENT:
                pass
            case GameStates.DEBUG:
                pass

        return actions

    def run(self, field: fld.Field, actions: list[Optional[Action]]) -> None:
        

        # собрать все позиции: свои + враги + мяч
        positions = [r.get_pos() for r in field.allies] +[r.get_pos() for r in field.enemies] +[field.ball.get_pos(    )]      
   
        
        if self.last_positions is not None:
            total_move = sum((a - b).mag() for a, b in zip(positions, self.last_positions))
            if total_move < 10:              # суммарное смещение < 10 мм за цикл
                self.stable_count += 1
            else:
                self.stable_count = 0        # кто-то двинулся — счётчик сброшен
        self.last_positions = positions

        if self.stable_count < 10:           # 10 циклов подряд все стояли
            return                           # ждём

        robot = field.allies[2] #robot2, this is our robot who move by me
        robot_pos = robot.get_pos()#robots pos, this is our robot who move by me
        robot_angle = robot.get_angle()#robots angle, this is our robot who move by me
        ball_pos = field.ball.get_pos()#balls pos

        robot_enemy_1=field.enemies[1]#robot_enemy1
        robot_enemy_3=field.enemies[3]#robot_enemy3


        #P_ATTEMP = aux.lerp(ball_pos, field.enemy_goal.center, 0.6) #pos target beetwen goal and ball
        P_ATTEMP = aux.lerp(robot_enemy_1.get_pos(), robot_enemy_3.get_pos(), 0.6) #pos target beetwen robo_enemy_1 and robot_enemy_3
        
        angle_to_attemp = aux.angle_to_point(robot_pos, P_ATTEMP)   #  angle pont beetwin target point and robot
        angle_ball = aux.angle_to_point(P_ATTEMP, ball_pos)         # balls angle from pont target

        if self.step == 0:
            # turn to the target
            actions[2] = Actions.GoToPoint(robot_pos, angle_to_attemp)
            err = abs(aux.wind_down_angle(angle_to_attemp - robot_angle))#
            print ('step 0')
            if err < 0.4:
                self.step = 1

        elif self.step == 1:
            # move to the target with targets angle
            actions[2] = Actions.GoToPoint(P_ATTEMP, angle_to_attemp)
            print('step1', "  ", robot_pos)
            if (P_ATTEMP - robot_pos).mag() < 80:
                self.step = 2
            else:
                actions[2] = Actions.GoToPoint(P_ATTEMP, angle_to_attemp)
                

        elif self.step == 2:
            # move to the ball angle from pont target
            actions[2] = Actions.GoToPoint(robot_pos, angle_ball)
            err = abs(aux.wind_down_angle(angle_ball - robot_angle))
            print('step2')
                        # Получаем текущие координаты врагов
            e1_pos = robot_enemy_1.get_pos()
            e3_pos = robot_enemy_3.get_pos()
            
            # Проверяем: сдвинулись ли враги (больше 50 мм) ИЛИ сдвинулся мяч
            enemy_moved = (self.enemy1_old - e1_pos).mag() > 50 or (self.enemy3_old - e3_pos).mag() > 50
            ball_moved = (self.ball_pos_old - ball_pos).mag() >= 2
            
            if enemy_moved or ball_moved:
                self.step = 0  # Всё изменилось — начинаем сначала (поворот → едем)
                
            # Обязательно сохраняем текущие позиции для следующего цикла
            self.enemy1_old = e1_pos
            self.enemy3_old = e3_pos
            self.ball_pos_old = ball_pos
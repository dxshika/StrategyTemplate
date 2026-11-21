'''

"""High-level strategy code"""

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

    def __init__(
        self,
    ) -> None:
        self.we_active = False

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
        """
        ONE ITERATION of strategy
        NOTE: robots will not start acting until this function returns an array of actions,
              if an action is overwritten during the process, only the last one will be executed)

        Examples of getting coordinates:
        - field.allies[8].get_pos(): aux.Point -   coordinates  of the 8th  robot from the allies
        - field.enemies[14].get_angle(): float - rotation angle of the 14th robot from the opponents

        - field.ally_goal.center: Point - center of the ally goal
        - field.enemy_goal.hull: list[Point] - polygon around the enemy goal area


        Examples of robot control:
        - actions[2] = Actions.GoToPoint(aux.Point(1000, 500), math.pi / 2)
                The robot number 2 will go to the point (1000, 500), looking in the direction π/2 (up, along the OY axis)

        - actions[3] = Actions.Kick(field.enemy_goal.center)
                The robot number 3 will hit the ball to 'field.enemy_goal.center' (to the center of the enemy goal)

        - actions[9] = Actions.BallGrab(0.0)
                The robot number 9 grabs the ball at an angle of 0.0 (it looks to the right, along the OX axis)
        """

        
        
        

    def __init__(self) -> None:
        self.we_active = False
        self.step = 0          # ← вот это добавь

    
                
        P_ATTEMP = aux.lerp(field.ball.get_pos(), field.enemy_goal.center, 0.6)
        angle_vec= aux.angle_to_point(P_ATTEMP, P_ATTEMP.arg())
        angle_ball    = aux.angle_to_point(P_ATTEMP, field.ball.get_pos())   # из целевой точки на мяч
            if step == 0:
                actions[2] = Actions.GoToPoint(field.allies[2].get_pos, angle_vec)
                step = 1 

            elif step == 1:
                 actions[2] = Actions.GoToPoint(P_ATTEMP, angle_vec)
                 step = 2 
                    
            elif step == 2:
                actions[2] = Actions.GoToPoint(field.allies[2].get_pos, angle)
                step = 0 
                


                '''

"""High-level strategy code"""

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
        

        robot = field.allies[2] #robot2 
        robot_pos = robot.get_pos()#robots pos
        robot_angle = robot.get_angle()#robots angle
        ball_pos = field.ball.get_pos()#balls pos

        P_ATTEMP = aux.lerp(ball_pos, field.enemy_goal.center, 0.6) #pos target beetwen goal and ball
        angle_to_attemp = aux.angle_to_point(robot_pos, P_ATTEMP)   #  angle pont beetwin target point and robot
        angle_ball = aux.angle_to_point(P_ATTEMP, ball_pos)         # balls angle from pont target

        if self.step == 0:
            # turn to the target
            actions[2] = Actions.GoToPoint(robot_pos, angle_to_attemp)
            err = abs(aux.wind_down_angle(angle_to_attemp - robot_angle))#
            if err < 0.4:
                self.step = 1

        elif self.step == 1:
            # move to the target with targets angle
            actions[2] = Actions.GoToPoint(P_ATTEMP, robot_angle)
            if (P_ATTEMP - robot_pos).mag() < 100:
                self.step = 2

        elif self.step == 2:
            # move to the ball angle from pont target
            actions[2] = Actions.GoToPoint(robot_pos, angle_ball)
            err = abs(aux.wind_down_angle(angle_ball - robot_angle))
            if (self.ball_pos_old - ball_pos).mag() >= 2:
                self.step = 0
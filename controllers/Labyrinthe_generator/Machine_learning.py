import numpy as np
import Robot_Controller as rc
import random
from copy import deepcopy
from numpy import zeros


# Set of actions
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

# Set of environment states
EMPTY_SQUARE = 0
WALL = 1
TARGET = 2
ROBOT = -1

# Learning rate, discount factor & exploration factor
ALPHA = 0.1
GAMMA = 0.9
EPSILON = 0.2

class Q_learning :

    def __init__(self, map, supervisor, epuck):
        self.map = deepcopy(map)
        self.rows = len(map)
        self.cols = len(map[0])

        # game status
        self.nb_episodes = 0
        self.threshold = -0.5 * self.rows 
        self.total_rewards = 0 
        self.game_status = 'start'                                                                                                                                                                                    

        # postion of target
        target_pos_tuple = [(r,c) for r in range(self.rows) for c in range(self.cols) if self.map[r][c] == TARGET]
        self.target_pos = list(target_pos_tuple[0])

        # robot stuff
        robot_pos_tuple = [(r,c) for r in range(self.rows) for c in range(self.cols) if self.map[r][c] == ROBOT]     
        self.robot_pos = list(robot_pos_tuple[0])
        self.robot_state = 'start'
        self.robot = rc.rb_ctrl(supervisor,epuck)
        
        self.visited_cells = []
        
        # initiate Q
        num_states = self.rows * self.cols
        self.Q = zeros((num_states, 4), float)

        random.seed(1)

    def Q_learning(self, action, reward, current_state, next_state) :

        target = reward + GAMMA * np.max(self.Q[next_state, :])

        # update the Q_table using a weighted average of the current Q_value and the target
        self.Q[current_state, action] = (1 - ALPHA) * self.Q[current_state, action] + ALPHA * target

        # another way to update the Q_table
        # self.Q[current_state, action] = self.Q[current_state, action] + ALPHA * (target - self.Q[current_state, action])
            
    def get_game_status(self):
        # the robot has reached the threshold 
        if self.total_rewards < self.threshold:
            return 'lose'
        # the robot found the target
        if self.robot_pos == self.target_pos:
            return 'win'
        return 'not_over'

    def get_reward(self):
        # the robot finds the target
        if self.robot_pos == self.target_pos:
            return 1.0
            
        # the robot is blocked, another episode must start
        if self.robot_state == 'blocked':
            return self.threshold - 1

        if self.robot_state == 'valid':
            # the robot already visited this cell
            if self.robot_pos in self.visited_cells:
                return -0.50
            else:
                return +0.04

        if self.robot_state == 'invalid':
            return -0.75

    def act(self, action):
        self.update_state(action)
        reward = self.get_reward()
        self.total_rewards += reward
        status = self.get_game_status()
        return reward, status

    def update_state(self, action):
        # we check if the action is valid
        valid_actions = self.valid_actions()

        # no action possible
        if not valid_actions :
            self.robot_state = 'blocked'

        elif action in valid_actions:
            self.robot_state = 'valid'
            self.act_robot(action)

        else:
            self.robot_state = 'invalid'
            
    def act_robot(self, action):
        last_x = self.robot_pos[0]
        last_y = self.robot_pos[1]

        # perform the action
        if action == UP:
            self.robot.haut()
            self.robot_pos[0]-=1

        if action == DOWN:
            self.robot.bas()
            self.robot_pos[0]+=1

        if action == LEFT:
            self.robot.gauche()
            self.robot_pos[1]-=1

        if action == RIGHT:
            self.robot.droite()
            self.robot_pos[1]+=1

        # mark the new space on which the robot is
        new_x = self.robot_pos[0]
        new_y = self.robot_pos[1]      
        self.update_map(last_x, last_y, new_x, new_y)

    def valid_actions(self):
        actions = [UP, DOWN, LEFT, RIGHT]
        x = self.robot_pos[0]
        y = self.robot_pos[1]

        # we check if the robot is in the corner or is surrounded by walls
        if (x == 0) or (x > 0 and self.map[x-1][y] == WALL):
            actions.remove(UP)

        if (x == self.rows-1) or (x < self.rows-1 and self.map[x+1][y] == WALL):
            actions.remove(DOWN)

        if (y == 0) or (y > 0 and self.map[x][y-1] == WALL):
            actions.remove(LEFT)

        if (y == self.cols-1) or (y < self.cols-1 and self.map[x][y+1] == WALL):
            actions.remove(RIGHT)

        return actions
        
    def restart(self, map):
        # message
        print("The robot "+self.game_status)
        print("Episode "+str(self.nb_episodes)+" finished\n")

        # restart the position of the robot
        self.map = deepcopy(map)
        robot_pos_tuple = [(r,c) for r in range(self.rows) for c in range(self.cols) if self.map[r][c] == ROBOT]     
        self.robot_pos = list(robot_pos_tuple[0])
        self.robot.restart(self.robot_pos[0], self.robot_pos[1])

        self.game_status = 'start'
        self.robot_state = 'start' 
        self.total_rewards = 0
        self.visited_cells = []
        self.nb_episodes+=1

    def epsilon_greedy_policy(self):
        r = random.random()

        # EXPLORATION
        if r < EPSILON:
            action = random.randint(UP, RIGHT)

        # EXPLOITATION
        else:
            index = self.pos_to_index()

            q_values = self.Q[index]
            value_max = np.max(q_values)

            action_max_reward = []
            for i in range(len(self.Q[index])):
                if self.Q[index][i] == value_max:
                    action_max_reward.append(i)

            action = action_max_reward[random.randint(0, len(action_max_reward)-1)]

        return action

    def pos_to_index(self):
        return self.robot_pos[0] * self.rows + self.robot_pos[1]

    def update_map(self, last_x, last_y, new_x, new_y):
        self.map[last_x][last_y] = EMPTY_SQUARE
        self.map[new_x][new_y] = ROBOT
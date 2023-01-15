"""Labyrinthe_generator controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot, Node, Field, Supervisor
import Machine_learning as ml

#-------------------------------------
# -1 : position du robot au début
# 0 : case vide
# 1 : case mur
# 2 : position de l'objectif du robot
#-------------------------------------

"""
map = [
    [1,0,0,0,1,0,1,1],
    [-1,0,1,0,0,0,1,1],
    [1,1,1,0,1,1,2,1],
    [1,1,1,0,0,1,0,1],
    [1,0,0,0,1,1,0,1],
    [0,0,1,1,0,0,0,1],
    [1,0,0,1,0,1,1,1],
    [1,1,0,0,0,1,0,0]]
"""

map = [
       [-1,1,2],
       [0,0,0],
       [0,1,1]]
       
supervisor = Supervisor()

sol = supervisor.getFromDef("Sol")

floorSize = sol.getField("floorSize")
floortranslation = sol.getField("translation")

sizeX = len(map[1])/8
sizeY = len(map)/8

root_node = supervisor.getRoot()
children_field = root_node.getField('children')

#Taille du sol en fonction de la matrice
floorSize.setSFVec2f([sizeX,sizeY])
if sizeX < 1:
    translateX = 0.4375-(0.5*(1-sizeX))
else:
    translateX = 0.4375+(0.5*(sizeX-1))
if sizeY < 1:
    translateY = 0.4375-0.5*(1-sizeY)
else:
    translateY = 0.4375+(0.5*(sizeY-1))

floortranslation.setSFVec3f([translateX,translateY,0])

#Place le mur et le robot en dehors de la map au debut
node = supervisor.getRoot().getField("children").getMFNode(-1)

if node.getField("name").getSFString() == "e-puck":
    epuck = node
    epuck.getField("translation").setSFVec3f([-1.5,-1.5,0.005])
else:
    print("Erreur")
    
#Place les murs, le robots et l'objectif en fonction de la matrice
for x in range(len(map)):
    for y in range(len(map[x])):
        #Place les murs
        if map[x][y] == 1:
            children_field.importMFNodeFromString(-1, 'Wall {translation ' + str(0.125*x) + ' ' + str(0.125*y) + ' 0.05}')
            
            #mur_duplic.getField("translation").setSFVec3f([0.125*x,0.125*y,0.05])
        #Place le robot
        elif map[x][y] == -1:
            epuck.getField("translation").setSFVec3f([0.125*x,0.125*y,0.005])

# get the time step of the current world.
timestep = int(supervisor.getBasicTimeStep())

# start the learning
q_learning = ml.Q_learning(map, supervisor, epuck)
current_state = q_learning.pos_to_index()

# take a decision every modulo_step
modulo_step = 10000000000000000000000
max_episode = 10000

print(q_learning.threshold)

# Main loop:
while supervisor.step(timestep) != -1 and q_learning.nb_episodes < max_episode:

    if supervisor.step(timestep)%modulo_step == 0 :
        if q_learning.game_status != 'lose' and q_learning.game_status != 'win':
            # the robot choose an action
            chosen_action = q_learning.epsilon_greedy_policy()
    
            # perform the action
            reward, q_learning.game_status = q_learning.act(chosen_action)
            next_state = q_learning.pos_to_index()
    
            # update the Q_table
            q_learning.Q_learning(chosen_action, reward, current_state, next_state)
            current_state = next_state
            
            # print(q_learning.Q)
        
        else:
            # the robot loose or win the game, we restart a new episode
            q_learning.restart(map)

print("end")
# Enter here exit cleanup code.
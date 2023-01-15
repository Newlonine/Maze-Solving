# Maze solving with e-Puck

Gwenaël Delille - Nolwenn Paluet - M2 SIIA
***
### Machine Learning algorithms
We plan to use the Q-learning algorithm to train our robot to find the goal in our maze.

### Robotic Application
We plan to use Webots, an open-source robot simulator and E-puck, a tiny robot made for research and education. 
The first step is to designed a matrix which represents the maze and then to create it. And the second one is to program the function to direct the robot.

***
***
## Objectives description
For this project, we decided to use reinforcement learning to train a robot to find a goal in a maze. Our main objective was to learn more about Machine Learning and especially more about Reinforcement Learning.

## High-level description


## Results 
We tested program with two mazes : a 3x3 and a 8x8. It takes a lot of time for the robot to found the goal but fortunately we can speed up the simulation time.

In the 8x8 maze, the goal is at position (2, 6).
[Here](https://drive.google.com/file/d/1yFsZX92hPTwopLn47fQF8B3Z4vM2EjSW/view?usp=sharing), you can observe the beggining of the simulation.
[Here](https://drive.google.com/file/d/16_QhFwZmLGX2QW8OcrxxOORnK6ro7d3o/view?usp=sharing), you can observe the simulation once the robot has found the best path.

In the 3x3 maze, the goal is at position (0, 2).
[Here](https://drive.google.com/file/d/1e6Re5GzfiHdBouwmHn9sDVmYKUPmo5Mk/view?usp=sharing), the video of the simulation.

## Challenges

For the robotic application, we wanted to use ROS but we found it difficult so we decided to use Webots, we only needed a simple robot with few sensors and actuators. 
Then, we had some difficulties to move the robot with a precise distance so we decided to teleport the robot and not using its motors.
For the machine learning algorithms, we had some trouble finding the right parameters : sometimes the robot explores too much, sometimes not enough. Sometimes it retraces its steps too much so we had to adjust the reward.
For the human interaction, we didn't know what to do. A user can designed its own maze but they can not interact with the robot during the simulation.

## Future work
If we had more time, we would improve the movements of the robot. In our version, the robot is teleported to the location that it decides to go to but we would like a real movement thanks to its motors. 
We can also improve the reinforcement learning by adding a neural network, i.e. doing deep reinforcement learning.
Last, we would add human interaction, where the user would make a decision instead of the robot and observe how it adapts and reacts.

## Takeaways
- A lab session dedicated to this project would be nice. This can help us to think about what to do and also help us to start it. The subject of this project was far too free although examples have been given.
- About the group work : *insert something*
***
***
## Requirements
- [Webots R2022a](https://github.com/cyberbotics/webots/releases/tag/R2022a)
- Python 3.9

## Installation

- Open Webots
- Go to *File* -> *Open Wolrds...*
- In the project repository go to *worlds* and select *iml.wbt*
- To run the simulation, click on the play button above the scene view
- You can modify the maze by changing the map : project repository -> *controllers* -> *Labyrinthe_generator* -> *Labyrinthe_generator.py*

## Resources used

 - https://samyzaf.com/ML/rl/qmaze.html 
 - https://blog.engineering.publicissapient.fr/2020/02/12/reinforcement-learning-introduction/
 - https://towardsdatascience.com/how-to-design-reinforcement-learning-reward-function-for-a-lunar-lander-562a24c393f6
 - https://cyberbotics.com/doc/guide

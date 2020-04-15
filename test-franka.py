import gym
import frankaenv

e = gym.make('Franka-v0')
e.reset()
while True:
    e.render()
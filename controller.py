#!/usr/bin/env python
# manual

"""
This script allows you to manually control the simulator or Duckiebot
using the keyboard arrows.
"""

import sys
import argparse
import pyglet
from pyglet.window import key
import numpy as np
import gym

import frankaenv


# from experiments.utils import save_img


# Register a keyboard handler
import glfw


def on_press(window, key, scancode, action, mods):
    global action_to_take, grasp, action_array
    pos = np.zeros(4)
    _pos_step = 0.1

    # controls for moving position
    if key == glfw.KEY_A:
        pos[1] -= _pos_step  # dec x
    elif key == glfw.KEY_D:
        pos[1] += _pos_step  # inc x
    elif key == glfw.KEY_W:
        pos[0] -= _pos_step  # dec y
    elif key == glfw.KEY_S:
        pos[0] += _pos_step  # inc y
    elif key == glfw.KEY_DOWN:
        pos[2] -= _pos_step  # dec z
    elif key == glfw.KEY_UP:
        pos[2] += _pos_step  # inc z
    elif key == glfw.KEY_ESCAPE:
        np.save('actions', action_array)
        exit()

    pos[3] = grasp
    action_to_take = pos
    action_array.append(action_to_take)

def on_scroll_action(window, x_offset, y_offset):
    global action_to_take, grasp, action_array
    
    grasp = np.clip(grasp + 0.05 * y_offset, -1, 1)
    action_to_take = [0., 0., 0., grasp]
    action_array.append(action_to_take)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--env-name', default="FetchPickAndPlace-v1")
    parser.add_argument('--seed', default=1, type=int, help='seed')
    parser.add_argument('--record',action='store_true')
    args = parser.parse_args()

    env = gym.make(args.env_name)
    env._max_episode_steps = 10000
    env.seed(args.seed)
    env.reset()

    env.render()

    env.unwrapped.viewer.cam.trackbodyid = 0
    env.unwrapped.viewer.cam.elevation = -44        # camera rotation around the axis in the plane going through the frame origin (if 0 you just see a line)
    env.unwrapped.viewer.cam.azimuth = 120     

    env.render()

    action_to_take = np.zeros(4)
    grasp = 0
    action_array = []

    if args.record:
        glfw.set_key_callback(env.unwrapped.viewer.window, on_press)
        glfw.set_scroll_callback(env.unwrapped.viewer.window, on_scroll_action)

        while True:
            env.render()

            if not np.array_equal(action_to_take, np.zeros(4)):
                _, _, d , _ = env.step(action_to_take)
                if d: 
                    env.seed(args.seed)
                    env.reset()                   
                    
                    env.unwrapped.viewer.cam.trackbodyid = 0
                    env.unwrapped.viewer.cam.elevation = -44
                    env.unwrapped.viewer.cam.azimuth = 120

                    env.render()
                    action_to_take = np.zeros(4)
                
                action_to_take = np.zeros(4)
    else:
        actions = np.load('actions.npy')
        for action in actions:
            env.step(action)
            env.render()
            

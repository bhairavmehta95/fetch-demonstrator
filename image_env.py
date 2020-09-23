import gym 
import numpy as np
from PIL import Image
import h5py

env = gym.make('FetchPush-v1')
env = gym.wrappers.FlattenObservation(env   )

with h5py.File('data.h5', 'w') as hf:
    for episode in range(3):
        g = hf.create_group(f'episode_{episode}')
        o = env.reset()
        done = False

        observations = []
        next_observations = []
        images = []
        rewards = []
        actions = []
        dones = []

        while not done:
            action = env.action_space.sample()
            no, r, done, _ = env.step(action)
            # img = env.render(mode='rgb_array')

            observations.append(o)
            actions.append(action)
            next_observations.append(no)
            rewards.append(r)
            # images.append(img)
            dones.append(done)

            o = no

        g.create_dataset('observations',data=observations)
        g.create_dataset('actions',data=actions)
        g.create_dataset('next_observations', data=next_observations)
        g.create_dataset('rewards', data=rewards)
        # g.create_dataset('images', data=images)
        g.create_dataset('dones', data=dones)
    

        





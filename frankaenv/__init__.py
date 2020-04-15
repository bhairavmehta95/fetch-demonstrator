from gym.envs.registration import registry, register, make, spec

register(
    id='Franka-v0',
    entry_point='frankaenv.franka_env:FrankaEnv',
    max_episode_steps=200,
)

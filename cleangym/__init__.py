from gym.envs.registration import register

register(
    id='Carnot-v0',
    entry_point='cleangym.carnot_lim:CarnotEnv',
    max_episode_steps=60,
)

register(
    id='Carnot-v1',
    entry_point='cleangym.carnot:CarnotEnv',
    max_episode_steps=60,
)

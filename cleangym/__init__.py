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

register(
    id='GridWorld-v0',
    entry_point='cleangym.gridworld:GridWorldEnv',
    max_episode_steps = 50,
)

register(
    id='DumbLoop-v0',
    entry_point='cleangym.loop_perimeter:LoopEnv',
    max_episode_steps = 200,
)

register(
    id='DumbLoop-v1',
    entry_point='cleangym.loop_off_perimeter:LoopEnv',
    max_episode_steps = 200,
)

register(
    id='DumbLoop-v2',
    entry_point='cleangym.loop_area:LoopEnv',
    max_episode_steps = 200,
)

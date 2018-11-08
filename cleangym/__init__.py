from gym.envs.registration import register

register(
    id='Carnot-v0',
    entry_point='cleangym.carnot_lim:CarnotEnv',
    max_episode_steps=500,
)

register(
    id='Carnot-v1',
    entry_point='cleangym.carnot:CarnotEnv',
    max_episode_steps=500,
)

register(
    id='Carnot-v2',
    entry_point='cleangym.carnot_dV:CarnotEnv',
    max_episode_steps=500,
)

register(
    id='Beeler-v0',
    entry_point='cleangym.beeler:BeelerEnv',
    max_episode_steps=500,
)

register(
    id='Beeler-v1',
    entry_point='cleangym.beeler_dV:BeelerEnv',
    max_episode_steps=500,
)

register(
    id='Stirling-v0',
    entry_point='cleangym.stirling:StirlingEnv',
    max_episode_steps=500,
)

register(
    id='Stirling-v1',
    entry_point='cleangym.stirling_dV:StirlingEnv',
    max_episode_steps=500,
)

register(
    id='Otto-v0',
    entry_point='cleangym.otto:OttoEnv',
    max_episode_steps=500,
)

register(
    id='Otto-v1',
    entry_point='cleangym.otto_dV:OttoEnv',
    max_episode_steps=500,
)


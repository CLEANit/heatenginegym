from gym.envs.registration import register

register(
    id='Carnot-v0',
    entry_point='heatenginegym.carnot_lim:CarnotEnv',
    max_episode_steps=200,
)

register(
    id='Carnot-v1',
    entry_point='heatenginegym.carnot:CarnotEnv',
    max_episode_steps=200,
)

register(
    id='Carnot-v2',
    entry_point='heatenginegym.carnot_dV:CarnotEnv',
    max_episode_steps=200,
)

register(
    id='Carnot-v3',
    entry_point='heatenginegym.carnot_continuous:CarnotEnv',
    max_episode_steps=200,
)

register(
    id='Carnot-v4',
    entry_point='heatenginegym.carnot_mdp:CarnotEnv',
    max_episode_steps=200,
)

register(
    id='Beeler-v0',
    entry_point='heatenginegym.beeler:BeelerEnv',
    max_episode_steps=200,
)

register(
    id='Beeler-v1',
    entry_point='heatenginegym.beeler_dV:BeelerEnv',
    max_episode_steps=200,
)

register(
    id='Stirling-v0',
    entry_point='heatenginegym.stirling:StirlingEnv',
    max_episode_steps=200,
)

register(
    id='Stirling-v1',
    entry_point='heatenginegym.stirling_dV:StirlingEnv',
    max_episode_steps=200,
)

register(
    id='Otto-v0',
    entry_point='heatenginegym.otto:OttoEnv',
    max_episode_steps=200,
)

register(
    id='Otto-v1',
    entry_point='heatenginegym.otto_dV:OttoEnv',
    max_episode_steps=200,
)


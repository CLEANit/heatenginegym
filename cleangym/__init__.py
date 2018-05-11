from gym.envs.registration import register

register(
    id='Carnot-v0',
    entry_point='cleangym.carnot:CarnotEnv',
)

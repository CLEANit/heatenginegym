from gym.envs.registration import register

register(
    id='cylinder-v0',
    entry_point='gym_cylinder.envs:CylinderEnv',
)
register(
    id='easy-cylinder-v0',
    entry_point='gym_cylinder.envs:EasyCylinderEnv',
)
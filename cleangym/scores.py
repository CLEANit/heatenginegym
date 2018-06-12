def Scores(game):
    if game == 'CartPole-v0':
        return 0.0, 200.0

    elif game == 'CartPole-v1':
        return 0.0, 500.0

    elif game == 'MountainCar-v0':
        return -200.0, 0.0

    elif game == 'Pendulum-v0':
        return -3254.0, 0.0

    elif game == 'Acrobot-v1':
        return -500.0, 0.0

    elif game == 'Carnot-v0':
        return -1.0, 1.0

    elif game == 'Carnot-v1':
        return -1.0, 1.0

    else:
        return 0.0, 0.0

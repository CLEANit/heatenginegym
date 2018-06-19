# Min and Max scores of each game used when calculating probabilites in selection process

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

    elif game == 'GridWorld-v0':
        return 0.0, 50.0

    elif game == 'DumbLoop-v0':
        return -200.0, 0.0

    elif game == 'DumbLoop-v1':
        return -200.0, 0.0

    elif game == 'DumbLoop-v2':
        return -200.0, 300.0

    else:
        return 0.0, 0.0

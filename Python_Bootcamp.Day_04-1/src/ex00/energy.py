from itertools import zip_longest


def fix_wirring(plugs, sockets, cables):
    return ['plug {x[1][1]} into {x[1][0]} using {x[0]}'.format(x=i) if i[0] != 'x' and i[1][0] != 'x' and i[1][1] != 'x' else 'weld {x[1][1]} to {x[1][0]} without plug'.format(x=i) if i[1][0] != 'x' and i[1][1] != 'x' else '\0' for i in zip(list(filter(lambda x: str(x)[:4] == 'plug', plugs)) + ['x']*len(cables), zip(filter(lambda x: str(
        x)[:6] == 'socket', sockets), filter(lambda x: str(x)[:5] == 'cable', cables)))]


if __name__ == '__main__':
    plugs = ['plug1', 'plug2', 'plug3']
    sockets = ['socket1', 'socket2', 'socket3', 'socket4']
    cables = ['cable1', 'cable2', 'cable3', 'cable4']

    for c in fix_wirring(plugs, sockets, cables):
        print(c)

    plugs = ['plugZ', None, 'plugY', 'plugX']
    sockets = [1, 'socket1', 'socket2', 'socket3', 'socket4']
    cables = ['cable2', 'cable1', False]

    for c in fix_wirring(plugs, sockets, cables):
        print(c)

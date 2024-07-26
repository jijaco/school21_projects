import yaml

with open("../../materials/todo.yml", 'r') as fp:
    todo_yaml = yaml.load(fp)

deploy_data = [
    {
        'name': 'Generate ansible file',
        'hosts': 'localhost',
        'become': 'yes',
        'tasks': [
            {'name': 'Install packages',
             'ansible.builtin.package':
                {'name': todo_yaml['server']['install_packages'],
                    'state': 'present'}},
            {'name': 'Copy files',
             'ansible.builtin.shell': 'cp ../ex00/{} ../ex01/{} ./'.format(todo_yaml['server']['exploit_files'][0], todo_yaml['server']['exploit_files'][1]),
             },
            {'name': 'Execute files',
             'ansible.builtin.shell': 'python3 ./{} ./{} --bad-guys {}'.format(todo_yaml['server']['exploit_files'][0], todo_yaml['server']['exploit_files'][1],
                                                                               ','.join(todo_yaml['bad_guys']))}
        ]
    }
]

with open('deploy.yml', 'w') as file:
    yaml.dump(deploy_data, file, default_flow_style=False)

# print(yaml.dump(deploy_data))

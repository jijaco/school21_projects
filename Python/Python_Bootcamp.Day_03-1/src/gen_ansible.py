import yaml

with open("../../materials/todo.yml", 'r') as fp:
    x = yaml.load(fp)

deploy_data = [
    {
        'name': 'Generate ansible file',
        'hosts': 'localhost',
        'become': 'yes',
        'tasks': [
            {'name': 'Install packages',
             'ansible.builtin.package':
                {'name': ['python3', 'nginx'],
                    'state': 'present'}},
            {'name': 'Copy files',
             'ansible.builtin.copy':
                {'src': './gen_ansible.py',
                    'dest': '../gen_ansible.py'}},
            {'name': 'Execute files',
             'ansible.builtin.shell': 'python3 ../ex00/exploit.py ../ex01/consumer.py'}
        ]
    }
]

with open('deploy.yml', 'w') as file:
    yaml.dump(deploy_data, file, default_flow_style=False)

# print(yaml.dump(deploy_data))

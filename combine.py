def combine_gpu(server_gpu):
    all_gpu = []
    for server in server_gpu:
        for gpu in server_gpu[server]:
            gpu['host'] = server
            all_gpu.append(gpu)
    return all_gpu


def combine_user(server_processes):
    users = {}
    for server in server_processes:
        for p in server_processes[server]:
            user = p['user']
            if user not in users:
                users[user] = {
                    'proc': 0,
                    'mem': 0,
                    'host': set(),
                }
            users[user]['proc'] += 1
            users[user]['mem'] += p['mem']
            users[user]['host'].add(server)
    return [
        {
            'user': user,
            'proc': info['proc'],
            'mem': info['mem'],
            'host': ','.join(info['host']),
        }
        for user, info in users.items()
    ]


def get_user_from_process(process):
    # count number of processes and total memory usage for each user
    users = {}
    for p in process:
        user = users.setdefault(p['user'], {'proc': 0, 'mem': 0, 'gpu': []})
        user['proc'] += 1
        user['mem'] += p['mem']
        user['gpu'].append(str(p['gpu']))
    return [
        {
            'user': user,
            'proc': users[user]['proc'],
            'mem': users[user]['mem'],
            'gpu': ','.join(users[user]['gpu'])
        }
        for user, info in users.items()
    ]

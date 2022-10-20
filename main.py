import argparse
import json

from combine import *
from data import *
from fetch_data import *
from table import *
from utils import *


def get_servers(args: argparse.Namespace):
    arg_server = args.server
    servers = []
    if len(arg_server) == 1 and arg_server[0].endswith('.json'):
        with open(arg_server[0]) as f:
            servers = json.load(f)
    else:
        if args.index:
            raise ValueError('index can only be used when input is json config')
        for server_str in arg_server:
            user_pwd, host = server_str.split('@')
            user, pwd = user_pwd.split(':')
            servers.append({
                'host': host,
                'username': user,
                'password': pwd
            })
    if args.index:
        index = [int(i) for i in args.index.split(',')]
        servers = [servers[i] for i in index]
    return list(filter(lambda s: s['username'] and s['password'] and s['host'], servers))


def separate_mode(server_processes, server_gpus, sort_gpu, sort_proc, sort_user):
    for server in server_processes:
        users = get_user_from_process(server_processes[server])
        # GPU Table
        server_gpus[server].sort(key=lambda g: g[sort_gpu], reverse=is_reverse(sort_gpu))
        table_gpu = Table(title=f'GPU [{server}]',
                          headers=['GPU', 'Mem-Free', 'Mem-Use', 'GPU-Util'],
                          align='llrr',
                          unit=['', ' MiB', ' MiB', '%'])
        for gpu in server_gpus[server]:
            table_gpu.add_row([gpu['id'], gpu['mem-free'], gpu['mem-used'], gpu['gpu-util']])
        # Process Table
        server_processes[server].sort(key=lambda p: p[sort_proc], reverse=is_reverse(sort_proc))
        table_proc = Table(title=f'Process [{server}]',
                           headers=['User', 'GPU', 'PID', 'Mem', 'CPU', 'Time', 'Command'],
                           align='lcccccr',
                           unit=['', '', '', ' MiB', '', '', ''])
        for p in server_processes[server]:
            table_proc.add_row([p['user'], p['gpu'], p['pid'], p['mem'],
                                '{mem} MiB ({util}%)'.format(mem=p['cpu-mem'], util=p['cpu-util']),
                                seconds_format(p['time']),
                                simplify_command(p['command'])])
        # User Table
        users.sort(key=lambda u: u[sort_user], reverse=is_reverse(sort_user))
        table_user = Table(title=f'User [{server}]',
                           headers=['User', 'Proc', 'Mem', 'GPU'],
                           align='lcrr',
                           unit=['', '', ' MiB', ''])
        for u in users:
            table_user.add_row([u['user'], u['proc'], u['mem'], u['gpu']])

        print(table_gpu, table_proc, table_user, sep='\n\n')


def combine_mode(server_processes, server_gpus, sort_gpu, sort_proc, sort_user):
    all_gpus = combine_gpu(server_gpus)
    all_gpus.sort(key=lambda g: g[sort_gpu], reverse=is_reverse(sort_gpu))
    table_gpu = Table(title='GPU',
                      headers=['Host', 'GPU', 'Mem-Free', 'Mem-Use', 'GPU-Util'],
                      align='llrrr',
                      unit=['', '', ' MiB', ' MiB', '%'])
    for gpu in all_gpus:
        table_gpu.add_row([gpu['host'], gpu['id'], gpu['mem-free'], gpu['mem-used'], gpu['gpu-util']])

    all_users = combine_user(server_processes)
    all_users.sort(key=lambda u: u[sort_user], reverse=is_reverse(sort_user))
    table_user = Table(title='User',
                       headers=['User', 'Proc', 'Mem', 'Host'],
                       align='lcrr',
                       unit=['', '', ' MiB', ''])
    for u in all_users:
        table_user.add_row([u['user'], u['proc'], u['mem'], u['host']])

    print(table_gpu, table_user, sep='\n\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--combine', action='store_true', help='combine all server\'s output')
    parser.add_argument('-i', '--index', type=str, help='index of servers to show (only when input is json config)')
    parser.add_argument('server', type=str, nargs='+',
                        help='json config file or server address in format of user:password@host')
    parser.add_argument('-g', '--sort-gpu', choices=GPU_KEY, help='sort gpu by key', default='mem-free')
    parser.add_argument('-p', '--sort-proc', choices=PROC_KEY, help='sort process by key', default='mem')
    parser.add_argument('-u', '--sort-user', choices=['user', 'proc', 'mem'], help='sort user by key', default='mem')
    args = parser.parse_args()

    servers = get_servers(args)
    process, gpu = {}, {}
    for server in servers:
        host = server['host']
        p, g = handle_server(**server)
        process[host] = p
        gpu[host] = g

    if args.combine:
        combine_mode(process, gpu, args.sort_gpu, args.sort_proc, args.sort_user)
    else:
        separate_mode(process, gpu, args.sort_gpu, args.sort_proc, args.sort_user)


if __name__ == '__main__':
    main()

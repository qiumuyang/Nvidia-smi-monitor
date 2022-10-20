from typing import Generator

from paramiko import SSHClient, AutoAddPolicy

from parse import parse_gpu_process, parse_gpu_status


def fetch_process_info(client, pid: int) -> dict:
    cmd = 'ps -p {pid} -o user=,etimes=,rss=,pcpu=,command='.format(pid=pid)
    _, stdout, _ = client.exec_command(cmd)
    info = stdout.read().decode('UTF-8').strip().split(maxsplit=4)
    return {
        'user': info[0],
        'time': int(info[1]),  # in seconds
        'cpu-mem': int(info[2]) // 1024,  # in MiB
        'cpu-util': float(info[3]),
        'command': info[4],
    }


def fetch_gpu_process(client) -> Generator[dict, None, None]:
    _, stdout, _ = client.exec_command('nvidia-smi')
    for process in parse_gpu_process(stdout.read().decode('UTF-8')):
        # add more info from pid
        process.update(fetch_process_info(client, process['pid']))
        yield process


def fetch_gpu_status(client) -> Generator[dict, None, None]:
    _, stdout, _ = client.exec_command('nvidia-smi')
    for status in parse_gpu_status(stdout.read().decode('UTF-8')):
        yield status


def handle_server(host: str, username: str, password: str):
    with SSHClient() as client:
        client.set_missing_host_key_policy(AutoAddPolicy())
        client.connect(
            hostname=host,
            username=username,
            password=password
        )
        processes = list(fetch_gpu_process(client))
        statuses = list(fetch_gpu_status(client))
    return processes, statuses


__all__ = ['handle_server']

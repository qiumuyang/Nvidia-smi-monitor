import re
from typing import Generator


def parse_gpu_process(info: str) -> Generator[dict, None, None]:
    # Header: GPU, [GI,] [CI,] PID, Type, Process name, GPU Memory Usage
    # [] means optional
    # only focus on digits, i.e. GPU, PID, Memory
    pattern = re.compile(r'(\d+).*?(\d+).*?(\d+)MiB')
    for line in info.splitlines():
        # remove table-border and spaces
        line = line.strip('|').strip()
        match = pattern.fullmatch(line)
        if match:
            yield {
                'gpu': int(match.group(1)),
                'pid': int(match.group(2)),
                'mem': int(match.group(3)),
            }


def parse_gpu_status(info: str) -> Generator[dict, None, None]:
    # Header: Fan, Temp, Perf, Pwr:Usage/Cap, Memory-Usage, GPU-Util, Compute M.
    n_gpu = 0
    pattern = re.compile(r'(\d+)C +P(\d) +(\d+W / \d+W).*?(\d+)MiB / (\d+)MiB.*?(\d+)%')
    for line in info.splitlines():
        match = pattern.search(line)
        if match:
            yield {
                'id': n_gpu,  # TODO: fetch ID from the info string, current implementation is not robust
                'temp': int(match.group(1)),
                'perf': int(match.group(2)),
                'power': match.group(3),
                'mem-used': int(match.group(4)),
                'mem-total': int(match.group(5)),
                'mem-free': int(match.group(5)) - int(match.group(4)),
                'gpu-util': int(match.group(6)),
            }
            n_gpu += 1

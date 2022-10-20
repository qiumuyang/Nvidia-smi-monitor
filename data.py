# available sort keys for gpu and process
GPU_KEY = ['id', 'temp', 'mem-free', 'mem-used', 'mem-total', 'gpu-util']  # non-sortable: perf, power

PROC_KEY = ['pid', 'user', 'gpu', 'mem', 'cpu-mem', 'cpu-util', 'time']  # non-sortable: command

# the following keys need to set sort(reverse=True)
REVERSE = [
    # gpu
    'mem-free', 'mem-used', 'mem-total', 'temp',
    # process
    'mem', 'cpu-mem', 'cpu-util', 'gpu-util', 'time',
    # user
    'proc'
]


def is_reverse(key: str) -> bool:
    return key in REVERSE

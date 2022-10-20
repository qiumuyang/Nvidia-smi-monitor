from datetime import timedelta


def simplify_command(command: str, limit: int = 30) -> str:
    tokens = command.split()
    cmd = tokens[0]

    if '/' in cmd:
        cmd = cmd.split('/')[-1]  # do not show full path

    simple_cmd = cmd + ' ' + ' '.join(tokens[1:])
    if len(simple_cmd) <= limit:
        return simple_cmd
    else:
        return simple_cmd[:limit - 3] + '...'


def seconds_format(sec: int) -> str:
    # convert elapsed seconds to string (1d 02:03:04)
    delta = timedelta(seconds=sec)
    day = f'{delta.days}d ' if delta.days else ''
    return (day +
            f'{delta.seconds // 3600:02d}:' +
            f'{delta.seconds % 3600 // 60:02d}:' +
            f'{delta.seconds % 60:02d}')


__all__ = ['simplify_command', 'seconds_format']

"""Run a Python agent with a small outbound network probe."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

PROBE_DIR = Path(__file__).resolve().parent / 'probe'


def run(command, canary, allowed):
    if not canary or len(canary) < 8:
        raise ValueError('Use a synthetic canary of at least 8 characters')
    with tempfile.TemporaryDirectory(prefix='egress-lab-') as directory:
        events = Path(directory) / 'events.jsonl'
        env = os.environ.copy()
        env['PYTHONPATH'] = str(PROBE_DIR) + os.pathsep + env.get('PYTHONPATH', '')
        env['EGRESS_LAB_EVENTS'] = str(events)
        env['EGRESS_LAB_CANARY'] = canary
        result = subprocess.run(command, env=env, check=False)
        observations = []
        if events.exists():
            for line in events.read_text().splitlines():
                try:
                    observations.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
        destinations = sorted({e['host'] for e in observations if e.get('type') == 'connect'})
        leaks = sum(bool(e.get('canary_seen')) for e in observations)
        disallowed = sorted(set(destinations) - set(allowed)) if allowed else []
        return {
            'command_exit_code': result.returncode,
            'destinations': destinations,
            'disallowed_destinations': disallowed,
            'canary_exposures': leaks,
            'events': observations,
            'pass': result.returncode == 0 and leaks == 0 and not disallowed,
        }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--canary', required=True, help='Synthetic secret to detect')
    parser.add_argument('--allow-host', action='append', default=[], help='Allowed destination hostname; repeatable')
    parser.add_argument('--output', help='Write JSON report here')
    parser.add_argument('command', nargs=argparse.REMAINDER, help='Python command after --')
    args = parser.parse_args()
    command = args.command[1:] if args.command[:1] == ['--'] else args.command
    if not command:
        parser.error('Provide a Python command after --')
    try:
        report = run(command, args.canary, args.allow_host)
    except ValueError as exc:
        parser.error(str(exc))
    encoded = json.dumps(report, indent=2, sort_keys=True)
    if args.output:
        Path(args.output).write_text(encoded + '\n')
    print(encoded)
    return 0 if report['pass'] else 2


if __name__ == '__main__':
    sys.exit(main())

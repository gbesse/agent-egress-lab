# agent-egress-lab

[Français](README.md) · [English](README.en.md) · [Español](README.es.md)

Network egress regression test for **Python** agents. Run an agent with a synthetic canary: the report lists destinations and flags whether the canary appeared in an HTTP send. Exit code `2` fails CI on an exposure or a blocked destination.

## Quick start

Python 3.11+, no external dependencies.

```bash
python3 egress_lab.py --canary SYNTHETIC-CANARY-123 --allow-host 127.0.0.1 -- python3 examples/leaky_agent.py
python3 -m unittest discover -s tests -v
```

The first command should fail with `canary_exposures > 0`: the example sends only the synthetic canary to a local server. Use `--output report.json` to save a report and repeat `--allow-host` for an allowlist. Without an allowlist, destinations are observed only.

## Scope

The probe is injected through `sitecustomize` into the Python process and Python children that inherit its environment. It observes `socket.connect` and `http.client.HTTPConnection.send`. Native clients, non-Python processes, and some network paths are outside its coverage. Request bodies are not stored. This prototype is a regression test, not a security boundary.

Initial signal: [browser-use telemetry report](https://github.com/browser-use/browser-use/issues/5216). This repository does not reproduce that specific issue.

MIT licensed. Issues and pull requests for new adapters are welcome.

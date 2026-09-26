# agent-egress-lab

[Français](README.md) · [English](README.en.md) · [Español](README.es.md)

## Projets et signal à l'origine

- [browser-use](https://github.com/browser-use/browser-use) rend les agents navigateur accessibles. Son [issue #5216](https://github.com/browser-use/browser-use/issues/5216) signale un écart possible entre la description de la télémétrie et les données transmises. C'est un **signal de besoin**, pas un problème que nous affirmons avoir reproduit.
- **Notre angle :** tester, en CI, si un agent Python envoie un leurre synthétique vers une destination réseau. L'outil fonctionne sans intégration à browser-use et sa couverture est limitée aux appels Python instrumentés.

Test de sortie réseau pour agents **Python**. Exécutez un agent avec une valeur leurre synthétique : le rapport indique les destinations contactées et si la valeur est apparue dans un envoi HTTP. Un code de sortie `2` fait échouer la CI quand une fuite ou une destination interdite est détectée.

## Démarrage

Python 3.11+, sans dépendance externe.

```bash
python3 egress_lab.py --canary SYNTHETIC-CANARY-123 --allow-host 127.0.0.1 -- python3 examples/leaky_agent.py
python3 -m unittest discover -s tests -v
```

La première commande doit échouer avec `canary_exposures > 0` : `examples/leaky_agent.py` n'envoie que le leurre à un serveur local. Utilisez `--output report.json` pour archiver le rapport et répétez `--allow-host` pour définir une liste blanche. Le mode sans liste blanche observe seulement les destinations.

## Périmètre

La sonde est injectée via `sitecustomize` dans le processus Python et ses sous-processus Python qui héritent de l'environnement. Elle observe `socket.connect` et `http.client.HTTPConnection.send`. Elle ne voit pas tous les clients natifs, les processus non Python, ni tous les chemins réseau. Le rapport ne stocke pas le corps des requêtes. Ce prototype est un test de régression, pas une frontière de sécurité.


Licence MIT. Contributions et adaptateurs bienvenus via issues et pull requests.

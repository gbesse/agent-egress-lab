# agent-egress-lab

[Français](README.md) · [English](README.en.md) · [Español](README.es.md)

## Proyectos relacionados y señal original

- [browser-use](https://github.com/browser-use/browser-use) facilita los agentes de navegador. Su [incidencia #5216](https://github.com/browser-use/browser-use/issues/5216) señala una posible diferencia entre la descripción de la telemetría y los datos enviados. Es una **señal de necesidad**, no un problema que afirmemos haber reproducido.
- **Nuestro enfoque:** probar en CI si un agente Python envía un señuelo sintético a un destino de red. La herramienta no está integrada con browser-use y solo cubre llamadas Python instrumentadas.

Prueba de regresión de salida de red para agentes **Python**. Ejecuta un agente con un señuelo sintético: el informe enumera los destinos e indica si el señuelo apareció en un envío HTTP. El código de salida `2` hace fallar la CI ante una exposición o un destino prohibido.

## Inicio rápido

Python 3.11+, sin dependencias externas.

```bash
python3 egress_lab.py --canary SYNTHETIC-CANARY-123 --allow-host 127.0.0.1 -- python3 examples/leaky_agent.py
python3 -m unittest discover -s tests -v
```

La primera orden debe fallar con `canary_exposures > 0`: el ejemplo envía solamente el señuelo a un servidor local. Usa `--output report.json` para guardar el informe y repite `--allow-host` para definir destinos permitidos. Sin lista permitida, los destinos solo se observan.

## Alcance

La sonda se inyecta mediante `sitecustomize` en el proceso Python y en los subprocesos Python que heredan su entorno. Observa `socket.connect` y `http.client.HTTPConnection.send`. No cubre clientes nativos, procesos que no son Python ni todas las rutas de red. El informe no guarda los cuerpos de las solicitudes. Este prototipo es una prueba de regresión, no una barrera de seguridad.


Licencia MIT. Se aceptan incidencias y solicitudes de cambios para nuevos adaptadores.

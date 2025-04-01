# State of Health
PASTA and related services State of Health service

## Premises

1. All services are considered "up" unless proven otherwise.
1. Higher level services can imply that a lower level service is "up"

## Pixi Installation
1. Install pixi (see https://pixi.sh)
2. `cd soh`
3. `pixi init`
4. `pixi shell`
5. `pip install .`
6. `cd src/soh`
7. `python health_check.py <server>`

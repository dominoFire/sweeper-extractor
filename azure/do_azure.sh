#! /bin/bash

set -e

# NOTA: Asegurate de usar python3

python azure/pricing_vm_parser.py
python azure/parse_cloudharmony.py

# Necesitas tener instalado el paquete de azure personalizado (por ahora)
python azure/list_services.py

python azure/pricing_merge.py

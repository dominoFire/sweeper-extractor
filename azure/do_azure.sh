#! /bin/bash

# NOTA: Asegurate de usar python3

set -e

python azure/pricing_vm_parser.py
python azure/parse_cloudharmony.py

# Descarga los datos de azure
python azure/list_services.py

# Mezcla todos los datos generados
python azure/pricing_merge.py

# Dejamos los datos listos para la cubeta
python azure/prepare_sweeper.py

# Copiamos el archivo final
gsutil cp azure/data/configs.json gs://sweeper/configs/azure/configs.json

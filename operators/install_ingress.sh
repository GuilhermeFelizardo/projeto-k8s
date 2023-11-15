#!/bin/bash

# Caminhos para os scripts
SCRIPT_PYTHON="/Users/guilherme/projeto-k8s/operators/nginx-ingress-controller/install-nginx-ingress-controller.py"
SCRIPT_SH="/Users/guilherme/projeto-k8s/operators/nginx-ingress-controller/change_dns.sh"


# Executar o script Python
echo "Executando o script de instalação do NGINX Ingress Controller..."
python3 "$SCRIPT_PYTHON"

# Verificar se o script Python foi executado com sucesso
if [ $? -eq 0 ]; then
    echo "Instalação do NGINX Ingress Controller concluída. Prosseguindo para a alteração do DNS."
else
    echo "Falha na instalação do NGINX Ingress Controller. Abortando a alteração do DNS."
    exit 1
fi

# Executar o script shell
echo "Executando o script para alterar o DNS..."
bash "$SCRIPT_SH"

# Verificar se o script shell foi executado com sucesso
if [ $? -eq 0 ]; then
    echo "Alteração do DNS concluída com sucesso."
else
    echo "Falha na alteração do DNS."
    exit 1
fi

echo "Processo concluído."

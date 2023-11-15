#!/bin/bash

# Definir diretórios base
BASE_DIR="/Users/guilherme/projeto-k8s/operators"

# Executar scripts Python3
echo "Executando install-kubed.py"
python3 "$BASE_DIR/kubed/install-kubed.py"

echo "Executando cert-manager-iam-setup.py"
python3 "$BASE_DIR/cert-manager/cert-manager-iam-setup.py"

echo "Executando install-cert-manager.py"
python3 "$BASE_DIR/cert-manager/install-cert-manager.py"

# Aplicar arquivos YAML
echo "Aplicando cluster-issuer-route53.yaml"
kubectl apply -f "$BASE_DIR/cert-manager/resources/cluster-issuer-route53.yaml"

echo "Aplicando certificate.yaml"
kubectl apply -f "$BASE_DIR/cert-manager/resources/certificate.yaml"

echo "Processo concluído."

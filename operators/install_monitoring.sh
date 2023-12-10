#!/bin/bash

# Parar a execução se um comando falhar
set -e

# Definindo o diretório base
DIR_BASE="/Users/guilherme/projeto-k8s/operators"

# Executando os scripts Python em sequência
echo "Instalando kube-prometheus..."
python3 "$DIR_BASE/kube-prometheus/install-kube-prometheus.py"
python3 "$DIR_BASE/kube-prometheus/prometheus-rules/install-prometheus-rules.py"
python3 "$DIR_BASE/kube-prometheus/prometheus-service-monitor/install-prometheus-service-monitor.py"
python3 "$DIR_BASE/kube-prometheus/grafana-dashboards/install-grafana-dashboards.py"

echo "Instalando loki..."
python3 "$DIR_BASE/loki/install-loki.py"

echo "Instalando tempo..."
python3 "$DIR_BASE/tempo/install-tempo.py"

echo "Todos os scripts foram executados com sucesso."

#!/bin/bash

# Obter o endereço do Load Balancer
load_balancer_address=$(kubectl get svc -A | grep -i LoadBalancer | awk '{print $5}')

# Verificar se o endereço foi capturado
if [ -z "$load_balancer_address" ]; then
    echo "Endereço do Load Balancer não encontrado."
    exit 1
fi

# Executar o comando da AWS CLI com o endereço do Load Balancer
aws --no-cli-pager route53 change-resource-record-sets --hosted-zone-id Z06942553H9NBQ4TIUM5T --change-batch "{
  \"Changes\": [{
    \"Action\": \"UPSERT\",
    \"ResourceRecordSet\": {
      \"Name\": \"*.guilhermefreis.com\",
      \"Type\": \"CNAME\",
      \"TTL\": 300,
      \"ResourceRecords\": [{ \"Value\": \"$load_balancer_address\" }]
    }
  }]
}"

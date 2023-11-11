
# Instalação do Kube Prometheus via Helm

Este documento fornece instruções passo a passo para a instalação do Kube Prometheus usando Helm em um cluster Kubernetes.

## Pré-requisitos

- Um cluster Kubernetes configurado
- Helm instalado

## Adicionar Repositório Prometheus-Community ao Helm

Primeiro, adicione o repositório Prometheus-Community ao seu Helm:

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
```

## Criar Namespace

Crie um namespace chamado `monitoring` para a instalação do Prometheus:

```bash
kubectl create namespace monitoring
```

## Instalar ou Atualizar Kube Prometheus

Instale ou atualize o Kube Prometheus no namespace `monitoring` usando o comando a seguir. Certifique-se de ter um arquivo chamado `custom-values.yaml` com suas configurações personalizadas para o Kube Prometheus. Se não tiver este arquivo, o Prometheus será instalado com as configurações padrão:

```bash
helm install --upgrade prometheus prometheus-community/kube-prometheus-stack -n monitoring -f custom-values.yaml
```

## Verificação

Para verificar se o Kube Prometheus foi instalado ou atualizado corretamente, execute:

```bash
kubectl get pods -n monitoring
```

Você deve ver os pods do Kube Prometheus em execução no namespace `monitoring`.
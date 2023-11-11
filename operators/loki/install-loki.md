# Instalação do Loki via Helm

Este documento fornece instruções passo a passo para a instalação do Loki usando Helm em um cluster Kubernetes.

## Pré-requisitos

- Um cluster Kubernetes configurado
- Helm instalado

## Adicionar Repositório do Grafana ao Helm

Primeiro, adicione o repositório do Grafana, que contém o chart do Loki, ao seu Helm:

```bash
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
```

## Criar Namespace

É recomendado criar um namespace específico para o Loki. No exemplo abaixo, um namespace chamado `monitoring` é criado:

```bash
kubectl create namespace monitoring
```

## Instalar Loki

Com o repositório adicionado e o namespace criado, você pode instalar o Loki. Certifique-se de ter um arquivo chamado `custom-values.yaml` com suas configurações personalizadas para o Loki. Se você não tiver este arquivo, o Loki será instalado com as configurações padrão.

```bash
helm upgrade --install loki grafana/loki-stack -f custom-values.yaml -n monitoring
```

## Verificação

Após a instalação, você pode verificar se o Loki foi instalado corretamente com o seguinte comando:

```bash
kubectl get pods -n monitoring
```

Você deve ver os pods do Loki em execução no namespace `monitoring`.

# Projeto Kubernetes

Este repositório contém os recursos e scripts necessários para configurar e gerenciar um cluster Kubernetes. Ele inclui configurações para diversos operadores e ferramentas essenciais para um ambiente Kubernetes robusto e eficiente.

## Estrutura do Repositório

O repositório está organizado nas seguintes pastas e arquivos:

- `eksctl`: Contém os scripts de política e configuração para o EKS.
- `operators`: Diretório principal para os operadores Kubernetes.

### Operadores

Dentro do diretório `operators`, você encontrará:

- `cert-manager`: Scripts e documentação para instalar e configurar o cert-manager no Kubernetes.
- `kube-prometheus`: Recursos para instalar o Prometheus no Kubernetes, incluindo dashboards personalizados para o Grafana.
- `kubed`: Scripts para a instalação do Kubed.
- `loki`: Configurações e scripts para instalar o Loki, um agregador de logs.
- `not-ready`: Recursos ainda em desenvolvimento, incluindo configurações para o AWS ALB Ingress Controller, Karpenter e Nginx Ingress Controller.

## Como Usar

Cada pasta operador contém scripts Python (`install-<operador>.py`) e documentação (`install-<operador>.md`) para instalação e configuração. Siga as instruções em cada arquivo de documentação para configurar os operadores no seu cluster Kubernetes.

### Configuração Inicial

1. Configure seu cluster Kubernetes usando os recursos na pasta `eksctl`.
2. Escolha os operadores necessários na pasta `operators` e siga as instruções de instalação em cada subpasta.

## Licença

Este projeto é licenciado sob a Licença XYZ. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.


---

Este README oferece uma visão geral básica do projeto. Para detalhes específicos de cada componente, consulte a documentação correspondente nas subpastas.

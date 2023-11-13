# Instalação do NGINX Ingress Controller

Este script automatiza a instalação do NGINX Ingress Controller em um cluster Kubernetes usando Helm.

## Funcionalidades do Script

- O script instala o NGINX Ingress Controller em um namespace `nginx-ingress`.
- Utiliza o Helm para gerenciar a instalação.
- Aplica um arquivo de valores personalizados `custom-values.yaml`.

## Como Executar

1. Certifique-se de que o Helm está instalado e configurado no seu ambiente.
2. Coloque o arquivo `custom-values.yaml` no mesmo diretório do script.
3. Execute o script Python para instalar o NGINX Ingress Controller.

# Pré-requisitos
Python 3.x instalado.
Helm instalado e configurado.
Acesso ao cluster Kubernetes.
Customização
Você pode modificar o arquivo custom-values.yaml para personalizar a instalação do NGINX Ingress Controller conforme necessário.
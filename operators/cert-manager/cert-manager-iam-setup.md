# Script para Configuração do Cert-manager com Route 53

Este script Python é projetado para configurar uma IAM Role e uma política no AWS IAM, permitindo que o `cert-manager` no Kubernetes interaja com o AWS Route 53 para automação de certificados TLS/SSL.

## Funcionalidades do Script

O script executa as seguintes ações:

1. **Cria uma Política IAM**: Define e cria uma política IAM com permissões específicas para interagir com o Route 53.
2. **Obtém o OIDC Provider ARN**: Busca o ARN do provedor OIDC associado ao seu cluster EKS.
3. **Cria uma IAM Role com Trust Relationship**: Cria uma role IAM com uma política de trust relationship que permite a integração com o OIDC do EKS.
4. **Associa a Política à Role IAM**: Anexa a política IAM recém-criada à role IAM.

## Detalhes do Script

### Importação de Bibliotecas

O script utiliza `boto3` para interagir com o AWS IAM e EKS, e `subprocess` para executar comandos de sistema.

### Variáveis Iniciais

- `cluster_name`: Nome do seu cluster EKS.
- `role_name`: Nome desejado para a IAM Role.
- `namespace`: Namespace do Kubernetes onde o `cert-manager` está instalado.
- `service_account_name`: Nome da Service Account do Kubernetes usada pelo `cert-manager`.

### Funções Principais

- `get_oidc_endpoint(cluster_name)`: Retorna o endpoint OIDC do cluster EKS.
- `get_oidc_provider_arn(cluster_name)`: Obtém o ARN do provedor OIDC do cluster EKS.
- `create_iam_policy_and_role(...)`: Cria a política e a role IAM necessárias para a integração do `cert-manager` com o Route 53.

### Execução

Para executar o script, simplesmente rode-o em um ambiente Python com as credenciais da AWS configuradas. É necessário ter permissões apropriadas na AWS para criar roles e políticas no IAM.

## Pré-requisitos

- AWS CLI configurado com as credenciais apropriadas.
- Boto3 instalado (`pip install boto3`).
- Acesso ao Kubernetes e ao AWS com as permissões necessárias.

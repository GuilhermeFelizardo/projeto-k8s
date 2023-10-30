# Configuração de IAM para Karpenter no Amazon EKS

Este script foi desenvolvido para configurar as Roles e Policies necessárias para usar o Karpenter com um cluster Amazon EKS.

## Preparação

Antes de executar o script, assegure-se de ter o SDK da AWS (`boto3`) instalado e configurado com as credenciais adequadas.

## Como executar

1. Configure a variável `CLUSTER_NAME` com o nome do seu cluster EKS.
2. Execute o script: `python setup-iam-config.py`.

## Funções

### `get_aws_configurations()`

Recupera informações básicas do ambiente AWS, como Região, Endpoint OIDC do cluster EKS e ID da conta AWS.

### `create_karpenter_node_role()`

Cria a Role de nó para o Karpenter, que será assumida por instâncias EC2 lançadas pelo Karpenter.

### `attach_policies_to_role()`

Anexa políticas AWS necessárias à Role de nó do Karpenter.

### `create_and_associate_instance_profile()`

Cria um perfil de instância para o Karpenter e o associa à Role de nó.

### `create_karpenter_controller_role(oidc_endpoint, aws_account_id)`

Cria a Role de controle para o Karpenter, que o próprio Karpenter usará para fazer chamadas AWS em seu nome.

### `put_controller_policy(AWS_REGION, AWS_ACCOUNT_ID)`

Adiciona a política ao Controller Role, dando-lhe permissões para operar com EKS, EC2 e outros serviços necessários.

### `main()`

Função principal que chama as outras funções em sequência e configura o ambiente.

## Observações

O script verifica se a Role ou o Perfil de Instância já existem antes de tentar criá-los. Se eles já existirem, o script simplesmente imprimirá uma mensagem e continuará.

---

**Nota:** Esta documentação descreve o que cada função no script faz e como o script deve ser executado. Adapte conforme suas necessidades.


###

# Update aws-auth ConfigMap

- groups:
  - system:bootstrappers
  - system:nodes
  rolearn: arn:${AWS_PARTITION}:iam::${AWS_ACCOUNT_ID}:role/KarpenterNodeRole-${CLUSTER_NAME}
  username: system:node:{{EC2PrivateDNSName}}

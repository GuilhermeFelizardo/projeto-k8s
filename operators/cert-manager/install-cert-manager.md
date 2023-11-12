# Documentação: Cert-manager

## O que é Cert-manager?

Cert-manager é uma solução Kubernetes-native para automatizar a emissão e renovação de certificados TLS/SSL. Ele se integra com várias Autoridades Certificadoras (ACs), incluindo Let's Encrypt, para fornecer uma maneira automatizada de garantir que seus certificados estejam sempre atualizados.

## Instalando Cert-manager com Helm

A instalação do cert-manager usando Helm é um processo simples e recomendado para a gestão eficiente do cert-manager no Kubernetes. Siga os passos abaixo para instalar:

1. Adicione o repositório Helm do cert-manager:

   ```bash
   helm repo add jetstack https://charts.jetstack.io
   ```

2. Atualize a lista de repositórios Helm para garantir que você tenha as últimas versões disponíveis:

   ```bash
   helm repo update
   ```

3. Instale o cert-manager no seu cluster Kubernetes com a versão desejada, criando o namespace `cert-manager` e configurando os Custom Resource Definitions (CRDs) necessários:

   ```bash
   helm upgrade --install \
     cert-manager jetstack/cert-manager \
     --namespace cert-manager \
     --create-namespace \
     --version v1.13.2 \
     -f custom-values.yaml
   ```

   Certifique-se de que o arquivo `custom-values.yaml` esteja presente no diretório de onde você está executando o comando, pois ele contém configurações personalizadas para o cert-manager.

Após a execução desses comandos, o cert-manager estará instalado e pronto para uso no seu cluster Kubernetes.

## Configuração Adicional

Após a instalação, você pode configurar `ClusterIssuers` ou `Issuers` para emitir certificados, dependendo das suas necessidades e da configuração do seu cluster.

Nesta versão atualizada da documentação, os passos para instalar o `cert-manager` via Helm são detalhados, incluindo a adição do repositório, a atualização dos repositórios e o comando para instalar ou atualizar o `cert-manager`.

Para ver qual a ultima versão disponível, consultar "https://cert-manager.io/docs/installation/"


## Arquivos de Configuração Explicados

### ClusterIssuer

O arquivo `ClusterIssuer` é usado para definir uma entidade que pode emitir certificados. Aqui está uma breve explicação dos campos neste arquivo:

```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory # O endereço do servidor ACME
    email: guilherme_f.reis@hotmail.com # E-mail para registrar e recuperar credenciais perdidas
    privateKeySecretRef:
      name: letsencrypt-private-key # Secret que armazenará a chave de conta ACME
    solvers:
    - http01:
        ingress:
          class: nginx # Solver HTTP01 para provar a propriedade do domínio usando o ingress controller nginx
```

```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: guilherme_f.reis@hotmail.com
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
      - selector: # Solver R53
          dnsZones:
            - "guilhermefreis.com"
        dns01:
          route53:
            region: us-east-1
            hostedZoneID: Z06942553H9NBQ4TIUM5T
```

### Certificate

O arquivo `Certificate` é usado para solicitar um certificado a partir de um `Issuer` ou `ClusterIssuer`. Ele define para quais domínios você deseja um certificado, entre outros detalhes:

```yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: meu-certificado
  namespace: cert-manager
spec:
  secretName: meu-certificado-tls # Nome do Secret onde o certificado será armazenado
  secretTemplate:
    annotations:
      kubed.appscode.com/sync: "" # Annotation para sincronizar o Secret com Kubed
  issuerRef:
    name: letsencrypt # Referência ao ClusterIssuer definido anteriormente
    kind: ClusterIssuer
  dnsNames:
  - "guilhermefreis.com" # Domínio para o qual o certificado será emitido
```

---

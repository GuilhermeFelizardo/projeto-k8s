
---

# Documentação: Cert-manager

## O que é Cert-manager?

Cert-manager é uma solução Kubernetes-native para automatizar a emissão e renovação de certificados TLS/SSL. Ele se integra com várias Autoridades Certificadoras (ACs), incluindo Let's Encrypt, para fornecer uma maneira automatizada de garantir que seus certificados estejam sempre atualizados.

## Instalando Cert-manager

Para instalar o cert-manager em seu cluster Kubernetes:

```bash
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.1/cert-manager.yaml
```

Para ver qual a ultima versão disponível, consultar "https://cert-manager.io/docs/installation/"

Certifique-se de que `kubectl` esteja corretamente configurado e de que você possua permissões suficientes para instalar componentes no cluster.

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

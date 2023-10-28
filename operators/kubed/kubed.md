
---

# Documentação: Kubed

## O que é Kubed?

Kubed é um daemon para Kubernetes que oferece várias funcionalidades essenciais para lidar com clusters em produção. Entre estas funcionalidades, destacam-se a habilidade de manter ConfigMaps e Secrets sincronizados entre múltiplos namespaces, backup de ConfigMaps/Secrets em repositórios Git, detecção e notificação de eventos indesejados no cluster, e mais.

## Replicação de Secrets com Kubed

Um recurso bastante útil do Kubed é a sua capacidade de replicar automaticamente Secrets (e ConfigMaps) entre diferentes namespaces. Isso é especialmente valioso quando você precisa compartilhar uma configuração ou credenciais comuns por vários namespaces.

## Como Funciona?

Para replicar um Secret (ou ConfigMap) em todos os namespaces:

1. **Instalação do Kubed:** Certifique-se de que o Kubed esteja instalado e operacional em seu cluster.
2. **Adicionar Annotation:** Para replicar um Secret (ou ConfigMap), adicione a seguinte annotation:
   ```yaml
   kubed.appscode.com/sync: ""
   ```
3. **Criação/Atualização do Secret:** Crie ou atualize seu Secret (ou ConfigMap) com a annotation adicionada.
4. **Replicação Automática:** O Kubed irá automaticamente detectar essa annotation e iniciar a replicação do Secret para todos os outros namespaces no cluster.

## Exemplo

Imagine que você possui um Secret chamado `my-secret` no namespace `default` e quer replicá-lo em todos os outros namespaces.

1. **Adicione a Annotation ao Secret:**
   ```yaml
   apiVersion: v1
   kind: Secret
   metadata:
     name: my-secret
     namespace: default
     annotations:
       kubed.appscode.com/sync: ""
   data:
     password: [seu_dado_codificado_em_base64]
   ```

2. **Aplicando essa Configuração:** Após aplicar essa configuração, o Kubed identificará a annotation e replicará `my-secret` para todos os outros namespaces do cluster.

---

Este documento deve fornecer uma visão geral clara do funcionamento do Kubed, especialmente em relação à replicação de Secrets. Sinta-se à vontade para adaptar o conteúdo às necessidades e estilo da sua documentação.

---

# *network-setup.py** - Documentação

## **Objetivo**

O script `setup-network-config.py` tem como principal finalidade configurar automaticamente a rede do Karpenter em um cluster EKS. Fazendo uso das AWS SDKs, ele adiciona tags às subnets e security groups, facilitando a descoberta pelo Karpenter.

## **Requisitos**

- **Python** com a biblioteca **Boto3** instalada.
- Acesso à AWS com permissões adequadas para listar e descrever clusters EKS, nodegroups, launch templates e também para criar tags em subnets e security groups.

## **Configuração**

Antes de executar o script, é necessário definir o nome do seu cluster:

```python
CLUSTER_NAME = 'nome-do-seu-cluster'
```

## **Uso**

Para executar o script, use o seguinte comando:

```bash
$ python network-setup.py
```

## **Funcionalidades**

### **1. tag_subnets_for_karpenter_discovery(cluster_name)**

- **Descrição**: Adiciona a tag `karpenter.sh/discovery` às subnets associadas a cada nodegroup do cluster EKS especificado.
- **Finalidade**: Facilitar a descoberta destas subnets pelo Karpenter.

### **2. tag_security_groups_for_karpenter_discovery(cluster_name)**

- **Descrição**: Adiciona a tag `karpenter.sh/discovery` aos security groups associados ao primeiro nodegroup do cluster EKS ou ao launch template desse nodegroup.
- **Finalidade**: Facilitar a descoberta desses security groups pelo Karpenter.

## **Feedback ao Usuário**

Ao ser executado, o script fornecerá feedbacks em tempo real, informando sobre as tags adicionadas em cada subnet e security group.

---

import yaml
from kubernetes import client, config
import boto3

CLUSTER_NAME = 'production-cluster'
AWS_PARTITION = 'aws'

def get_aws_account_id():
    sts_client = boto3.client('sts')
    response = sts_client.get_caller_identity()
    return response['Account']

def load_kube_config():
    config.load_kube_config()

def get_aws_auth_configmap():
    v1 = client.CoreV1Api()
    return v1.read_namespaced_config_map(name="aws-auth", namespace="kube-system")

def role_entry_exists(map_roles, rolearn):
    """Verifica se uma entrada com o mesmo rolearn já existe."""
    for entry in map_roles:
        if entry.get("rolearn") == rolearn:
            return True
    return False

def update_aws_auth_configmap(configmap, new_role_entry):
    map_roles = []

    if 'mapRoles' in configmap.data:
        try:
            map_roles = yaml.safe_load(configmap.data['mapRoles'])
        except yaml.YAMLError:
            print("Erro ao deserializar mapRoles. Usando uma lista vazia.")

    # Verifica se a entrada já existe
    if not role_entry_exists(map_roles, new_role_entry["rolearn"]):
        map_roles.append(new_role_entry)
        configmap.data['mapRoles'] = yaml.safe_dump(map_roles, default_flow_style=False)

        v1 = client.CoreV1Api()
        v1.replace_namespaced_config_map(name="aws-auth", namespace="kube-system", body=configmap)
    else:
        print("A entrada já existe no ConfigMap e não será adicionada novamente.")

def main():
    AWS_ACCOUNT_ID = get_aws_account_id()
    # Constrói a nova entrada
    new_role_entry = {
        "groups": [
            "system:bootstrappers",
            "system:nodes"
        ],
        "rolearn": f"arn:{AWS_PARTITION}:iam::{AWS_ACCOUNT_ID}:role/KarpenterNodeRole-{CLUSTER_NAME}",
        "username": "system:node:{{EC2PrivateDNSName}}"
    }

    load_kube_config()
    configmap = get_aws_auth_configmap()
    update_aws_auth_configmap(configmap, new_role_entry)

    print("ConfigMap 'aws-auth' atualizado com sucesso!")

if __name__ == "__main__":
    main()

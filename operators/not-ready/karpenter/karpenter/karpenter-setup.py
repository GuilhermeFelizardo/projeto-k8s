import json
import subprocess
import yaml
import boto3

# Configurações iniciais
KARPENTER_VERSION = "v0.32.1"
CLUSTER_NAME = "production-cluster"  # Modifique para o nome do seu cluster, se necessário
AWS_PARTITION = "aws"

def get_aws_account_id():
    """Retorna o ID da conta AWS para o perfil atualmente conectado."""
    sts_client = boto3.client('sts')
    response = sts_client.get_caller_identity()
    return response['Account']

def run_command(command):
    """Executa um comando no shell."""
    subprocess.run(command, shell=True, check=True)

def modify_karpenter_yaml(nodegroup):
    """Modifica o arquivo karpenter.yaml para configurar a afinidade de nó."""
    with open('karpenter.yaml', 'r') as file:
        data = yaml.safe_load(file)

    # Modificar afinidade de nó aqui
    for item in data:
        if item['kind'] == 'Deployment' and item['metadata']['name'] == 'karpenter-controller':
            item['spec']['template']['spec']['affinity'] = {
                'nodeAffinity': {
                    'requiredDuringSchedulingIgnoredDuringExecution': {
                        'nodeSelectorTerms': [
                            {
                                'matchExpressions': [
                                    {
                                        'key': 'karpenter.sh/nodepool',
                                        'operator': 'DoesNotExist'
                                    },
                                    {
                                        'key': 'eks.amazonaws.com/nodegroup',
                                        'operator': 'In',
                                        'values': [nodegroup]
                                    }
                                ]
                            }
                        ]
                    }
                },
                'podAntiAffinity': {
                    'requiredDuringSchedulingIgnoredDuringExecution': [
                        {
                            'topologyKey': "kubernetes.io/hostname"
                        }
                    ]
                }
            }

    with open('karpenter.yaml', 'w') as file:
        yaml.safe_dump(data, file, default_flow_style=False)

def deploy_karpenter(AWS_ACCOUNT_ID, NODEGROUP):
    """Gera o arquivo de deployment do Karpenter e aplica as mudanças."""

    # # Gera o arquivo de deployment do Karpenter
    # run_command(f"helm template karpenter oci://public.ecr.aws/karpenter/karpenter --version {KARPENTER_VERSION} --namespace karpenter "
    #             f"--set settings.clusterName={CLUSTER_NAME} "
    #             f"--set serviceAccount.annotations.\"eks\\.amazonaws\\.com/role-arn\"=\"arn:{AWS_PARTITION}:iam::{AWS_ACCOUNT_ID}:role/KarpenterControllerRole-{CLUSTER_NAME}\" "
    #             f"--set controller.resources.requests.cpu=1 "
    #             f"--set controller.resources.requests.memory=1Gi "
    #             f"--set controller.resources.limits.cpu=1 "
    #             f"--set controller.resources.limits.memory=1Gi > karpenter.yaml")

    # # Modifica o arquivo karpenter.yaml
    # modify_karpenter_yaml(NODEGROUP)

    # Cria o namespace e CRDs do Karpenter, e aplica o arquivo karpenter.yaml
    run_command("kubectl create namespace karpenter")
    run_command(f"kubectl create -f https://raw.githubusercontent.com/aws/karpenter/{KARPENTER_VERSION}/pkg/apis/crds/karpenter.sh_nodepools.yaml")
    run_command(f"kubectl create -f https://raw.githubusercontent.com/aws/karpenter/{KARPENTER_VERSION}/pkg/apis/crds/karpenter.k8s.aws_ec2nodeclasses.yaml")
    run_command(f"kubectl create -f https://raw.githubusercontent.com/aws/karpenter/{KARPENTER_VERSION}/pkg/apis/crds/karpenter.sh_nodeclaims.yaml")
    run_command("kubectl apply -f karpenter.yaml")

def get_nodegroup_name():
    try:

        result = subprocess.run(["kubectl", "get", "nodes", "-o=jsonpath='{.items[0].metadata.labels.eks\\.amazonaws\\.com/nodegroup}'"], capture_output=True, text=True)
        nodegroup_name = json.loads(result.stdout)
        return nodegroup_name
    except Exception as e:
        raise ValueError("Não foi possível recuperar o nome do nodegroup. Certifique-se de que o rótulo eks.amazonaws.com/nodegroup está definido.") from e

def main():
    AWS_ACCOUNT_ID = get_aws_account_id()
    NODEGROUP = "your-nodegroup-name"  # Substitua pelo nome do seu nodegroup

    deploy_karpenter(AWS_ACCOUNT_ID, NODEGROUP)

    print("Karpenter configurado com sucesso!")

if __name__ == "__main__":
    main()

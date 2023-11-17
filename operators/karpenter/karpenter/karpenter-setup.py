import subprocess

def get_aws_account_id():
    return subprocess.check_output("aws sts get-caller-identity --query 'Account' --output text", shell=True).decode().strip()

def install_karpenter(karpenter_version, cluster_name, aws_partition, aws_account_id):
    command = (
        f"helm install karpenter oci://public.ecr.aws/karpenter/karpenter --version {karpenter_version} "
        f"--namespace karpenter --create-namespace --set settings.clusterName={cluster_name} "
        f"--set serviceAccount.annotations.\"eks\\.amazonaws\\.com/role-arn\"=\"arn:{aws_partition}:iam::{aws_account_id}:role/KarpenterControllerRole-{cluster_name}\" "
        f"--set controller.resources.requests.cpu=1 --set controller.resources.requests.memory=1Gi "
        f"--set controller.resources.limits.cpu=1 --set controller.resources.limits.memory=1Gi"
    )
    result = subprocess.run(command, shell=True, capture_output=True)
    if result.returncode != 0:
        print("Falha ao instalar/atualizar o Karpenter:", result.stderr.decode())
    else:
        print("Karpenter instalado/atualizado com sucesso.")

def main():
    karpenter_version = 'v0.32.1'
    cluster_name = 'production-cluster'
    aws_partition = 'aws'  # Ajuste conforme necessário
    aws_account_id = get_aws_account_id()

    install_karpenter(karpenter_version, cluster_name, aws_partition, aws_account_id)

if __name__ == '__main__':
    main()

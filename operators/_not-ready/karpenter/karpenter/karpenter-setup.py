import subprocess
import os

script_dir = os.path.dirname(os.path.abspath(__file__))

def get_aws_account_id():
    return subprocess.check_output("aws sts get-caller-identity --query 'Account' --output text", shell=True).decode().strip()

def install_karpenter(karpenter_version):
    custom_values_path = os.path.join(script_dir, 'custom-values.yaml')
    command = (
        f"helm install karpenter oci://public.ecr.aws/karpenter/karpenter --version {karpenter_version} "
        f"--namespace karpenter --create-namespace -f {custom_values_path}"
    )
    result = subprocess.run(command, shell=True, capture_output=True)
    if result.returncode != 0:
        print("Falha ao instalar/atualizar o Karpenter:", result.stderr.decode())
    else:
        print("Karpenter instalado/atualizado com sucesso.")

def main():
    karpenter_version = 'v0.32.1'

    install_karpenter(karpenter_version)

if __name__ == '__main__':
    main()

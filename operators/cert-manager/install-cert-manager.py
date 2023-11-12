import subprocess
import os

def run_command(command, error_message):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = process.communicate()
    if process.returncode != 0:
        print(error_message)
        print(f"Detalhes do erro: {err.decode('utf-8')}")
        return False
    return True

def install_cert_manager():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    custom_values_path = os.path.join(script_dir, 'custom-values.yaml')

    if not run_command("helm repo add jetstack https://charts.jetstack.io", "Erro ao adicionar o repositório jetstack."):
        return

    if not run_command("helm repo update", "Erro ao atualizar os repositórios do Helm."):
        return

    if not run_command(f"helm upgrade --install cert-manager jetstack/cert-manager --namespace cert-manager --create-namespace --version v1.13.2 -f {custom_values_path}", "Erro ao instalar o cert-manager com Helm."):
        return

    print("Cert-manager instalado com sucesso!")

if __name__ == "__main__":
    install_cert_manager()

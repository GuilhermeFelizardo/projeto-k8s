import subprocess

def run_command(command, error_message):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = process.communicate()
    if process.returncode != 0:
        print(error_message)
        print(f"Detalhes do erro: {err.decode('utf-8')}")
        return False
    return True

def install_kubed():
    if not run_command("helm repo add appscode https://charts.appscode.com/stable/", "Erro ao adicionar o repositório Appscode."):
        return

    if not run_command("helm repo update", "Erro ao atualizar os repositórios do Helm."):
        return

    if not run_command("helm install kubed appscode/kubed --version v0.13.2 --namespace kube-system", "Erro ao instalar o Kubed com Helm."):
        return

    print("Kubed instalado com sucesso!")

if __name__ == "__main__":
    install_kubed()
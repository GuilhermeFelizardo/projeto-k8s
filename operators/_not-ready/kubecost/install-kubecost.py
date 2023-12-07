import subprocess
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
namespace = "kubecost"

def run_command(command, error_message):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = process.communicate()
    if process.returncode != 0:
        print(f"{error_message}\nDetalhes: {err.decode('utf-8')}")
        return False, err.decode('utf-8')
    return True, out.decode('utf-8')

def install_or_upgrade_kubecost():
    success, _ = run_command("helm repo add kubecost https://kubecost.github.io/cost-analyzer/", "Erro ao adicionar o repositório kubecost.")
    if not success:
        return

    success, _ = run_command("helm repo update", "Erro ao atualizar os repositórios do Helm.")
    if not success:
        return

    custom_values_path = os.path.join(script_dir, 'custom-values.yaml')
    success, _ = run_command(f"helm upgrade --install kubecost kubecost/cost-analyzer --create-namespace -n {namespace} -f {custom_values_path}", "Erro ao instalar ou atualizar o Kubecost.")
    if not success:
        return

    print(f"Kubecost instalado ou atualizado com sucesso no namespace {namespace}!")

if __name__ == "__main__":
    install_or_upgrade_kubecost()

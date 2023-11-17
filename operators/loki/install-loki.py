import os
import subprocess

namespace = "monitoring"
script_dir = os.path.dirname(os.path.abspath(__file__))

def run_command(command, error_message):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = process.communicate()
    if process.returncode != 0:
        print(f"{error_message}\nDetalhes: {err.decode('utf-8')}")
        return False, err.decode('utf-8')
    return True, out.decode('utf-8')

def install_loki():
    success, _ = run_command("helm repo add grafana https://grafana.github.io/helm-charts", "Erro ao adicionar o repositório Grafana.")
    if not success:
        return

    success, _ = run_command("helm repo update", "Erro ao atualizar os repositórios do Helm.")
    if not success:
        return

    custom_values_path = os.path.join(script_dir, 'custom-values.yaml')
    success, _ = run_command(f"helm upgrade --install loki grafana/loki-stack --create-namespace -n {namespace} -f {custom_values_path}", "Erro ao instalar o Loki.")
    if not success:
        return

    print(f"Loki instalado com sucesso no namespace {namespace}!")

if __name__ == "__main__":
    install_loki()

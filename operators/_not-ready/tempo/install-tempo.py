import subprocess
import os

script_dir = os.path.dirname(os.path.abspath(__file__))

def run_command(command, error_message):
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError:
        print(error_message)
        return False
    return True

def install_tempo_helm_chart():
    # Adicionando o repositório Grafana
    if not run_command("helm repo add grafana https://grafana.github.io/helm-charts", "Erro ao adicionar o repositório Grafana."):
        return

    # Atualizando os repositórios Helm
    if not run_command("helm repo update", "Erro ao atualizar os repositórios do Helm."):
        return

    # Instalando o chart Tempo
    values_file_path = os.path.join(script_dir, 'custom-values.yaml')
    install_command = f"helm upgrade --install tempo grafana/tempo --namespace monitoring --version 1.6.3 --create-namespace -f {values_file_path}"
    if not run_command(install_command, "Erro ao instalar o chart Tempo com Helm."):
        return

    print("Chart Tempo instalado com sucesso.")

if __name__ == "__main__":
    install_tempo_helm_chart()

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
    # Adding the Grafana repository
    if not run_command("helm repo add grafana https://grafana.github.io/helm-charts", "Failed to add Grafana repository."):
        return

    # Updating Helm repositories
    if not run_command("helm repo update", "Failed to update Helm repositories."):
        return

    # Installing the Tempo chart
    values_file_path = os.path.join(script_dir, 'custom-values.yaml')
    install_command = f"helm upgrade --install tempo grafana/tempo --namespace monitoring --create-namespace -f {values_file_path}"
    if not run_command(install_command, "Failed to install the Tempo chart with Helm."):
        return

    print("Tempo chart successfully installed.")

if __name__ == "__main__":
    install_tempo_helm_chart()
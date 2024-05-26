import subprocess
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
namespace = "monitoring"

def run_command(command, error_message):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = process.communicate()
    if process.returncode != 0:
        print(f"{error_message}\nError details: {err.decode('utf-8')}")
        return False, err.decode('utf-8')
    return True, out.decode('utf-8')

def install_or_upgrade_prometheus():
    # Add Prometheus Community Helm repository
    success, _ = run_command("helm repo add prometheus-community https://prometheus-community.github.io/helm-charts", "Failed to add prometheus-community repository.")
    if not success:
        return

    # Update Helm repositories
    success, _ = run_command("helm repo update", "Failed to update Helm repositories.")
    if not success:
        return

    # Path to custom values file
    custom_values_path = os.path.join(script_dir, 'custom-values.yaml')

    # Install or upgrade Prometheus using Helm
    success, _ = run_command(f"helm upgrade --install prometheus prometheus-community/kube-prometheus-stack --create-namespace -n {namespace} -f {custom_values_path}", "Failed to install or upgrade Prometheus.")
    if not success:
        return

    print(f"Prometheus installed or upgraded successfully in the {namespace} namespace!")

if __name__ == "__main__":
    install_or_upgrade_prometheus()
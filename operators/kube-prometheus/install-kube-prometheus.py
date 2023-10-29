import subprocess
import os 

class KubePrometheusInstaller:

    def __init__(self, namespace="monitoring"):
        self.namespace = namespace
        self.script_dir = os.path.dirname(os.path.abspath(__file__))

    @staticmethod
    def run_command(command, error_message):
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = process.communicate()
        if process.returncode != 0:
            print(f"Detalhes: {err.decode('utf-8')}")
            return False, err.decode('utf-8')
        return True, out.decode('utf-8')

    def namespace_exists(self):
        success, _ = self.run_command(f"kubectl get namespaces {self.namespace}",
                                      "")
        return success

    def install_prometheus(self):
        success, _ = self.run_command("helm repo add prometheus-community https://prometheus-community.github.io/helm-charts",
                                      "Erro ao adicionar o repositório prometheus-community.")
        if not success:
            return

        success, _ = self.run_command("helm repo update",
                                      "Erro ao atualizar os repositórios do Helm.")
        if not success:
            return

        if not self.namespace_exists():
            print(f"Namespace {self.namespace} não existe. Criando...")
            success, _ = self.run_command(f"kubectl create namespace {self.namespace}",
                                          f"Erro ao criar o namespace {self.namespace}.")
            if success:
                print(f"Namespace {self.namespace} criado com sucesso!")

        custom_values_path = os.path.join(self.script_dir, 'custom-values.yaml')
        success, _ = self.run_command(f"helm install prometheus prometheus-community/kube-prometheus-stack -n {self.namespace} -f {custom_values_path}",
                                      "Erro ao instalar o Prometheus.")

        if not success:
            return

        print(f"Prometheus instalado com sucesso no namespace {self.namespace}!")

    def upgrade_prometheus(self):
        success, _ = self.run_command(f"helm upgrade prometheus prometheus-community/kube-prometheus-stack -n {self.namespace}",
                                      "Erro ao atualizar o Prometheus.")
        if not success:
            return

        print(f"Prometheus atualizado com sucesso no namespace {self.namespace}!")

if __name__ == "__main__":
    installer = KubePrometheusInstaller()
    installer.install_prometheus()
    # Para atualizar o Prometheus depois:
    # installer.upgrade_prometheus()

import os
import subprocess

class LokiInstaller:
    
    def __init__(self, namespace="monitoring"):
        self.namespace = namespace
        self.script_dir = os.path.dirname(os.path.abspath(__file__))

    @staticmethod
    def run_command(command, error_message):
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = process.communicate()
        if process.returncode != 0:
            print(f"{error_message}\nDetalhes: {err.decode('utf-8')}")
            return False, err.decode('utf-8')
        return True, out.decode('utf-8')

    def namespace_exists(self):
        success, _ = self.run_command(f"kubectl get namespaces {self.namespace}", "")
        return success

    def install_loki(self):
        success, _ = self.run_command("helm repo add grafana https://grafana.github.io/helm-charts", "Erro ao adicionar o repositório Grafana.")
        if not success:
            return

        success, _ = self.run_command("helm repo update", "Erro ao atualizar os repositórios do Helm.")
        if not success:
            return

        if not self.namespace_exists():
            print(f"Namespace {self.namespace} não existe. Criando...")
            success, _ = self.run_command(f"kubectl create namespace {self.namespace}", f"Erro ao criar o namespace {self.namespace}.")
            if success:
                print(f"Namespace {self.namespace} criado com sucesso!")

        custom_values_path = os.path.join(self.script_dir, 'custom-values.yaml')
        success, _ = self.run_command(f"helm upgrade --install loki grafana/loki-stack -f {custom_values_path} -n {self.namespace}", "Erro ao instalar o Loki.")

        if not success:
            return

        print(f"Loki instalado com sucesso no namespace {self.namespace}!")

if __name__ == "__main__":
    loki_installer = LokiInstaller()
    loki_installer.install_loki()

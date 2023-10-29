import subprocess

class KubedInstaller:
    
    def __init__(self):
        pass

    @staticmethod
    def run_command(command, error_message):
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = process.communicate()
        if process.returncode != 0:
            print(error_message)
            print(f"Detalhes do erro: {err.decode('utf-8')}")
            return False, ""
        return True, out.decode('utf-8')

    def install_kubed(self):
        success, _ = self.run_command("helm repo add appscode https://charts.appscode.com/stable/",
                                    "Erro ao adicionar o repositório appscode.")
        if not success:
            return

        success, _ = self.run_command("helm repo update",
                                    "Erro ao atualizar os repositórios do Helm.")
        if not success:
            return

        success, search_result = self.run_command("helm search repo appscode/kubed --version v0.12.0",
                                                "Erro ao procurar pela versão do kubed no repositório appscode.")
        if not success or "appscode/kubed" not in search_result:
            print("Versão especificada do kubed não encontrada no repositório appscode.")
            return

        success, _ = self.run_command("helm install kubed appscode/kubed --version v0.12.0 --namespace kube-system",
                                    "Erro ao instalar o kubed.")
        if not success:
            return

        print("Kubed instalado com sucesso!")


if __name__ == "__main__":
    installer = KubedInstaller()
    installer.install_kubed()
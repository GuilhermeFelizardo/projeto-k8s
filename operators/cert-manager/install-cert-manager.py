import subprocess

class CertManagerInstaller:
    
    def __init__(self):
        pass

    @staticmethod
    def run_command(command, error_message):
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = process.communicate()
        if process.returncode != 0:
            print(error_message)
            print(f"Detalhes do erro: {err.decode('utf-8')}")
            return False
        return True
    
    def install_cert_manager(self):
        if not self.run_command("kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.1/cert-manager.yaml",
                                "Erro ao instalar o cert-manager."):
            return

        print("Cert-manager instalado com sucesso!")

if __name__ == "__main__":
    installer = CertManagerInstaller()
    installer.install_cert_manager()

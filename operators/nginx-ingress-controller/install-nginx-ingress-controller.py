import subprocess
import os

def run_command(command, error_message):
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError:
        print(error_message)
        return False
    return True

def install_nginx_ingress():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    custom_values_path = os.path.join(script_dir, 'custom-values.yaml')

    # Adicionando o repositório nginx-stable
    if not run_command("helm repo add nginx-stable https://helm.nginx.com/stable", "Erro ao adicionar o repositório nginx-stable."):
        return

    # Atualizando os repositórios Helm
    if not run_command("helm repo update", "Erro ao atualizar os repositórios do Helm."):
        return

    # Instalando o NGINX Ingress Controller
    if not run_command(f"helm upgrade --install nginx-ingress nginx-stable/nginx-ingress --namespace nginx-ingress --create-namespace -f {custom_values_path}", "Erro ao instalar o NGINX Ingress Controller com Helm."):
        return

    print("NGINX Ingress Controller instalado com sucesso.")

if __name__ == "__main__":
    install_nginx_ingress()

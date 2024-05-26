Claro! Aqui está a documentação atualizada com os comandos do Helm para instalar o Reflector:

# Documentation: Reflector

## What is Reflector?

Reflector is a Kubernetes tool that facilitates the synchronization of Kubernetes resources across multiple namespaces. It ensures that resources such as Secrets and ConfigMaps are consistently replicated across different namespaces, allowing for easier management and maintenance of Kubernetes clusters.

## Installation with Helm

This section provides step-by-step instructions for installing Reflector using Helm in a Kubernetes cluster.

### Prerequisites

- A configured Kubernetes cluster
- Helm installed

### Add Emberstack Repository to Helm

First, add the Emberstack repository to your Helm:

```bash
helm repo add emberstack https://emberstack.github.io/helm-charts
```

### Update Helm Repositories

Next, update the Helm repositories to ensure you have the latest charts:

```bash
helm repo update
```

### Install Reflector

After adding and updating the repository, you can install Reflector in your desired namespace:

```bash
helm upgrade --install reflector emberstack/reflector --namespace kube-system
```

You can use the `install-reflector.py` script to perform the previous steps.

## Verification

To verify if Reflector has been installed correctly, run:

```bash
kubectl get pods -n kube-system
```

You should see the Reflector pods running in the specified namespace.

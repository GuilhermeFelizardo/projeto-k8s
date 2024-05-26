# Installing Grafana Tempo via Helm

This document provides step-by-step instructions for installing Grafana Tempo using Helm in a Kubernetes cluster.

## Add Grafana Repository to Helm

First, add the Grafana repository to your Helm:

```bash
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
```

## Install Grafana Tempo

With the repository added, you can proceed to install Grafana Tempo. Ensure you have a file named `custom-values.yaml` with your custom configurations for Tempo. If you do not have this file, Tempo will be installed with the default settings.

```bash
helm upgrade --install tempo grafana/tempo --create-namespace -n monitoring -f custom-values.yaml
```
You can use the `install-tempo.py` script to perform the previous steps.

## Verification

After installation, you can verify that Grafana Tempo has been correctly installed with the following command:

```bash
kubectl get pods -n monitoring
```

You should see the Tempo pods running in the `monitoring` namespace.

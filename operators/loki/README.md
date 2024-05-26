# Installing Loki via Helm

This document provides step-by-step instructions for installing Loki using Helm in a Kubernetes cluster.

## Add Grafana Repository to Helm

First, add the Grafana repository, which contains the Loki chart, to your Helm:

```bash
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
```

## Install Loki

With the repository added, you can proceed to install Loki. Ensure you have a file named `custom-values.yaml` with your custom configurations for Loki. If you do not have this file, Loki will be installed with the default settings.

```bash
helm upgrade --install loki grafana/loki-stack --create-namespace -n monitoring -f custom-values.yaml
```
You can use the `install-loki.py` script to perform the previous steps.

## Verification

After installation, you can verify that Loki has been correctly installed with the following command:

```bash
kubectl get pods -n monitoring
```

You should see the Loki pods running in the `monitoring` namespace.

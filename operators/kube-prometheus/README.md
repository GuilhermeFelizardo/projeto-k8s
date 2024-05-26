# Installing Kube Prometheus via Helm

This document provides step-by-step instructions for installing Kube Prometheus using Helm in a Kubernetes cluster.

## Add Prometheus-Community Repository to Helm

First, add the Prometheus-Community repository to your Helm:

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
```

## Install or Upgrade Kube Prometheus

Install or upgrade Kube Prometheus in the `monitoring` namespace using the following command. Make sure you have a file named `custom-values.yaml` with your custom configurations for Kube Prometheus. If you don't have this file, Prometheus will be installed with default configurations:

```bash
helm install --upgrade prometheus prometheus-community/kube-prometheus-stack --create-namespace -n monitoring -f custom-values.yaml
```

## Verification

To verify if Kube Prometheus has been installed or upgraded correctly, run:

```bash
kubectl get pods -n monitoring
```

You should see the Kube Prometheus pods running in the `monitoring` namespace.

You can use the `install-kube-prometheus.py` script to perform the previous steps.

# Managing Configurations in Kube Prometheus

## Overview

In your Kube Prometheus environment, configurations for Grafana dashboards, Prometheus rules, and service monitors are essential for customizing monitoring and visualization components. These configurations are often defined using ConfigMaps or custom resources, depending on the nature of the configuration. This structure enables you to extend Prometheus and Grafana capabilities to meet your specific monitoring needs.

## Directory Structure and File Explanation

- **kube-prometheus**
  - **grafana-dashboards**: Contains YAML files for custom Grafana dashboards.
    - `app-1-dashboard.yaml`: Defines a custom dashboard for a example application.
    - `loki-dashboard.yaml`: Provides a dashboard for visualizing logs collected by Loki.
  - **prometheus-rules**: Holds custom alerting and recording rules for Prometheus.
    - `high-memory-usage-rules.yaml`: Contains rules to alert on high memory usage.
    - `kubecost-cpu-usage-irate-rule.yaml`: Rules for monitoring CPU usage via Kubecost metrics.
    - `pods-evicted-rules.yaml`: Alerts when pods are evicted.
    - `pods-restart-rules.yaml`: Alerts when pods are restarted.
  - **prometheus-service-monitor**
    - `app-1.yaml`: ServiceMonitor configuration to scrape metrics from an example application.

## Configuration Details

### Grafana Dashboards

To create custom Grafana dashboards:
- Dashboards are defined in YAML files and must be loaded into Grafana as ConfigMaps.
- These dashboards can then be automatically detected and used by Grafana, assuming Grafana is configured to load dashboards from ConfigMaps.

### Prometheus Rules

Custom alerting and recording rules for Prometheus are also defined in YAML files and should be applied via PrometheusRule:
- These PrometheusRules are loaded by Prometheus, allowing for the extension of its alerting capabilities.

### Service Monitors

To monitor new services using Prometheus:
- A `ServiceMonitor` must be created for each service you want to monitor.
- This custom resource specifies how Prometheus should discover and scrape metrics from these services.

## Integration Features

This setup is pre-integrated with:
- **Loki**: For log aggregation and querying, enhancing observability with log data alongside metrics.
- **Kubecost**: For monitoring and managing Kubernetes cost efficiency directly from within Prometheus.
- **Example Application**: Demonstrates monitoring capabilities with a pre-configured service monitor.

By using these configurations, you can tailor your observability infrastructure to better fit your operational requirements and enhance your monitoring strategies.

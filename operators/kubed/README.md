# NOTE

**AT THE MOMENT APPSCODE REPO DONS'T HAVE KUBED IMAGE.**

# Documentation: Kubed

## What is Kubed?

Kubed is a Kubernetes daemon that offers various essential functionalities for managing clusters in production. Among these functionalities, it stands out for its ability to keep ConfigMaps and Secrets synchronized across multiple namespaces, backup ConfigMaps/Secrets to Git repositories, detect and notify of unwanted events in the cluster, and more.

## Secret Replication with Kubed

A highly useful feature of Kubed is its ability to automatically replicate Secrets (and ConfigMaps) across different namespaces. This is especially valuable when you need to share a common configuration or credentials across multiple namespaces.

## How Does it Work?

To replicate a Secret (or ConfigMap) across all namespaces:

1. **Kubed Installation:** Ensure that Kubed is installed and operational in your cluster.
2. **Adding Annotation:** To replicate a Secret (or ConfigMap), add the following annotation:
   ```yaml
   kubed.appscode.com/sync: ""
   ```
3. **Creating/Updating the Secret:** Create or update your Secret (or ConfigMap) with the added annotation.
4. **Automatic Replication:** Kubed will automatically detect this annotation and initiate the replication of the Secret to all other namespaces in the cluster.

## Example

Imagine you have a Secret named `my-secret` in the `default` namespace and you want to replicate it to all other namespaces.

1. **Add Annotation to the Secret:**
   ```yaml
   apiVersion: v1
   kind: Secret
   metadata:
     name: my-secret
     namespace: default
     annotations:
       kubed.appscode.com/sync: ""
   data:
     password: [your_data_encoded_in_base64]
   ```

2. **Applying this Configuration:** After applying this configuration, Kubed will identify the annotation and replicate `my-secret` to all other namespaces in the cluster.

Here's a Markdown document detailing the installation of Kubed via Helm:

# Installing Kubed via Helm

This document provides step-by-step instructions for installing Kubed using Helm in a Kubernetes cluster.

## Prerequisites

- A configured Kubernetes cluster
- Helm installed

## Add Appscode Repository to Helm

First, add the Appscode repository to your Helm:

```bash
helm repo add appscode https://charts.appscode.com/stable/
helm repo update
```

## Install Kubed

After adding and updating the repository, you can install Kubed. The installation will be done in the `kube-system` namespace:

```bash
helm install kubed appscode/kubed --version v0.13.2 --namespace kube-system
```

You can use the `install-kubed.py` script to perform the previous steps.


## Verification

To verify if Kubed has been installed correctly, run:

```bash
kubectl get pods -n kube-system
```

You should see the Kubed pods running in the `kube-system` namespace.
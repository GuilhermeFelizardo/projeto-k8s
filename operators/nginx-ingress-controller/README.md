# NGINX Ingress Controller Installation Guide

This guide provides step-by-step instructions for installing the NGINX Ingress Controller in a Kubernetes cluster using Helm.

## Installation Steps

1. **Add the nginx-stable Helm repository**:

   ```bash
   helm repo add nginx-stable https://helm.nginx.com/stable
   ```

2. **Update Helm repositories**:

   ```bash
   helm repo update
   ```

3. **Install the NGINX Ingress Controller**:

   ```bash
   helm upgrade --install nginx-ingress nginx-stable/nginx-ingress --namespace nginx-ingress --create-namespace -f custom-values.yaml
   ```

   Ensure that you replace `custom-values.yaml` with the path to your custom configuration file if you have one.
   
   You can use the `install-nginx-ingress-controller` script to perform the previous steps.

## Verification

To verify that the NGINX Ingress Controller has been successfully installed, you can use the following command:

```bash
kubectl get pods -n nginx-ingress
```

You should see the NGINX Ingress Controller pods running in the `nginx-ingress` namespace.

For more details on configuring and using the NGINX Ingress Controller, refer to the [official documentation](https://docs.nginx.com/nginx-ingress-controller/).
```

Feel free to adjust the README as needed to include any additional information or customization instructions.
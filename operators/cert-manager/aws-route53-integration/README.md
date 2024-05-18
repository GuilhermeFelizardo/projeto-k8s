# Script for Configuring Cert-manager with Route 53

This Python script is designed to configure an IAM Role and a policy in AWS IAM, allowing `cert-manager` in Kubernetes to interact with AWS Route 53 for TLS/SSL certificate automation.

## Script Features

The script performs the following actions:

1. **Creates an IAM Policy**: Defines and creates an IAM policy with specific permissions to interact with Route 53. This policy includes permissions for actions such as `route53:GetChange`, `route53:ChangeResourceRecordSets`, `route53:ListResourceRecordSets`, and `route53:ListHostedZonesByName`.

2. **Gets the OIDC Provider ARN**: Retrieves the ARN of the OIDC provider associated with your EKS cluster. This ARN is used to establish a trust relationship between the IAM role and the OIDC provider.

3. **Creates an IAM Role with Trust Relationship**: Creates an IAM role with a trust relationship policy allowing integration with EKS OIDC. This trust relationship enables the IAM role to assume the permissions of the Kubernetes service account used by `cert-manager`.

4. **Attaches the Policy to the IAM Role**: Attaches the newly created IAM policy to the IAM role. This ensures that the IAM role has the necessary permissions to interact with Route 53.

## Script Details

### Library Imports

The script utilizes `boto3` to interact with AWS IAM and EKS, and `subprocess` to execute system commands.

### Initial Variables

- `cluster_name`: Name of your EKS cluster.
- `role_name`: Desired name for the IAM Role.
- `namespace`: Kubernetes namespace where `cert-manager` is installed.
- `service_account_name`: Name of the Kubernetes Service Account used by `cert-manager`.

### Main Functions

- `get_oidc_endpoint(cluster_name)`: Returns the OIDC endpoint of the EKS cluster.
- `get_oidc_provider_arn(cluster_name)`: Obtains the ARN of the OIDC provider for the EKS cluster.
- `create_iam_policy_and_role(...)`: Creates the necessary IAM policy and role for `cert-manager` integration with Route 53.

### Execution

To run the script, simply execute it in a Python environment with AWS credentials configured. Appropriate permissions in AWS are required to create roles and policies in IAM.

## Prerequisites

- AWS CLI configured with appropriate credentials.
- Boto3 installed (`pip install boto3`).
- Access to Kubernetes and AWS with necessary permissions.

## Conclusion
The script initializes with the required variables such as the name of the EKS cluster, the desired IAM role name, the Kubernetes namespace where `cert-manager` is installed, and the name of the Kubernetes Service Account used by `cert-manager`.

Then, it defines a policy document that specifies the permissions required to interact with Route 53, including actions such as retrieving changes, modifying resource record sets, and listing hosted zones.

The script utilizes the `boto3` library to interact with AWS IAM and EKS. It includes functions to obtain the OIDC endpoint and the OIDC provider ARN associated with the EKS cluster. These values are crucial for establishing trust relationships between IAM roles and OIDC providers.

The `create_iam_policy_and_role(...)` function orchestrates the creation of an IAM policy and an IAM role. This function ensures that the IAM role has the necessary permissions defined by the IAM policy and establishes a trust relationship with the OIDC provider.

Overall, the script streamlines the setup process for enabling `cert-manager` to automate TLS/SSL certificate management with Route 53 in AWS.
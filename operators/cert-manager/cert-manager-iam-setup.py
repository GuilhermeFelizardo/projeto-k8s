import boto3
import json
import subprocess

cluster_name = 'production-cluster'

policy_document = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "route53:GetChange",
            "Resource": "arn:aws:route53:::change/*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "route53:ChangeResourceRecordSets",
                "route53:ListResourceRecordSets"
            ],
            "Resource": "arn:aws:route53:::hostedzone/*"
        },
        {
            "Effect": "Allow",
            "Action": "route53:ListHostedZonesByName",
            "Resource": "*"
        }
    ]
}

def get_oidc_endpoint(cluster_name):
    eks_client = boto3.client('eks')
    try:
        cluster_info = eks_client.describe_cluster(name=cluster_name)
        oidc_issuer = cluster_info['cluster']['identity']['oidc']['issuer']
        oidc_issuer = oidc_issuer.replace("https://", "")
        return oidc_issuer
    except Exception as e:
        print(f"Erro ao buscar o OIDC endpoint: {e}")
        return None

def get_oidc_provider_arn(cluster_name):
    eks_client = boto3.client('eks')
    try:
        cluster_info = eks_client.describe_cluster(name=cluster_name)
        oidc_issuer = cluster_info['cluster']['identity']['oidc']['issuer']
        account_id = get_account_id()
        oidc_provider_arn = f"arn:aws:iam::{account_id}:oidc-provider/oidc.eks.us-east-1.amazonaws.com/id/{oidc_issuer.split('/')[-1]}"
        return oidc_provider_arn
    except Exception as e:
        print(f"Erro ao buscar o OIDC provider ARN: {e}")
        return None

def create_iam_policy_and_role(role_name, policy_document, cluster_name, namespace, service_account_name):
    iam_client = boto3.client('iam')
    policy_name = f"{role_name}-policy"

    # Tenta criar a política
    try:
        iam_client.create_policy(
            PolicyName=policy_name,
            PolicyDocument=json.dumps(policy_document)
        )
        print(f"Política '{policy_name}' criada com sucesso.")
    except iam_client.exceptions.EntityAlreadyExistsException:
        print(f"A política '{policy_name}' já existe.")

    # Obtém o OIDC Provider ARN
    oidc_provider_arn = get_oidc_provider_arn(cluster_name)
    oidc_provider = get_oidc_endpoint(cluster_name)
    if not oidc_provider_arn:
        return

    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": "sts:AssumeRoleWithWebIdentity",
                "Principal": {
                    "Federated": oidc_provider_arn
                },
                "Condition": {
                    "StringEquals": {
                        f"{oidc_provider}:sub": f"system:serviceaccount:{namespace}:{service_account_name}"
                    }
                }
            }
        ]
    }

    # Tenta criar a role
    try:
        iam_client.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(trust_policy),
            Description="Role para integração com EKS OIDC"
        )
        print(f"Role '{role_name}' criada com sucesso.")

    except iam_client.exceptions.EntityAlreadyExistsException:
        print(f"A role '{role_name}' já existe.")

    policy_arn = f"arn:aws:iam::{get_account_id()}:policy/{policy_name}"
        
    iam_client.attach_role_policy(
        RoleName=role_name,
        PolicyArn=policy_arn
    )
    print(f"Política '{policy_name}' associada à role '{role_name}'.")

def get_account_id():
    sts_client = boto3.client('sts')
    return sts_client.get_caller_identity()["Account"]

if __name__ == "__main__":
    role_name = "cert-manager-r53"

    namespace = "cert-manager"
    service_account_name = "cert-manager"
    role_name = "cert-manager-r53"
    aws_account_id = get_account_id()

    iam_role =  f'arn:aws:iam::{aws_account_id}:role/{role_name}'

    create_iam_policy_and_role(role_name, policy_document, cluster_name, namespace, service_account_name)

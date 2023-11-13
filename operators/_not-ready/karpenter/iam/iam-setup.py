import boto3
import json
import botocore

CLUSTER_NAME = 'production-cluster'
AWS_PARTITION = 'aws'
iam_client = boto3.client('iam')
eks_client = boto3.client('eks')
sts_client = boto3.client('sts')


def get_aws_configurations():
    AWS_REGION = boto3.session.Session().region_name
    OIDC_ENDPOINT = eks_client.describe_cluster(name=CLUSTER_NAME)['cluster']['identity']['oidc']['issuer']
    AWS_ACCOUNT_ID = sts_client.get_caller_identity()['Account']

    return AWS_REGION, OIDC_ENDPOINT, AWS_ACCOUNT_ID


def create_karpenter_node_role():
    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {
                "Service": "ec2.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }]
    }

    try:
        iam_client.create_role(
            RoleName=f"KarpenterNodeRole-{CLUSTER_NAME}",
            AssumeRolePolicyDocument=json.dumps(trust_policy)
        )
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'EntityAlreadyExists':
            print(f"Role KarpenterNodeRole-{CLUSTER_NAME} já existe. Continuando...")
        else:
            raise e  # Se for um erro diferente, ele ainda será lançado.


def attach_policies_to_role():
    policies = [
        "AmazonEKSWorkerNodePolicy",
        "AmazonEKS_CNI_Policy",
        "AmazonEC2ContainerRegistryReadOnly",
        "AmazonSSMManagedInstanceCore"
    ]

    for policy in policies:
        iam_client.attach_role_policy(
            RoleName=f"KarpenterNodeRole-{CLUSTER_NAME}",
            PolicyArn=f"arn:{AWS_PARTITION}:iam::aws:policy/{policy}"
        )


def create_and_associate_instance_profile():
    try:
        iam_client.create_instance_profile(
            InstanceProfileName=f"KarpenterNodeInstanceProfile-{CLUSTER_NAME}"
        )
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'EntityAlreadyExists':
            print(f"Instance Profile KarpenterNodeInstanceProfile-{CLUSTER_NAME} já existe. Continuando...")
        else:
            raise e

def create_karpenter_controller_role(oidc_endpoint, aws_account_id):
    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {
                "Federated": f"arn:{AWS_PARTITION}:iam::{aws_account_id}:oidc-provider/{oidc_endpoint.lstrip('https://')}"
            },
            "Action": "sts:AssumeRoleWithWebIdentity",
            "Condition": {
                "StringEquals": {
                    f"{oidc_endpoint.lstrip('https://')}:aud": "sts.amazonaws.com",
                    f"{oidc_endpoint.lstrip('https://')}:sub": "system:serviceaccount:karpenter:karpenter"
                }
            }
        }]
    }

    try:
        iam_client.create_role(
            RoleName=f"KarpenterControllerRole-{CLUSTER_NAME}",
            AssumeRolePolicyDocument=json.dumps(trust_policy)
        )
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'EntityAlreadyExists':
            print(f"Role KarpenterControllerRole-{CLUSTER_NAME} já existe. Continuando...")
        else:
            raise e

def put_controller_policy(AWS_REGION, AWS_ACCOUNT_ID):
    controller_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Action": [
                    "ssm:GetParameter",
                    "ec2:DescribeImages",
                    "ec2:RunInstances",
                    "ec2:DescribeSubnets",
                    "ec2:DescribeSecurityGroups",
                    "ec2:DescribeLaunchTemplates",
                    "ec2:DescribeInstances",
                    "ec2:DescribeInstanceTypes",
                    "ec2:DescribeInstanceTypeOfferings",
                    "ec2:DescribeAvailabilityZones",
                    "ec2:DeleteLaunchTemplate",
                    "ec2:CreateTags",
                    "ec2:CreateLaunchTemplate",
                    "ec2:CreateFleet",
                    "ec2:DescribeSpotPriceHistory",
                    "pricing:GetProducts"
                ],
                "Effect": "Allow",
                "Resource": "*",
                "Sid": "Karpenter"
            },
            {
                "Action": "ec2:TerminateInstances",
                "Condition": {
                    "StringLike": {
                        "ec2:ResourceTag/karpenter.sh/provisioner-name": "*"
                    }
                },
                "Effect": "Allow",
                "Resource": "*",
                "Sid": "ConditionalEC2Termination"
            },
            {
                "Effect": "Allow",
                "Action": "iam:PassRole",
                "Resource": f"arn:{AWS_PARTITION}:iam::{AWS_ACCOUNT_ID}:role/KarpenterNodeRole-{CLUSTER_NAME}",
                "Sid": "PassNodeIAMRole"
            },
            {
                "Effect": "Allow",
                "Action": "eks:DescribeCluster",
                "Resource": f"arn:{AWS_PARTITION}:eks:{AWS_REGION}:{AWS_ACCOUNT_ID}:cluster/{CLUSTER_NAME}",
                "Sid": "EKSClusterEndpointLookup"
            }
        ]
    }


    iam_client.put_role_policy(
        RoleName=f"KarpenterControllerRole-{CLUSTER_NAME}",
        PolicyName=f"KarpenterControllerPolicy-{CLUSTER_NAME}",
        PolicyDocument=json.dumps(controller_policy)
    )


def main():
    AWS_REGION, OIDC_ENDPOINT, AWS_ACCOUNT_ID = get_aws_configurations()
    print(AWS_REGION, OIDC_ENDPOINT, AWS_ACCOUNT_ID)
   
    create_karpenter_node_role()
    attach_policies_to_role()
    create_and_associate_instance_profile()

    create_karpenter_controller_role(OIDC_ENDPOINT, AWS_ACCOUNT_ID)
    put_controller_policy(AWS_REGION, AWS_ACCOUNT_ID)

    print(f"Configuração para {CLUSTER_NAME} concluída!")

if __name__ == "__main__":
    main()
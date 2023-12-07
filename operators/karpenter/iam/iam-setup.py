import boto3
import json

# Configurações Iniciais
cluster_name = 'production-cluster'
aws_partition = 'aws'
aws_region = boto3.Session().region_name

# Cliente AWS
iam_client = boto3.client('iam')
sts_client = boto3.client('sts')
eks_client = boto3.client('eks')

# Funções
def get_account_id():
    return sts_client.get_caller_identity().get('Account')

def get_oidc_endpoint(cluster_name):
    return eks_client.describe_cluster(name=cluster_name)['cluster']['identity']['oidc']['issuer']

def create_karpenter_node_role(cluster_name, aws_partition):
    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {"Service": "ec2.amazonaws.com"},
            "Action": "sts:AssumeRole"
        }]
    }
    role_name = f"KarpenterNodeRole-{cluster_name}"
    create_role(iam_client, role_name, trust_policy)
    attach_policies_to_role(iam_client, role_name, [
        "AmazonEKSWorkerNodePolicy",
        "AmazonEKS_CNI_Policy",
        "AmazonEC2ContainerRegistryReadOnly",
        "AmazonSSMManagedInstanceCore"
    ])

def create_karpenter_controller_role(cluster_name, oidc_endpoint, aws_account_id, aws_partition, aws_region):
    oidc_hostpath = oidc_endpoint.split('//')[1]
    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {
                "Federated": f"arn:{aws_partition}:iam::{aws_account_id}:oidc-provider/{oidc_hostpath}"
            },
            "Action": "sts:AssumeRoleWithWebIdentity",
            "Condition": {
                "StringEquals": {
                    f"{oidc_hostpath}:aud": "sts.amazonaws.com",
                    f"{oidc_hostpath}:sub": "system:serviceaccount:karpenter:karpenter"
                }
            }
        }]
    }
    role_name = f"KarpenterControllerRole-{cluster_name}"
    create_role(iam_client, role_name, trust_policy)
    controller_policy = json.dumps({
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
                    "ec2:ResourceTag/karpenter.sh/nodepool": "*"
                }
            },
            "Effect": "Allow",
            "Resource": "*",
            "Sid": "ConditionalEC2Termination"
        },
        {
            "Effect": "Allow",
            "Action": "iam:PassRole",
            "Resource": f"arn:{aws_partition}:iam::{aws_account_id}:role/KarpenterNodeRole-{cluster_name}",
            "Sid": "PassNodeIAMRole"
        },
        {
            "Effect": "Allow",
            "Action": "eks:DescribeCluster",
            "Resource": f"arn:{aws_partition}:eks:{aws_region}:{aws_account_id}:cluster/{cluster_name}",
            "Sid": "EKSClusterEndpointLookup"
        },
        {
            "Sid": "AllowScopedInstanceProfileCreationActions",
            "Effect": "Allow",
            "Resource": "*",
            "Action": [
            "iam:CreateInstanceProfile"
            ],
            "Condition": {
            "StringEquals": {
                f"aws:RequestTag/kubernetes.io/cluster/{cluster_name}": "owned",
                "aws:RequestTag/topology.kubernetes.io/region": f"{aws_region}"
            },
            "StringLike": {
                "aws:RequestTag/karpenter.k8s.aws/ec2nodeclass": "*"
            }
            }
        },
        {
            "Sid": "AllowScopedInstanceProfileTagActions",
            "Effect": "Allow",
            "Resource": "*",
            "Action": [
            "iam:TagInstanceProfile"
            ],
            "Condition": {
            "StringEquals": {
                f"aws:ResourceTag/kubernetes.io/cluster/{cluster_name}": "owned",
                f"aws:ResourceTag/topology.kubernetes.io/region": f"{aws_region}",
                f"aws:RequestTag/kubernetes.io/cluster/{cluster_name}": "owned",
                f"aws:RequestTag/topology.kubernetes.io/region": f"{aws_region}"
            },
            "StringLike": {
                "aws:ResourceTag/karpenter.k8s.aws/ec2nodeclass": "*",
                "aws:RequestTag/karpenter.k8s.aws/ec2nodeclass": "*"
            }
            }
        },
        {
            "Sid": "AllowScopedInstanceProfileActions",
            "Effect": "Allow",
            "Resource": "*",
            "Action": [
            "iam:AddRoleToInstanceProfile",
            "iam:RemoveRoleFromInstanceProfile",
            "iam:DeleteInstanceProfile"
            ],
            "Condition": {
            "StringEquals": {
                f"aws:ResourceTag/kubernetes.io/cluster/{cluster_name}": "owned",
                f"aws:ResourceTag/topology.kubernetes.io/region": f"{aws_region}"
            },
            "StringLike": {
                "aws:ResourceTag/karpenter.k8s.aws/ec2nodeclass": "*"
            }
            }
        },
        {
            "Sid": "AllowInstanceProfileReadActions",
            "Effect": "Allow",
            "Resource": "*",
            "Action": "iam:GetInstanceProfile"
        }
    ]
    })
    iam_client.put_role_policy(
        RoleName=role_name,
        PolicyName=f"KarpenterControllerPolicy-{cluster_name}",
        PolicyDocument=controller_policy
    )

def delete_role(iam_client, role_name):
    try:
        # Desassociar políticas gerenciadas vinculadas à role
        policies = iam_client.list_attached_role_policies(RoleName=role_name)['AttachedPolicies']
        for policy in policies:
            iam_client.detach_role_policy(RoleName=role_name, PolicyArn=policy['PolicyArn'])

        # Excluir políticas in-line associadas à role
        inline_policies = iam_client.list_role_policies(RoleName=role_name)['PolicyNames']
        for policy_name in inline_policies:
            iam_client.delete_role_policy(RoleName=role_name, PolicyName=policy_name)

        # Remover a role de todos os perfis de instância associados
        instance_profiles = iam_client.list_instance_profiles_for_role(RoleName=role_name)['InstanceProfiles']
        for profile in instance_profiles:
            iam_client.remove_role_from_instance_profile(InstanceProfileName=profile['InstanceProfileName'], RoleName=role_name)

        # Excluir a role
        iam_client.delete_role(RoleName=role_name)
        print(f"Role {role_name} excluída com sucesso.")
    except Exception as e:
        print(f"Erro ao excluir a role {role_name}: {e}")


def create_role(iam_client, role_name, trust_policy):
    try:
        iam_client.get_role(RoleName=role_name)
        print(f"Role {role_name} já existe. Excluindo e criando novamente.")
        delete_role(iam_client, role_name)
    except iam_client.exceptions.NoSuchEntityException:
        pass  # Role não existe, pode prosseguir para criá-la

    try:
        iam_client.create_role(RoleName=role_name, AssumeRolePolicyDocument=json.dumps(trust_policy))
        print(f"Role {role_name} criada com sucesso.")
    except Exception as e:
        print(f"Erro ao criar a role {role_name}: {e}")

def attach_policies_to_role(iam_client, role_name, policy_names):
    for policy_name in policy_names:
        policy_arn = f"arn:{aws_partition}:iam::aws:policy/{policy_name}"
        iam_client.attach_role_policy(RoleName=role_name, PolicyArn=policy_arn)
        print(f"Política {policy_name} anexada ao role {role_name}.")

def main():
    aws_account_id = get_account_id()
    oidc_endpoint = get_oidc_endpoint(cluster_name)

    create_karpenter_node_role(cluster_name, aws_partition)
    create_karpenter_controller_role(cluster_name, oidc_endpoint, aws_account_id, aws_partition, aws_region)

if __name__ == '__main__':
    main()

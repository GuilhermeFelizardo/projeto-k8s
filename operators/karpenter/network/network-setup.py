import boto3

CLUSTER_NAME = 'production-cluster' 

# Crie os clientes boto3
eks_client = boto3.client('eks')
ec2_client = boto3.client('ec2')


def tag_subnets_for_karpenter_discovery(cluster_name):
    # 1. Listar Nodegroups de um Cluster EKS
    nodegroups = eks_client.list_nodegroups(clusterName=cluster_name)['nodegroups']

    # 2. Iterar sobre cada Nodegroup
    for nodegroup in nodegroups:
        # 3. Obter Subnets associadas a um Nodegroup
        subnets = eks_client.describe_nodegroup(clusterName=cluster_name, nodegroupName=nodegroup)['nodegroup']['subnets']

        # 4. Criar uma Tag para cada Subnet
        for subnet in subnets:
            ec2_client.create_tags(Resources=[subnet], Tags=[{'Key': 'karpenter.sh/discovery', 'Value': cluster_name}])
            print(f"Adicionada a tag 'karpenter.sh/discovery' com valor '{cluster_name}' à subnet {subnet}.")

def tag_security_groups_for_karpenter_discovery(cluster_name):
    # 1. Obter o primeiro nodegroup do cluster
    nodegroup = eks_client.list_nodegroups(clusterName=cluster_name)['nodegroups'][0]

    # 2. Obter o launch template associado ao nodegroup
    launch_template = eks_client.describe_nodegroup(clusterName=cluster_name, nodegroupName=nodegroup)['nodegroup']['launchTemplate']
    launch_template_id = launch_template['id']
    launch_template_version = launch_template['version']

    # 3. Decidir de qual fonte pegar os security groups
    # Se você usa apenas o Cluster security group
    security_groups_cluster = eks_client.describe_cluster(name=cluster_name)['cluster']['resourcesVpcConfig']['clusterSecurityGroupId']

    launch_template_data = ec2_client.describe_launch_template_versions(
        LaunchTemplateId=launch_template_id,
        Versions=[launch_template_version]
    )['LaunchTemplateVersions'][0]['LaunchTemplateData']
    
    # Se você usa os security groups do Launch template de um nodegroup gerenciado
    security_groups_launch_template = launch_template_data.get('NetworkInterfaces', [{}])[0].get('Groups', [])

    # Decidir qual usar - aqui estou usando um condicional para verificar se o launch template tem security groups. 
    # Se não, usará security_groups_cluster.
    security_groups = security_groups_launch_template if security_groups_launch_template else [security_groups_cluster]

    # 4. Adicionar a tag
    for sg in security_groups:
        ec2_client.create_tags(Resources=[sg], Tags=[{'Key': 'karpenter.sh/discovery', 'Value': cluster_name}])
        print(f"Adicionada a tag 'karpenter.sh/discovery' com valor '{cluster_name}' ao security group {sg}.")


if __name__ == "__main__":
    tag_subnets_for_karpenter_discovery(CLUSTER_NAME)
    print(f"\nTags adicionadas às subnets para {CLUSTER_NAME}!")

    tag_security_groups_for_karpenter_discovery(CLUSTER_NAME)
    print(f"\nTags adicionadas aos security groups para {CLUSTER_NAME}!")
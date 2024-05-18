export TAG=v0.32.1
export AWS_PARTITION=aws
export CLUSTER_NAME=production-cluster
export AWS_ACCOUNT_ID=022887457179

export CLUSTER_ENDPOINT="$(aws eks describe-cluster --name ${CLUSTER_NAME} --query "cluster.endpoint" --output text)"
export KARPENTER_IAM_ROLE_ARN="arn:${AWS_PARTITION}:iam::${AWS_ACCOUNT_ID}:role/${CLUSTER_NAME}-karpenter"

echo $CLUSTER_ENDPOINT $KARPENTER_IAM_ROLE_ARN

curl -fsSL https://raw.githubusercontent.com/aws/karpenter/"${KARPENTER_VERSION}"/website/content/en/preview/getting-started/getting-started-with-karpenter/cloudformation.yaml  > cf.yaml \
&& aws cloudformation deploy \
  --stack-name "Karpenter-${CLUSTER_NAME}" \
  --template-file "cf.yaml" \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides "ClusterName=${CLUSTER_NAME}"


editar kubeconfig:

- groups:
  - system:bootstrappers
  - system:nodes
  rolearn: arn:${AWS_PARTITION}:iam::${AWS_ACCOUNT_ID}:role/KarpenterNodeRole-${CLUSTER_NAME}
  username: system:node:{{EC2PrivateDNSName}}

eksctl utils associate-iam-oidc-provider --cluster=production-cluster --approve

eksctl create iamserviceaccount \
    --name karpenter \
    --namespace karpenter \
    --cluster ${CLUSTER_NAME} \
    --role-name ${CLUSTER_NAME}-karpenter \
    --attach-policy-arn arn:${AWS_PARTITION}:iam::${AWS_ACCOUNT_ID}:policy/KarpenterControllerPolicy-${CLUSTER_NAME} \
    --override-existing-serviceaccounts \
    --approve

helm registry logout public.ecr.aws

helm upgrade --install karpenter oci://public.ecr.aws/karpenter/karpenter --version ${TAG} --namespace karpenter --create-namespace \
  --set serviceAccount.annotations."eks\.amazonaws\.com/role-arn"=${KARPENTER_IAM_ROLE_ARN} \
  --set settings.clusterName=${CLUSTER_NAME} \
  --set settings.interruptionQueue=${CLUSTER_NAME} \
  --set controller.resources.requests.cpu=1 \
  --set controller.resources.requests.memory=250Mi \
  --set controller.resources.limits.cpu=1 \
  --set controller.resources.limits.memory=250Mi \
  --wait

<!-- kubectl apply -f https://raw.githubusercontent.com/aws/karpenter/v0.31.0/pkg/apis/crds/karpenter.sh_nodepools.yaml
kubectl apply -f https://raw.githubusercontent.com/aws/karpenter/v0.31.0/pkg/apis/crds/karpenter.sh_nodeclaims.yaml
kubectl apply -f https://raw.githubusercontent.com/aws/karpenter/v0.31.0/pkg/apis/crds/karpenter.k8s.aws_ec2nodeclasses.yaml
 -->

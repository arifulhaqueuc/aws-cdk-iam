from aws_cdk import (
    aws_iam as iam,
    core
)

class MyEksCdkStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create the IAM role for EKS node instances
        eks_node_instance_role = iam.Role(
            self,
            'MyEKSNodeInstanceRole',
            assumed_by=iam.ServicePrincipal('ec2.amazonaws.com'),
            role_name='MyEKSNodeInstanceRole'
        )

        # Attach necessary policies to the role
        policy_arns = [
            'arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy',
            'arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy',
            'arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly'
        ]

        for policy_arn in policy_arns:
            eks_node_instance_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name(policy_arn))

        # Create the IAM role for EKS Fargate pod execution
        eks_fargate_execution_role = iam.Role(
            self,
            'MyEKSFargatePodExecutionRole',
            assumed_by=iam.ServicePrincipal('eks-fargate-pods.amazonaws.com'),
            role_name='MyEKSFargatePodExecutionRole'
        )

        # Attach necessary policies to the role, such as AmazonEC2FullAccess, AmazonS3ReadOnlyAccess, etc.
        # Modify the policy_arns list with the policies you want to attach.

        policy_arns = [
            'arn:aws:iam::aws:policy/AmazonEC2FullAccess',
            'arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess'
        ]

        for policy_arn in policy_arns:
            eks_fargate_execution_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name(policy_arn))

        # Optionally, you can export the ARNs of the roles for future reference
        core.CfnOutput(self, 'EKSNodeInstanceRoleArn', value=eks_node_instance_role.role_arn)
        core.CfnOutput(self, 'EKSFargatePodExecutionRoleArn', value=eks_fargate_execution_role.role_arn)

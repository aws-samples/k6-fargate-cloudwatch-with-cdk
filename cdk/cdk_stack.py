import os

from aws_cdk import (
    Stack,
    aws_ecr,
    aws_ec2,
    aws_ecs,
    aws_ssm,
    aws_iam
)
from aws_cdk.aws_ecr_assets import DockerImageAsset
import cdk_ecr_deployment
from constructs import Construct


class CdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        repository = aws_ecr.Repository(self, id='custom-k6')

        image = DockerImageAsset(self, id='k6-image-with-custom-scripts',
                                 directory=os.path.join(os.path.dirname(__file__), '../k6-scripts'))

        cdk_ecr_deployment.ECRDeployment(self, id='DeployDockerImage',
                                         src=cdk_ecr_deployment.DockerImageName(image.image_uri),
                                         dest=cdk_ecr_deployment.DockerImageName(repository.repository_uri)
                                         )

        vpc = aws_ec2.Vpc(self, 'K6Vpc')

        cluster = aws_ecs.Cluster(self, 'K6Cluster', vpc=vpc)

        execution_role = aws_iam.Role(self, 'ecsTaskExecutionRole',
                                      assumed_by=aws_iam.ServicePrincipal('ecs-tasks.amazonaws.com'),
                                      managed_policies=[
                                          aws_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMReadOnlyAccess"),
                                          aws_iam.ManagedPolicy.from_aws_managed_policy_name(
                                              "CloudWatchAgentServerPolicy"),
                                          aws_iam.ManagedPolicy.from_aws_managed_policy_name(
                                              "service-role/AmazonECSTaskExecutionRolePolicy"),
                                      ]
                                      )
        task_definition = aws_ecs.TaskDefinition(self, 'K6Task', compatibility=aws_ecs.Compatibility.FARGATE,
                                                 cpu='1024',
                                                 memory_mib='2048',
                                                 execution_role=execution_role
                                                 )

        task_definition.task_role.add_managed_policy(aws_iam.ManagedPolicy
                                                     .from_aws_managed_policy_name("CloudWatchAgentServerPolicy"))

        task_definition.add_container('k6',
                                      image=aws_ecs.ContainerImage.from_ecr_repository(repository),
                                      logging=aws_ecs.LogDriver.aws_logs(stream_prefix=cluster.cluster_name)
                                      )

        ssm_parameter = aws_ssm.StringParameter(self, 'statsd-config', parameter_name='ecs-cwagent-sidecar-fargate',
                                                string_value="""
{
    "metrics": {
        "namespace": "k6",
        "metrics_collected": {
            "statsd": {
                "service_address": ":8125",
                "metrics_collection_interval": 5,
                "metrics_aggregation_interval": 0
            }
        }
    }
}
""")
        task_definition.add_container('cloudwatch-agent',
                                      image=aws_ecs.ContainerImage.from_registry("amazon/cloudwatch-agent:latest"),
                                      secrets={"CW_CONFIG_CONTENT": aws_ecs.Secret.from_ssm_parameter(ssm_parameter)},
                                      logging=aws_ecs.LogDriver.aws_logs(stream_prefix=cluster.cluster_name)
                                      )

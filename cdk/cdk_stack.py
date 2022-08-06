import os

from aws_cdk import (
    Stack,
    aws_ecr,
    aws_ec2,
    aws_ecs
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
        task_definition = aws_ecs.TaskDefinition(self, 'K6Task', compatibility=aws_ecs.Compatibility.FARGATE,
                                                 cpu='1024',
                                                 memory_mib='2048'
                                                 )

        task_definition.add_container('K6Container',
                                      image=aws_ecs.ContainerImage.from_ecr_repository(repository),
                                      logging=aws_ecs.LogDriver.aws_logs(stream_prefix=cluster.cluster_name)
                                      )

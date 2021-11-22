from aws_cdk import core as cdk
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_elasticloadbalancingv2 as elb2

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core


class DbStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str,
                 cluster: ecs.ICluster, sg_db: ec2.ISecurityGroup, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create a new Fargate task definition
        task_def = ecs.FargateTaskDefinition(self,
                                             "FargateWithCdkPart2TaskDef",
                                             memory_limit_mib=1024,
                                             cpu=256)
        container = task_def.add_container("FargateWithCdkPar2Container",
                                           image=ecs.ContainerImage.from_registry("postgres:13-alpine"),
                                           memory_limit_mib=1024,
                                           environment=["POSTGRES_PASSWORD=product_db","POSTGRES_DB=product_db"])
        port_map = ecs.PortMapping(container_port=5432,
                                   host_port=5432,
                                   protocol=ecs.Protocol.TCP)
        container.add_port_mappings(port_map)

        # Create a Fargate Service
        fg_service = ecs.FargateService(self,
                                        "FargateWithCdkPart2FGService",
                                        cluster=cluster,
                                        task_definition=task_def,
                                        security_groups=[sg_db],
                                        cloud_map_options=ecs.CloudMapOptions(cloud_map_namespace=cluster.default_cloud_map_namespace))

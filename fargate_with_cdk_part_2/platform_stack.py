from aws_cdk import core as cdk
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_elasticloadbalancingv2 as elb2

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core


class PlatformStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create a VPC
        vpc = ec2.Vpc(self,
                      "FargateWithCdkPart2VPC",
                      max_azs=2)

        # New ECS cluster in the VPC
        cluster = ecs.Cluster(self,
                              "FargateWithCdkPart2Cluster",
                              vpc=vpc)
        
        # Create a new Fargate task definition
        task_def = ecs.FargateTaskDefinition(self,
                                             "FargateWithCdkPart2TaskDef",
                                             memory_limit_mib=512,
                                             cpu=256)
        container = task_def.add_container("FargateWithCdkPar2Container",
                                           image=ecs.ContainerImage.from_registry("nginx"),
                                           memory_limit_mib=256)
        port_map = ecs.PortMapping(container_port=80,
                                   host_port=80,
                                   protocol=ecs.Protocol.TCP)
        container.add_port_mappings(port_map)

        # Create a Fargate Service
        fg_service = ecs.FargateService(self,
                                        "FargateWithCdkPart2FGService",
                                        cluster=cluster,
                                        task_definition=task_def)
        
        # Create a security group for the ALB
        sg_alb = ec2.SecurityGroup(self,
                                   "ALBSecurityGroup",
                                   vpc=vpc)

        # New ALB in the VPC
        elb = elb2.ApplicationLoadBalancer(self,
                                           "FargateWithCdkPar2ALB",
                                           vpc=vpc,
                                           internet_facing=True,
                                           security_group=sg_alb)

        # Add a listener to the ALB to listen on port 80
        listener = elb.add_listener("FargateWithCdkPart2Listener",
                                    port=80,
                                    open=True)
        listener.connections.allow_default_port_from_any_ipv4("From the internet")
        listener.add_targets("FargateWithCdkPart2Target",
                             port=80,
                             targets=[fg_service.load_balancer_target(container_name="FargateWithCdkPar2Container",
                                                                      container_port=80)])

        # Create an security group for API Service
        sg_api = ec2.SecurityGroup(self,
                                   "APISecurityGroup",
                                   description="Allow access to API Service",
                                   vpc=vpc)
        
        # Create a security group for DB service
        sg_db = ec2.SecurityGroup(self,
                                  "DBSecurityGroup",
                                  description="Allow access to DB Service",
                                  vpc=vpc)

        # Allow API service security group access the DB service on port 5432
        sg_db.connections.allow_from(sg_api,
                                     ec2.Port.tcp(5432),
                                     "Postgresql access")

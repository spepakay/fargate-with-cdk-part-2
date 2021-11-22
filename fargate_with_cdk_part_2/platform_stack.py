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
        self.cluster = ecs.Cluster(self,
                              "FargateWithCdkPart2Cluster",
                              vpc=vpc)
        
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

        # Create an security group for API Service
        sg_api = ec2.SecurityGroup(self,
                                   "APISecurityGroup",
                                   description="Allow access to API Service",
                                   vpc=vpc)
        
        # Create a security group for DB service
        self.sg_db = ec2.SecurityGroup(self,
                                  "DBSecurityGroup",
                                  description="Allow access to DB Service",
                                  vpc=vpc)

        # Allow API service security group access the DB service on port 5432
        self.sg_db.connections.allow_from(sg_api,
                                     ec2.Port.tcp(5432),
                                     "Postgresql access")

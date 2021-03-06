import setuptools


with open("README.md") as fp:
    long_description = fp.read()


setuptools.setup(
    name="fargate_with_cdk_part_2",
    version="0.0.1",

    description="An empty CDK Python app",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="author",

    package_dir={"": "fargate_with_cdk_part_2"},
    packages=setuptools.find_packages(where="fargate_with_cdk_part_2"),

    install_requires=[
        "aws-cdk.core==1.133.0",
        "aws-cdk.aws-ec2===1.133.0",
        "aws-cdk.aws-ecs===1.133.0",
        "aws-cdk.aws-elasticloadbalancingv2===1.133.0",
    ],

    python_requires=">=3.6",

    classifiers=[
        "Development Status :: 4 - Beta",

        "Intended Audience :: Developers",

        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",

        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",

        "Typing :: Typed",
    ],
)

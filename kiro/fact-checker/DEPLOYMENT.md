# Deployment Guide

## Prerequisites

- AWS CLI configured with appropriate credentials
- Finch installed
- Terraform installed

## Local Testing

Test the application locally before deploying:

```bash
./test-local.sh
```

Access at http://localhost:8080

Stop and remove the test container:
```bash
finch stop fact-checker-test
finch rm fact-checker-test
```

## Deploy to AWS ECS

The application will be deployed to:
- Region: eu-north-1
- Platform: AWS Fargate with ARM64 (Graviton)
- Access: Public Application Load Balancer

Run the deployment:

```bash
./deploy.sh
```

This script will:
1. Build the ARM64 container image
2. Create ECR repository
3. Push image to ECR
4. Deploy ECS infrastructure with Terraform
5. Output the public URL

## Architecture

- VPC with 2 public subnets across 2 AZs
- Application Load Balancer (public)
- ECS Fargate service with ARM64 tasks
- CloudWatch Logs for container logs
- SQLite database included in container

## Cleanup

To destroy all resources:

```bash
cd terraform
terraform destroy -auto-approve
```

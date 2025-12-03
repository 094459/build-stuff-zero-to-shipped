#!/bin/bash
set -e

REGION="eu-north-1"
APP_NAME="fact-checker"

echo "=== Building container image ==="
finch build --platform linux/arm64 -t ${APP_NAME}:latest .

echo "=== Initializing Terraform ==="
cd terraform
terraform init

echo "=== Creating ECR repository ==="
terraform apply -target=aws_ecr_repository.app -auto-approve

ECR_URL=$(terraform output -raw ecr_repository_url)
echo "ECR Repository: ${ECR_URL}"

echo "=== Tagging and pushing image to ECR ==="
cd ..
finch tag ${APP_NAME}:latest ${ECR_URL}:latest
finch push ${ECR_URL}:latest

echo "=== Deploying infrastructure ==="
cd terraform
terraform apply -auto-approve

echo "=== Deployment complete ==="
terraform output alb_url

---
inclusion: always
---

# Container Builds with Finch and Amazon ECR

This guide covers building, packaging, tagging, and pushing container images to Amazon ECR using Finch MCP tools.

## Overview

Kiro provides MCP tools for streamlined container operations:

- `mcp_Finch_finch_build_container_image` - Build container images with multi-architecture support
- `mcp_Finch_finch_push_image` - Push images to registries (automatically tags with image hash)
- `mcp_Finch_finch_create_ecr_repo` - Create ECR repositories if they don't exist

## Building Container Images

### Basic Build with MCP

Use the Finch MCP tool to build images:

```python
# Build a single architecture image
mcp_Finch_finch_build_container_image(
    dockerfile_path="/absolute/path/to/Dockerfile",
    context_path="/absolute/path/to/context",
    tags=["myapp:latest", "myapp:v1.0.0"]
)
```

### Multi-Architecture Builds

Build for both ARM64 and AMD64 architectures:

```python
# Build for multiple platforms
mcp_Finch_finch_build_container_image(
    dockerfile_path="/absolute/path/to/Dockerfile",
    context_path="/absolute/path/to/context",
    tags=["myapp:latest"],
    platforms=["linux/amd64", "linux/arm64"]
)
```

**Important**: Always build for both architectures when deploying to AWS:
- `linux/arm64` - For AWS Graviton instances (cost-effective, energy-efficient)
- `linux/amd64` - For standard EC2 instances (x86_64)

### Build Options

The MCP build tool supports various options:

```python
mcp_Finch_finch_build_container_image(
    dockerfile_path="/absolute/path/to/Dockerfile",
    context_path="/absolute/path/to/context",
    tags=["myapp:v1.0.0", "myapp:latest"],
    platforms=["linux/amd64", "linux/arm64"],
    build_contexts=["additional-context=/path/to/context"],
    target="production",  # Multi-stage build target
    no_cache=False,  # Set to True to disable cache
    pull=True,  # Always pull base images
    progress="auto"  # Options: auto, plain, tty
)
```

## Amazon ECR Workflow

### Complete ECR Deployment Workflow

1. **Create ECR Repository** (if needed)
2. **Build Multi-Architecture Image**
3. **Push to ECR**

### Step 1: Create ECR Repository

```python
# Create repository if it doesn't exist
mcp_Finch_finch_create_ecr_repo(
    repository_name="myapp",
    region="us-east-1"  # Optional, uses default AWS region if not specified
)
```

The tool will:
- Check if the repository exists
- Create it if it doesn't exist
- Return the repository URI
- Handle authentication automatically

### Step 2: Build for ECR

Build the image with ECR tags:

```python
# Build multi-arch image with ECR tags
mcp_Finch_finch_build_container_image(
    dockerfile_path="/absolute/path/to/Dockerfile",
    context_path="/absolute/path/to/context",
    tags=[
        "123456789012.dkr.ecr.us-east-1.amazonaws.com/myapp:latest",
        "123456789012.dkr.ecr.us-east-1.amazonaws.com/myapp:v1.0.0"
    ],
    platforms=["linux/amd64", "linux/arm64"]
)
```

### Step 3: Push to ECR

```python
# Push image to ECR (automatically tags with hash)
mcp_Finch_finch_push_image(
    image="123456789012.dkr.ecr.us-east-1.amazonaws.com/myapp:latest"
)
```

**Important**: The push tool automatically:
- Verifies ECR login configuration
- Gets the image hash
- Creates a new tag using the hash
- Pushes the image with the hash tag
- Handles authentication via ecr-login credential helper

## Tagging Strategy

### Recommended Tags

Always use multiple tags for flexibility:

```python
tags=[
    f"{ecr_uri}/myapp:latest",           # Latest stable version
    f"{ecr_uri}/myapp:v1.0.0",           # Semantic version
    f"{ecr_uri}/myapp:v1.0",             # Minor version
    f"{ecr_uri}/myapp:v1",               # Major version
    f"{ecr_uri}/myapp:{git_commit_sha}"  # Git commit for traceability
]
```

### Tag Naming Conventions

- **latest** - Most recent stable release
- **v1.0.0** - Semantic versioning (MAJOR.MINOR.PATCH)
- **dev** - Development builds
- **staging** - Staging environment
- **prod** - Production releases
- **{commit-sha}** - Git commit hash for exact traceability

## Dockerfile Best Practices

### Multi-Architecture Compatible Dockerfile

```dockerfile
# Use multi-arch base images
FROM python:3.11-slim

# Use build arguments for platform info
ARG TARGETPLATFORM
ARG BUILDPLATFORM
ARG TARGETARCH

# Set working directory
WORKDIR /app

# Copy requirements first (better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["python", "app.py"]
```

### Multi-Stage Build for Smaller Images

```dockerfile
# Build stage
FROM python:3.11-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Runtime stage
FROM python:3.11-slim

WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .

ENV PATH=/root/.local/bin:$PATH

CMD ["python", "app.py"]
```

### Platform-Specific Dependencies

```dockerfile
FROM python:3.11-slim

ARG TARGETARCH

# Install architecture-specific packages
RUN if [ "$TARGETARCH" = "arm64" ]; then \
      echo "Installing ARM64 optimized packages"; \
      apt-get update && apt-get install -y libarm-specific; \
    elif [ "$TARGETARCH" = "amd64" ]; then \
      echo "Installing AMD64 optimized packages"; \
      apt-get update && apt-get install -y libx86-specific; \
    fi

WORKDIR /app
COPY . .

CMD ["python", "app.py"]
```

## Complete Example Workflow

### Python Flask Application to ECR

```python
# Configuration
ecr_region = "us-east-1"
ecr_account = "123456789012"
repo_name = "flask-app"
version = "v1.0.0"
ecr_uri = f"{ecr_account}.dkr.ecr.{ecr_region}.amazonaws.com"

# Step 1: Ensure ECR repository exists
mcp_Finch_finch_create_ecr_repo(
    repository_name=repo_name,
    region=ecr_region
)

# Step 2: Build multi-architecture image
mcp_Finch_finch_build_container_image(
    dockerfile_path="/workspace/Dockerfile",
    context_path="/workspace",
    tags=[
        f"{ecr_uri}/{repo_name}:latest",
        f"{ecr_uri}/{repo_name}:{version}"
    ],
    platforms=["linux/amd64", "linux/arm64"],
    pull=True
)

# Step 3: Push to ECR
mcp_Finch_finch_push_image(
    image=f"{ecr_uri}/{repo_name}:latest"
)

mcp_Finch_finch_push_image(
    image=f"{ecr_uri}/{repo_name}:{version}"
)
```

## Authentication and Permissions

### ECR Authentication

The Finch MCP tools handle ECR authentication automatically using the ecr-login credential helper. Ensure:

1. AWS credentials are configured (via AWS CLI, environment variables, or IAM role)
2. The credential helper is configured in Finch
3. IAM permissions include:
   - `ecr:GetAuthorizationToken`
   - `ecr:BatchCheckLayerAvailability`
   - `ecr:PutImage`
   - `ecr:InitiateLayerUpload`
   - `ecr:UploadLayerPart`
   - `ecr:CompleteLayerUpload`

### Required IAM Policy

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ecr:GetAuthorizationToken"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "ecr:BatchCheckLayerAvailability",
        "ecr:PutImage",
        "ecr:InitiateLayerUpload",
        "ecr:UploadLayerPart",
        "ecr:CompleteLayerUpload",
        "ecr:DescribeRepositories",
        "ecr:CreateRepository"
      ],
      "Resource": "arn:aws:ecr:*:*:repository/*"
    }
  ]
}
```

## Best Practices

### Building

- **Always build for both architectures** - Use `platforms=["linux/amd64", "linux/arm64"]`
- **Use multi-stage builds** - Reduce final image size
- **Leverage build cache** - Order Dockerfile instructions from least to most frequently changing
- **Use .dockerignore** - Exclude unnecessary files from build context
- **Pin base image versions** - Use specific tags, not `latest`

### Tagging

- **Use semantic versioning** - Follow MAJOR.MINOR.PATCH format
- **Include git commit SHA** - For exact traceability
- **Tag multiple versions** - latest, v1.0.0, v1.0, v1
- **Use descriptive environment tags** - dev, staging, prod

### Pushing

- **Push with hash tags** - The MCP tool automatically creates hash-based tags
- **Verify push success** - Check the returned status and message
- **Push multiple tags** - Push both latest and version-specific tags
- **Use ECR for AWS deployments** - Reduces data transfer costs and latency

### Security

- **Scan images for vulnerabilities** - Use ECR image scanning
- **Use minimal base images** - alpine or slim variants
- **Don't include secrets** - Use environment variables or AWS Secrets Manager
- **Run as non-root user** - Add USER instruction in Dockerfile
- **Keep images updated** - Regularly rebuild with latest base images

## Troubleshooting

### Build Fails

- Check Dockerfile syntax
- Verify base images support multi-arch
- Ensure build context path is correct
- Check for platform-specific dependencies

### Push Fails

- Verify AWS credentials are configured
- Check IAM permissions for ECR
- Ensure ECR repository exists
- Verify image was built successfully

### Authentication Issues

- Run `aws sts get-caller-identity` to verify AWS credentials
- Check ecr-login credential helper configuration
- Verify IAM role has ECR permissions
- Ensure AWS region is correct

### Multi-Arch Issues

- Verify base images support both architectures
- Check for architecture-specific dependencies
- Use TARGETARCH build argument for conditional logic
- Test on both architectures when possible

## Additional Resources

- Use `mcp_Finch_finch_build_container_image` for all builds
- Use `mcp_Finch_finch_push_image` for pushing to registries
- Use `mcp_Finch_finch_create_ecr_repo` for ECR repository management
- Refer to Finch MCP server documentation for latest capabilities

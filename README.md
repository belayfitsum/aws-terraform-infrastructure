# AWS Terraform Infrastructure

Modular Terraform infrastructure for AWS deployments.

## Structure

```
├── environments/
│   ├── dev/          # Development environment
│   └── prod/         # Production environment
└── modules/
    ├── vpc/          # VPC networking
    ├── security/     # Security groups
    ├── compute/      # EC2 instances
    └── database/     # RDS databases
```

## Usage

### Development
```bash
cd environments/dev
terraform init
terraform plan
terraform apply
```

### Production
```bash
cd environments/prod
terraform init
terraform plan
terraform apply
```

## Modules

- **VPC**: Creates VPC, subnets, IGW, route tables
- **Security**: Security groups for EC2 and RDS
- **Compute**: EC2 instances with configurable specs
- **Database**: RDS PostgreSQL with backup and encryption
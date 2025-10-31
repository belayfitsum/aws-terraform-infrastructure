# Production Environment - High Availability
terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "eu-central-1"
  
  default_tags {
    tags = local.common_tags
  }
}

locals {
  project_name = "devops-api-prod"
  environment  = "production"
  # Updated for pipeline demo - infrastructure change
  
  common_tags = {
    Project     = local.project_name
    Environment = local.environment
    ManagedBy   = "Terraform"
    Purpose     = "Production"
  }
}

# VPC Module
module "vpc" {
  source = "../../modules/vpc"
  
  project_name = local.project_name
  common_tags  = local.common_tags
}

# Security Module
module "security" {
  source = "../../modules/security"
  
  project_name      = local.project_name
  vpc_id           = module.vpc.vpc_id
  allowed_ssh_cidrs = var.allowed_ssh_cidrs
  common_tags      = local.common_tags
}

# Compute Module
module "compute" {
  source = "../../modules/compute"
  
  project_name       = local.project_name
  instance_type      = "t3.medium"
  key_pair_name      = var.key_pair_name
  subnet_id          = module.vpc.public_subnet_id
  security_group_ids = [module.security.ec2_security_group_id]
  volume_size        = 20
  common_tags        = local.common_tags
}

# Database Module
module "database" {
  source = "../../modules/database"
  
  project_name            = local.project_name
  private_subnet_ids      = module.vpc.private_subnet_ids
  security_group_ids      = [module.security.rds_security_group_id]
  db_instance_class       = "db.t3.small"
  allocated_storage       = 100
  backup_retention_period = 30
  deletion_protection     = true
  skip_final_snapshot     = false
  db_name                 = var.db_name
  db_username             = var.db_username
  db_password             = var.db_password
  common_tags             = local.common_tags
}

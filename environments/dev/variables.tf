variable "key_pair_name" {
  description = "AWS Key Pair name for EC2 access"
  type        = string
  default     = "postgres"
}

variable "allowed_ssh_cidrs" {
  description = "CIDR blocks allowed for SSH access"
  type        = list(string)
  default     = ["0.0.0.0/0"] # CHANGE THIS TO YOUR IP!
}

variable "create_rds" {
  description = "Whether to create RDS instance (costs money)"
  type        = bool
  default     = false # Start with false for free tier
}

variable "db_name" {
  description = "Database name"
  type        = string
  default     = "apidb"
}

variable "db_username" {
  description = "Database username"
  type        = string
  default     = "postgres"
}

variable "db_password" {
  description = "Database password"
  type        = string
  sensitive   = true
  default     = "changeme123"
}
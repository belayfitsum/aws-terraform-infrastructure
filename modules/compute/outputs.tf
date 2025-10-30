output "instance_id" {
  description = "EC2 instance ID"
  value       = aws_instance.api_server.id
}

output "public_ip" {
  description = "EC2 public IP"
  value       = aws_instance.api_server.public_ip
}

output "private_ip" {
  description = "EC2 private IP"
  value       = aws_instance.api_server.private_ip
}
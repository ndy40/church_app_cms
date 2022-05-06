output "server_id" {
  value = digitalocean_droplet.church-cms.ipv4_address
}

output "db_password" {
  value = random_string.db_password.result
}

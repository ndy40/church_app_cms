
resource "digitalocean_droplet" "church-cms" {
  image  = "ubuntu-20-04-x64"
  name   = "church-cms-staging"
  region = "lon1"
  size   = "s-1vcpu-1gb"
  tags = ["staging", "testing", "terraform"]

  lifecycle {
    ignore_changes = [image]
  }

  ssh_keys = [
    data.digitalocean_ssh_key.terraform.id
  ]

  connection {
    host = self.ipv4_address
    user = "root"
    type = "ssh"
    private_key = var.pvt_key
    timeout = "2m"
  }

  provisioner "remote-exec" {
    inline = [
      "export PATH=$PATH:/usr/bin",
      "sudo apt-get update",
      "sudo add-apt-repository --yes --update ppa:ansible/ansible",
      "sudo apt -q -y install software-properties-common ansible"
    ]
  }

  provisioner "file" {
    source = "../ansible-playbook"
    destination = "/opt"
  }
}

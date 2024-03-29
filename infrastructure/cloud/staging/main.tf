resource "digitalocean_droplet" "church-cms" {
  image  = "ubuntu-20-04-x64"
  name   = "church-cms-staging"
  region = "lon1"
  size   = "s-1vcpu-1gb"
  tags = ["staging", "testing", "terraform"]

#  lifecycle {
#    ignore_changes = [image]
#  }

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
      "sudo apt update",
      "sudo add-apt-repository -y ppa:ansible/ansible",
      "sudo apt -y install software-properties-common ansible",
    ]
  }
}


resource "digitalocean_firewall" "cms_firewall" {
  name = "only-22-80-443-5432"

  droplet_ids = [digitalocean_droplet.church-cms.id]

  inbound_rule {
    protocol = "tcp"
    port_range = "22"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }

  inbound_rule {
    protocol = "tcp"
    port_range = "80"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }

  inbound_rule {
    protocol = "tcp"
    port_range = "443"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }

  outbound_rule {
    protocol = "tcp"
    port_range = "1-65535"
    destination_addresses = ["0.0.0.0/0", "::0/0"]
  }
}

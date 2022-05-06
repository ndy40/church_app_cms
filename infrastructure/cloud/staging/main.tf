
resource "random_string" "db_password" {
  length = 16
  min_special = 3
  min_upper = 3
}

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
      "sudo apt -y install software-properties-common python3-dev python3-pip",
      "python3 -m pip install -q --no-input ansible"
    ]
  }

  provisioner "file" {
    source = "../ansible-playbook"
    destination = "/opt"
  }

  provisioner "remote-exec" {
    connection {
      host = self.ipv4_address
      user = "root"
      type = "ssh"
      private_key = var.pvt_key
      timeout = "2m"
    }

    inline = [
      "ansible-playbook /opt/ansible-playbook/playbook.yml -e \"db_password=${random_string.db_password.result} \""
    ]
  }
}
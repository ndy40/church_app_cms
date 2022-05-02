terraform {
  cloud {
    organization = "church_cms"

    workspaces {
      name = "church_cms_staging"
    }
  }

  required_providers {
    digitalocean = {
      source = "digitalocean/digitalocean"
      version = "~> 2.0"
    }
  }
}

variable "do_token" {}
variable "pvt_key" {}

data "digitalocean_ssh_key" "terraform" {
  name = "church_cms_staging"
}

provider "digitalocean" {
  token = var.do_token
}

terraform {
  required_version = ">= 0.13"
  backend "local" {} 
  required_providers {
    yandex = {
      source  = "yandex-cloud/yandex"
    }
  }
}

provider "yandex" {
  folder_id = var.folder_id
  service_account_key_file = file("dtc-de-sa-key.json")
  storage_access_key = file("access-key")
  storage_secret_key = file("secret-key")
}

resource "yandex_storage_bucket" "data_lake_bucket" {
  bucket = "${local.data_lake_bucket}-${var.folder_id}"

  versioning {
    enabled = true
  }

  force_destroy = true

}

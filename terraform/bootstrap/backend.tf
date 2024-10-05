terraform {
  backend "gcs" {
    bucket = "dauphine-bucket"
    prefix = "terraform/tf-boostrap"
  }
}

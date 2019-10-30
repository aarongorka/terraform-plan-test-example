terraform {
  backend "s3" {
    bucket = "cmdlab-terraform-backend"
    key    = "my_important_application"
    region = "ap-southeast-2"
  }
}

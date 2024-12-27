provider "aws" {
  region = "us-west-2"
}

resource "aws_s3_bucket" "my_bucket" {
  bucket = "my-s3-bucket"
}

resource "aws_rds_instance" "my_rds" {
  allocated_storage    = 20
  engine               = "mysql"
  instance_class       = "db.t2.micro"
  name                 = "mydatabase"
  username             = "admin"
  password             = "password"
  parameter_group_name = "default.mysql5.7"
}

resource "aws_glue_catalog_database" "my_glue_database" {
  name = "mygluedatabase"
}

resource "aws_glue_catalog_table" "my_glue_table" {
  name          = "mygluetable"
  database_name = aws_glue_catalog_database.my_glue_database.name
}

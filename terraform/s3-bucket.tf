resource "aws_s3_bucket" "bucket" {
  bucket = "my-test-bucket-odessa2"
  acl = "private"
  tags = {
    Name = "My bucket"
  }
  versioning {
    enabled = true
  }
  lifecycle_rule {
    enabled = true
    transition {
      days = 40
      storage_class = "STANDARD_IA"
    }
    expiration {
      days = 60
    }
  }
}

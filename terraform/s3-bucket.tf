resource "aws_s3_bucket" "test-bucket" {
  bucket = "test-bucket-lyle"

  tags = {
    Name        = "My bucket"
    Environment = "Dev"
  }
}

resource "aws_s3_bucket_acl" "public-acl" {
  bucket = aws_s3_bucket.test-bucket.id
  acl    = "public-read"
}

resource "aws_s3_bucket_policy" "public_read_access" {
  bucket = aws_s3_bucket.test-bucket.id
  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Sid": "AllowPublicRead",
	    "Principal": "*",
      "Action": [ "s3:*" ],
      "Resource": [
        "${aws_s3_bucket.test-bucket.arn}",
        "${aws_s3_bucket.test-bucket.arn}/*"
      ]
    }
  ]
}
EOF
}

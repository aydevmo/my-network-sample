provider "aws" {
  region = var.aws_region
}

locals {
  package_url = "https://github.com/aydevmo/my-network-sample/raw/main/automation/terraform/terraform_ping_01/lambda_function.zip"
  downloaded  = "downloaded_package_${md5(local.package_url)}.zip"
}

resource "null_resource" "download_package" {
  triggers = {
    downloaded = local.downloaded
  }

  provisioner "local-exec" {
    command = "curl -L -o ${local.downloaded} ${local.package_url}"
  }
}

data "null_data_source" "downloaded_package" {
  inputs = {
    id       = null_resource.download_package.id
    filename = local.downloaded
  }
}

module "lambda_function_existing_package_from_remote_url" {
  source = "terraform-aws-modules/lambda/aws"

  function_name = "my-lambda-http-head-${var.aws_region}"
  description   = "Http latency evaluation"
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.9"

  create_package         = false
  local_existing_package = data.null_data_source.downloaded_package.outputs["filename"]
}

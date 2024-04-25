terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.46.0"
    }
  }
}

provider "aws" {
  region  = var.aws_region
  profile = "admin-1"
}

# VPC
resource "aws_vpc" "vpc" {
  cidr_block           = "10.0.0.0/16"
  instance_tenancy     = "default"
  enable_dns_hostnames = true

  tags = {
    Name = "url-shortener-cluster-vpc-iac"
  }
}

# Public subnets
resource "aws_subnet" "public_subnet_1" {
  vpc_id            = aws_vpc.vpc.id
  cidr_block        = "10.0.0.0/19"
  availability_zone = "ap-southeast-1a"

  tags = {
    Name = "url-shortener-cluster-vpc-subnet-public1-ap-southeast-1a-iac"
  }
}
resource "aws_subnet" "public_subnet_2" {
  vpc_id            = aws_vpc.vpc.id
  cidr_block        = "10.0.32.0/19"
  availability_zone = "ap-southeast-1b"

  tags = {
    Name = "url-shortener-cluster-vpc-subnet-public2-ap-southeast-1b-iac"
  }
}
resource "aws_subnet" "public_subnet_3" {
  vpc_id            = aws_vpc.vpc.id
  cidr_block        = "10.0.64.0/19"
  availability_zone = "ap-southeast-1c"

  tags = {
    Name = "url-shortener-cluster-vpc-subnet-public3-ap-southeast-1c-iac"
  }
}

# Private subnets
resource "aws_subnet" "private_subnet_1" {
  vpc_id            = aws_vpc.vpc.id
  cidr_block        = "10.0.128.0/19"
  availability_zone = "ap-southeast-1a"

  tags = {
    Name = "url-shortener-cluster-vpc-subnet-private1-ap-southeast-1a-iac"
  }
}
resource "aws_subnet" "private_subnet_2" {
  vpc_id            = aws_vpc.vpc.id
  cidr_block        = "10.0.160.0/19"
  availability_zone = "ap-southeast-1b"

  tags = {
    Name = "url-shortener-cluster-vpc-subnet-private2-ap-southeast-1b-iac"
  }
}
resource "aws_subnet" "private_subnet_3" {
  vpc_id            = aws_vpc.vpc.id
  cidr_block        = "10.0.192.0/19"
  availability_zone = "ap-southeast-1c"

  tags = {
    Name = "url-shortener-cluster-vpc-subnet-private3-ap-southeast-1c-iac"
  }
}


# Internet gateway
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.vpc.id

  tags = {
    Name = "url-shortener-cluster-vpc-igw-iac"
  }
}

# Elastic IPs
resource "aws_eip" "nat_gateway_1_eip" {
  domain = "vpc"
}

# Nat gateways
resource "aws_nat_gateway" "private_subnet_1_nat_gateway" {
  connectivity_type = "public"
  subnet_id = aws_subnet.private_subnet_1.id
  allocation_id = aws_eip.nat_gateway_1_eip.id

  tags = {
    Name = "url-shortener-nat-gateway-1"
  }

  # To ensure proper ordering, it is recommended to add an explicit dependency
  # on the Internet Gateway for the VPC.
  depends_on = [aws_internet_gateway.igw]
}

# Public subnet route table
resource "aws_route_table" "public_rtb" {
  vpc_id = aws_vpc.vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }

  tags = {
    Name = "url-shortener-cluster-vpc-rtb-public-iac"
  }
}

# Private subnet route tables
resource "aws_route_table" "private_rtb_1" {
  vpc_id = aws_vpc.vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_nat_gateway.private_subnet_1_nat_gateway.id
  }

  tags = {
    Name = "url-shortener-cluster-vpc-rtb-private1-ap-southeast-1a-iac"
  }
}
resource "aws_route_table" "private_rtb_2" {
  vpc_id = aws_vpc.vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_nat_gateway.private_subnet_1_nat_gateway.id
  }

  tags = {
    Name = "url-shortener-cluster-vpc-rtb-private2-ap-southeast-1b-iac"
  }
}
resource "aws_route_table" "private_rtb_3" {
  vpc_id = aws_vpc.vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_nat_gateway.private_subnet_1_nat_gateway.id
  }

  tags = {
    Name = "url-shortener-cluster-vpc-rtb-private3-ap-southeast-1c-iac"
  }
}

# Route associations
resource "aws_route_table_association" "public_subnet_1_public_rtb_association" {
  subnet_id      = aws_subnet.public_subnet_1.id
  route_table_id = aws_route_table.public_rtb.id
}
resource "aws_route_table_association" "public_subnet_2_public_rtb_association" {
  subnet_id      = aws_subnet.public_subnet_2.id
  route_table_id = aws_route_table.public_rtb.id
}
resource "aws_route_table_association" "public_subnet_3_public_rtb_association" {
  subnet_id      = aws_subnet.public_subnet_3.id
  route_table_id = aws_route_table.public_rtb.id
}
resource "aws_route_table_association" "private_subnet_1_private_rtb_association" {
  subnet_id      = aws_subnet.private_subnet_1.id
  route_table_id = aws_route_table.private_rtb_1.id
}
resource "aws_route_table_association" "private_subnet_2_private_rtb_association" {
  subnet_id      = aws_subnet.private_subnet_2.id
  route_table_id = aws_route_table.private_rtb_2.id
}
resource "aws_route_table_association" "private_subnet_3_private_rtb_association" {
  subnet_id      = aws_subnet.private_subnet_3.id
  route_table_id = aws_route_table.private_rtb_3.id
}
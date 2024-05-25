############################################################################################################
# Set Up
############################################################################################################

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.48.0"
    }
    kubernetes = {
      source = "hashicorp/kubernetes"
      version = "2.30.0"
    }
}
  
  backend "s3" {
    bucket         = "terraform-remote-state-url-shortener-service"
    key            = "global/s3/terraform.tfstate"
    region         = "ap-southeast-1"
    dynamodb_table = "terraform-remote-locks-url-shortener-service"
    encrypt        = true
    # profile        = "admin-1"
  }
}

provider "aws" {
  region = var.aws_region
#   profile = "admin-1"
}

############################################################################################################
# Data sources
############################################################################################################

data "aws_eks_cluster" "cluster" {
  name = var.cluster_name
}

data "aws_eks_node_group" "node_group" {
  cluster_name    = var.cluster_name
  node_group_name = var.node_group_name
}

data "aws_caller_identity" "current" {

}

data "aws_eks_cluster_auth" "cluster_auth" {
  name = var.cluster_name
}

############################################################################################################
# Create Deployment for url shortener service
############################################################################################################

provider "kubernetes" {
  host                   = data.aws_eks_cluster.cluster.endpoint
  cluster_ca_certificate = base64decode(data.aws_eks_cluster.cluster.certificate_authority.0.data)
  token                  = data.aws_eks_cluster_auth.cluster_auth.token
  # exec {
  #   api_version = "client.authentication.k8s.io/v1beta1"
  #   # args        = ["eks", "get-token", "--cluster-name", var.cluster_name, "--profile", "admin-1"]
  #   args    = ["eks", "get-token", "--cluster-name", var.cluster_name]
  #   command = "aws"
  # }
  # config_path = "/home/runner/.kube/config"
}

resource "kubernetes_deployment_v1" "url_shortener_deployment" {
  metadata {
    name      = "deployment-url-shortener"
    namespace = var.namespace
  }

  spec {
    replicas = 3

    selector {
      match_labels = {
        "app.kubernetes.io/name" = "app-url-shortener"
      }
    }

    template {
      metadata {
        labels = {
          "app.kubernetes.io/name" = "app-url-shortener"
        }
      }

      spec {
        container {
          image   = "271407076537.dkr.ecr.ap-southeast-1.amazonaws.com/url-shortener:${var.image_tag}"
          name    = "app-url-shortener"

          resources {
            limits = {
              cpu    = "0.5"
              memory = "512Mi"
            }
            requests = {
              cpu    = "250m"
              memory = "50Mi"
            }
          }

          env {
            name  = "PROD"
            value = "true"
          }

          env {
            name  = "POSTGRES_K8s_HOST"
            value = "host.docker.internal"
          }

          env {
            name  = "REDIS_K8s_HOST"
            value = "host.docker.internal"
          }

          port {
            container_port = 8000
          }
        }
      }
    }
  }
}

############################################################################################################
# Create Service for url shortener service
############################################################################################################

resource "kubernetes_service_v1" "url_shortener_service" {
  metadata {
    name = "service-url-shortener"
    namespace = var.namespace

    annotations = {
      "alb.ingress.kubernetes.io/healthcheck-port"     = "8000"
      "alb.ingress.kubernetes.io/healthcheck-path"     = "/url-shortener/docs"
      "alb.ingress.kubernetes.io/healthcheck-protocol" = "HTTP"
    }
  }
  spec {
    selector = {
      "app.kubernetes.io/name" = "app-url-shortener"
    }

    port {
      port        = 80
      target_port = 8080
      protocol    = "TCP"
    }

    type = "NodePort"
  }
}
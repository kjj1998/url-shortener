output "identity" {
  value = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:${replace(aws_eks_cluster.cluster.identity[0].oidc[0].issuer, "https://", "")}"
}

output "cluster_security_group" {
    value = aws_eks_cluster.cluster.vpc_config[0].cluster_security_group_id
}
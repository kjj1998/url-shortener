#!/bin/sh

account_id=$(aws sts get-caller-identity --query "Account" --output text)
echo $account_id
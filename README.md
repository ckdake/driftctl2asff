# driftctl2asff

Converts driftctl json output to AWS Security Hub asff format. Runnable as an AWS ECS Task via ECR.

This works, but you may want to customize it for your needs. PRs welcome.

https://docs.driftctl.com/0.35.0/usage/cmd/scan-usage#structure-1
https://docs.aws.amazon.com/securityhub/latest/userguide/securityhub-findings-format-syntax.html
https://docs.aws.amazon.com/securityhub/latest/userguide/asff-required-attributes.html

## TODO

* Terraform examples to get this up and running
* Tests
* Installable github action?
* Terraform module?

## Development

Open in VS Code as a remote container.

## Usage by hand

Assuming your default aws profile has the creds to scan, access tf state, and push to security hub:

driftctl scan --from tfstate+s3://my-bucket/path/to/state.tfstate --output json://data/real-output.json

python driftctl2asff.py 123456 us-west-2 data/real-output.json > asff.json

aws securityhub batch-import-findings --cli-input-json "$(<asff.json)"

## Usage automatically in AWS

1. Make sure you have an ECR repository set up, and that Github has the ability to push to it (Terraform example coming soon)
1. Take the `github-actions-ci-sample.yaml` as a template to make something in `.github/workflows/driftctl-ci.yaml`. Mind the veraibles towards the top!
1. Enjoy as you get an images pushed to ECR as a result of each PR merge to `main` wherever your infra-as-code lives, for driftctl.
1. Run this image as a scheduled job in ECS with the right permissions, and enjoy results of driftctl appearing in your Security Hub.(Terraform example coming soon)
1. Triage and fix all the wild things in your AWS tenant that should be ignored, or add them to code. 

# driftctl2asff

WIP!

Converts driftctl json output to AWS Security Hub asff format

https://docs.driftctl.com/0.35.0/usage/cmd/scan-usage#structure-1
https://docs.aws.amazon.com/securityhub/latest/userguide/securityhub-findings-format-syntax.html
https://docs.aws.amazon.com/securityhub/latest/userguide/asff-required-attributes.html

## Development

Open in VS Code as a remote container.

## Usage

Assuming your default aws profile has the creds to scan, access tf state, and push to security hub:

driftctl scan --from tfstate+s3://my-bucket/path/to/state.tfstate --output json://data/real-output.json

python driftctl2asff.py 123456 us-west-2 data/real-output.json > asff.json

aws securityhub batch-import-findings --cli-input-json "$(<asff.json)"

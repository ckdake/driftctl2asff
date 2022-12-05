#!/bin/bash
set -eou pipefail

eval "$(aws sts assume-role --role-arn arn:aws:iam::"${TARGET_ACCOUNT_ID}":role/${TARGET_ROLE_NAME} --role-session-name driftctl-run | jq -r '.Credentials | "export AWS_ACCESS_KEY_ID=\(.AccessKeyId)\nexport AWS_SECRET_ACCESS_KEY=\(.SecretAccessKey)\nexport AWS_SESSION_TOKEN=\(.SessionToken)\n"')"

echo "running driftctl"
cd /app/driftctl
DCTL_S3_REGION="us-west-2" \
/bin/driftctl scan --driftignore /app/.driftignore --from tfstate+s3://"${TARGET_S3_STATE_BUCKET}"/*.tfstate --output json://output.json --output console:// || true

echo "converting results to asff"
python3 /app/driftctl2asff.py "$TARGET_ACCOUNT_ID" us-west-2 output.json > asff.json

echo "uploading results to securityhub"
aws securityhub batch-import-findings --cli-input-json "$(<asff.json)"

echo "finished running driftctl"
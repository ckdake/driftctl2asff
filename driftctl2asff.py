import json
import sys
import copy
import hashlib

if len(sys.argv) != 4:
    raise ValueError('requires three args: aws account, aws region, and filename')

finding_aws_account = sys.argv[1]
finding_aws_region = sys.argv[2]
filename = sys.argv[3]

with open(filename) as f:
    data = json.load(f)

finding_date = data["date"]
finding_template = {
    "AwsAccountId": finding_aws_account,
    "CreatedAt": finding_date,
    "Description": "(boilerplate or specific)",
    "GeneratorId": "(rule/check/etc)",
    "Id": "(product-specific identifier)",
    "ProductArn" : "arn:aws:securityhub:"+finding_aws_region+":"+finding_aws_account+":product/"+finding_aws_account+"/default",
    "Resources" : [],
    "SchemaVersion" : "2018-10-08",
    "Severity": {
        "Label": "CRITICAL",
        "Original": "8.3"
    },
    "Title": "(boilerplate or specific)",
    "Types": ["AWS Security Best Practices"],
    "UpdatedAt" : finding_date
}

asff = {"Findings" : []}

# ignore managed: "list of resources found in IaC and in sync with remote"
# iterate through each "unmanaged" - list of resources found in remote but not in IaC
if data["unmanaged"]:
    for f in data["unmanaged"]:
        finding = copy.deepcopy(finding_template)
        finding["Description"] = f["type"] + " found in AWS Account but not in IaC"
        finding["GeneratorId"] = "driftctl/unmanaged-resource"
        finding["Id"] = finding_aws_region + "/" + finding_aws_account + "/" + str(hashlib.md5(bytes(f["id"], 'utf-8')).hexdigest())
        finding["Resources"] = [{
            "Type": f["type"],
            "Id": f["id"]
        }]
        finding["Severity"] = {
            "Label": "HIGH"
        }
        finding["Title"] = "Resource found in AWS Account but not in IaC"
        asff["Findings"].append(finding)

# iterate through each "missing" -  list of resources found in IaC but not on remote
if data["missing"]:
    for f in data["missing"]:
        finding = copy.deepcopy(finding_template)
        finding["Description"] = f["type"] + " found in IaC but not in AWS Account"
        finding["GeneratorId"] = "driftctl/missing-resource"
        finding["Id"] = finding_aws_region + "/" + finding_aws_account + "/" + str(hashlib.md5(bytes(f["id"], 'utf-8')).hexdigest())
        finding["Resources"] = [{
            "Type": f["type"],
            "Id": f["id"]
        }]
        finding["Severity"] = {
            "Label": "HIGH"
        }
        finding["Title"] = "Resource found in IaC but not in AWS Account"
        asff["Findings"].append(finding)

# iterate through each "differences" - A list of changes on managed resources
if data["differences"]:
    for f in data["differences"]:
        finding = copy.deepcopy(finding_template)
        finding["Description"] = f["res"]["type"] + " different between AWS Account and IaC"
        finding["GeneratorID"] = "driftctl/missing-resource"
        finding["Id"] = finding_aws_region + "/" + finding_aws_account + "/" + str(hashlib.md5(bytes(f["res"]["id"], 'utf-8')).hexdigest())
        finding["Resources"] = [{
            "Type": f["res"]["type"],
            "Id": f["res"]["id"]
        }]
        finding["Severity"] = {
            "Label": "HIGH"
        }
        finding["Title"] = "Resource different between AWS Account and IaC"
        asff["Findings"].append(finding)

print(json.dumps(asff, indent=4, sort_keys=True))

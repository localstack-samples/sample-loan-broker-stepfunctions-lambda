# Loan Broker application with AWS Step Functions, DynamoDB, Lambda, SQS, and SNS

| Key          | Value                                                                                 |
| ------------ | ------------------------------------------------------------------------------------- |
| Environment  | <img src="https://img.shields.io/badge/LocalStack-deploys-4D29B4.svg?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAKgAAACoABZrFArwAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAALbSURBVHic7ZpNaxNRFIafczNTGIq0G2M7pXWRlRv3Lusf8AMFEQT3guDWhX9BcC/uFAr1B4igLgSF4EYDtsuQ3M5GYrTaj3Tmui2SpMnM3PlK3m1uzjnPw8xw50MoaNrttl+r1e4CNRv1jTG/+v3+c8dG8TSilHoAPLZVX0RYWlraUbYaJI2IuLZ7KKUWCisgq8wF5D1A3rF+EQyCYPHo6Ghh3BrP8wb1en3f9izDYlVAp9O5EkXRB8dxxl7QBoNBpLW+7fv+a5vzDIvVU0BELhpjJrmaK2NMw+YsIxunUaTZbLrdbveZ1vpmGvWyTOJToNlsuqurq1vAdWPMeSDzwzhJEh0Bp+FTmifzxBZQBXiIKaAq8BBDQJXgYUoBVYOHKQRUER4mFFBVeJhAQJXh4QwBVYeHMQJmAR5GCJgVeBgiYJbg4T8BswYPp+4GW63WwvLy8hZwLcd5TudvBj3+OFBIeA4PD596nvc1iiIrD21qtdr+ysrKR8cY42itCwUP0Gg0+sC27T5qb2/vMunB/0ipTmZxfN//orW+BCwmrGV6vd63BP9P2j9WxGbxbrd7B3g14fLfwFsROUlzBmNM33XdR6Meuxfp5eg54IYxJvXCx8fHL4F3w36blTdDI4/0WREwMnMBeQ+Qd+YC8h4g78wF5D1A3rEqwBiT6q4ubpRSI+ewuhP0PO/NwcHBExHJZZ8PICI/e73ep7z6zzNPwWP1djhuOp3OfRG5kLROFEXv19fXP49bU6TbYQDa7XZDRF6kUUtEtoFb49YUbh/gOM7YbwqnyG4URQ/PWlQ4ASllNwzDzY2NDX3WwioKmBgeqidgKnioloCp4aE6AmLBQzUExIaH8gtIBA/lFrCTFB7KK2AnDMOrSeGhnAJSg4fyCUgVHsolIHV4KI8AK/BQDgHW4KH4AqzCQwEfiIRheKKUAvjuuu7m2tpakPdMmcYYI1rre0EQ1LPo9w82qyNziMdZ3AAAAABJRU5ErkJggg=="> <img src="https://img.shields.io/badge/AWS-deploys-F29100.svg?logo=amazon">                                                                     |
| Services     | Step Functions, SQS, SNS, Lambda, DynamoDB, EventBridge                                 |
| Integrations | CDK, AWS CLI                                                                            |
| Categories   | Serverless; Event-Driven architecture                                                   |
| Level        | Intermediate                                                                            |
| GitHub       | [Repository link](https://github.com/localstack/loan-broker-stepfunctions-lambda-app)   |

## Introduction

The Loan Broker application with AWS Step Functions, DynamoDB, Lambda, SQS, and SNS demonstrates Gregor Hohpe's [Loan Broker example](https://www.enterpriseintegrationpatterns.com/ramblings/loanbroker_stepfunctions.html). The sample application implements a [Recipient List](https://www.enterpriseintegrationpatterns.com/patterns/messaging/RecipientList.html) pattern and a [Scatter Gather](https://www.enterpriseintegrationpatterns.com/patterns/messaging/RecipientList.html) pattern to retrieve a list of banks and dynamically route loan application to multiple banks respectively. The sample application implements the following integration among the various AWS services:

- User submits a loan application with personal data, desired terms, loan amount, and duration.
- Loan Broker fetches information from Credit Bureau and adds it to the loan application submitted earlier.
- Loan Broker routes the application to multiple banks, and the banks reply if they are willing to offer.
- Loan Broker aggregates all the result(s) and returns the result(s) to the user.

Users can deploy this application on LocalStack and AWS with no changes using Cloud Development Kit (CDK). To test this application sample, we will demonstrate how you use LocalStack to deploy the infrastructure on your developer machine and your CI environment. Furthermore, we will showcase how you can use Cloud Pods Launchpad to inject a Cloud Pod into your running LocalStack container to test the application without creating your infrastructure again!

## Prerequisites

- LocalStack Pro with the [`localstack` CLI](https://docs.localstack.cloud/getting-started/installation/#localstack-cli).
- [Cloud Development Kit](https://docs.localstack.cloud/user-guide/integrations/aws-cdk/) with the [`cdklocal`](https://www.npmjs.com/package/aws-cdk-local) installed.
- [AWS CLI](https://docs.localstack.cloud/user-guide/integrations/aws-cli/) with the [`awslocal` wrapper](https://docs.localstack.cloud/user-guide/integrations/aws-cli/#localstack-aws-cli-awslocal).

Start LocalStack Pro with the `LOCALSTACK_API_KEY` pre-configured:

```shell
export LOCALSTACK_API_KEY=<your-api-key>
DEBUG=1 localstack start
```

We specified DEBUG=1 to get the printed LocalStack logs directly in the terminal to help us see the event-driven architecture in action. If you prefer running LocalStack in detached mode, you can add the `-d` flag to the `localstack start` command, and use Docker Desktop to view the logs.

## Instructions

You can build and deploy the sample application on LocalStack by running our `Makefile` commands. To deploy the infrastructure, you can run `make deploy` and `make run` after installing the application dependencies. Here are instructions to deploy and test it manually step-by-step.

### Deploying the application

To create the AWS infrastructure locally, you can use CDK and our `cdklocal` wrapper. Before you can deploy the infrastructure, you need to install the application dependencies:

```sh
yarn
```

To deploy the infrastructure, you can run the following command:

```sh
cdklocal bootstrap
cdklocal deploy --all
```

This will deploy the `LoanBroker-RecipientList-Stack` and `LoanBroker-PubSub-Stack` stacks. You will see the following output:

```sh
Outputs:
LoanBroker-RecipientList-Stack.LoanBrokerArn = arn:aws:states:us-east-1:000000000000:stateMachine:LoanBroker-RecipientList-Stack-LoanBroker641FC9A8-dd79232c
Stack ARN:
arn:aws:cloudformation:us-east-1:000000000000:stack/LoanBroker-RecipientList-Stack/e7929928
```

Take a note of the `LoanBroker-RecipientList-Stack.LoanBrokerArn` output. You will need it to test the application.

## Testing the application

Before you can test the application, you need to pre-populate the `LoanBrokerBanksTable` for the `RecipientsList` stack:

```sh
awslocal dynamodb put-item \
    --table-name=LoanBrokerBanksTable \
    --item='{ "Type": { "S": "Home" }, "BankAddress": {"L": [ { "S": "BankRecipientPremium" }, { "S": "BankRecipientUniversal" }, { "S": "BankRecipientPawnshop" } ] } }'
```

Start the State Machine execution by running the following command:

```sh
awslocal stepfunctions start-execution \
    --name=cli-test-run \
    --state-machine-arn=<STATE_MACHINE_ARN> \
    --input="{\"SSN\": \"123-45-6789\", \"Amount\": 500000, \"Term\": 30 }"
```

Replace `<STATE_MACHINE_ARN>` with the `LoanBroker-RecipientList-Stack.LoanBrokerArn` output from the previous step. The result will contain the Execution ARN and the start date:

```sh
{
    "executionArn": "arn:aws:states:us-east-1:000000000000:execution:LoanBroker-RecipientList-Stack-LoanBroker641FC9A8-dd79232c:cli-test-run",
    "startDate": "2023-04-24T21:08:35.434000+05:30"
}
```

You can use the Execution ARN to see the output of the State Machine execution:

```sh
awslocal stepfunctions describe-execution \
    --execution-arn=<EXECUTION_ARN> \
    --query="output" | jq -r  '. | fromjson'
```

Replace the `<EXECUTION_ARN>` with the `executionArn` output from the previous step. The result will contain the output of the State Machine execution:

```json
{
  "SSN": "123-45-6789",
  "Amount": 500000,
  "Term": 30,
  "Credit": {
    "Score": 861,
    "History": 15
  },
  "Banks": {
    "BankAddress": [
      "BankRecipientPremium",
      "BankRecipientUniversal",
      "BankRecipientPawnshop"
    ]
  },
  "Quotes": [
    {
      "Quote": {
        "rate": 3.881919225968371,
        "bankId": "Premium"
      }
    },
    {
      "Quote": {
        "rate": 5.032719931679686,
        "bankId": "Universal"
      }
    },
    {
      "Quote": {
        "rate": 6.019381689166033,
        "bankId": "PawnShop"
      }
    }
  ]
}
```

## GitHub Action

This application sample hosts an example GitHub Action workflow that starts up LocalStack, builds the Lambda functions, and deploys the infrastructure on the runner. You can find the workflow in the `.github/workflows/main.yml` file. To run the workflow, you can fork this repository and push a commit to the `main` branch.

Users can adapt this example workflow to run in their own CI environment. LocalStack supports various CI environments, including GitHub Actions, CircleCI, Jenkins, Travis CI, and more. You can find more information about the CI integration in the [LocalStack documentation](https://docs.localstack.cloud/user-guide/ci/).

## Cloud Pods

[Cloud Pods](https://docs.localstack.cloud/user-guide/tools/cloud-pods/) are a mechanism that allows you to take a snapshot of the state in your current LocalStack instance, persist it to a storage backend, and easily share it with your team members.

You can convert your current AWS infrastructure state to a Cloud Pod using the `localstack` CLI. Check out our [Getting Started guide](https://docs.localstack.cloud/user-guide/tools/cloud-pods/getting-started/) and [LocalStack Cloud Pods CLI reference](https://docs.localstack.cloud/user-guide/tools/cloud-pods/pods-cli/) to learn more about Cloud Pods and how to use them.

To inject a Cloud Pod that contains the infrastructure for this application, you can run the following command:

```sh
localstack pod load file://$(pwd)/cloud-pod/loan-broker-application
```

Alternatively, you can use [Cloud Pods Launchpad](https://docs.localstack.cloud/user-guide/tools/cloud-pods/launchpad/) to quickly inject Cloud Pods into your running LocalStack container. Click on the [badge] to launch Cloud Pods Launchpad and inject the Cloud Pod for this application by clicking the `Inject` button.

You can use the [LocalStack Web Application](https://app.localstack.cloud) to view the [Step Functions Resource Browser](https://app.localstack.cloud/resources/stepfunctions) and see the State Machine that the Cloud Pod injected. Similarly, you can navigate to the [DynamoDB](https://app.localstack.cloud/resources/dynamodb) to see the `LoanBrokerBanksTable` table, alongside [Lambda functions](https://app.localstack.cloud/resources/lambda), [SNS topic](https://app.localstack.cloud/resources/sns), [SQS queue](https://app.localstack.cloud/resources/sqs), and more that the Cloud Pod injected.

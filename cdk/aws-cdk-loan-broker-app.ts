#!/usr/bin/env node
import "source-map-support/register";
import * as cdk from "aws-cdk-lib";
import { LoanBrokerRecipientListStack } from "./LoanBroker-RecipientList-stack";
import { LoanBrokerPubSubStack } from "./LoanBroker-PubSub-stack";

const app = new cdk.App();

const loanBrokerRecipientListStack = new LoanBrokerRecipientListStack(app, "LoanBroker-RecipientList-Stack", {
    env: { account: process.env.CDK_DEFAULT_ACCOUNT, region: process.env.CDK_DEFAULT_REGION },
});
cdk.Tags.of(loanBrokerRecipientListStack).add("Project", "AWS CDK Loan Broker");
cdk.Tags.of(loanBrokerRecipientListStack).add("Stackname", "LoanBroker-RecipientList-Stack");
cdk.Tags.of(loanBrokerRecipientListStack).add("aws-apn-id", "pc:9yq38ki5jw5mas7jhjthpgveo");


const loanBrokerPubSubStack = new LoanBrokerPubSubStack(app, "LoanBroker-PubSub-Stack", {
    env: { account: process.env.CDK_DEFAULT_ACCOUNT, region: process.env.CDK_DEFAULT_REGION },
});
cdk.Tags.of(loanBrokerPubSubStack).add("Project", "AWS CDK Loan Broker");
cdk.Tags.of(loanBrokerPubSubStack).add("Stackname", "LoanBroker-PubSub-Stack");
cdk.Tags.of(loanBrokerPubSubStack).add("aws-apn-id", "pc:9yq38ki5jw5mas7jhjthpgveo");

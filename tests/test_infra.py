import time
import json
import pytest
import boto3

@pytest.fixture
def stepfunctions_client():
    return boto3.client(
        "stepfunctions", region_name="us-east-1", endpoint_url="http://localhost:4566"
    )

@pytest.fixture
def dynamodb_client():
    return boto3.client(
        "dynamodb", region_name="us-east-1", endpoint_url="http://localhost:4566"
    )

def test_loan_broker_workflow(stepfunctions_client, dynamodb_client):
    response = stepfunctions_client.list_state_machines()
    state_machines = response["stateMachines"]

    state_machine_arn = None
    for state_machine in state_machines:
        if state_machine["name"].startswith(
            "LoanBroker-RecipientList-Stack-LoanBroker"
        ):
            state_machine_arn = state_machine["stateMachineArn"]
            break

    assert (
        state_machine_arn is not None
    ), "State machine with specified prefix not found"

    dynamodb_client.put_item(
        TableName="LoanBrokerBanksTable",
        Item={
            "Type": {"S": "Home"},
            "BankAddress": {
                "L": [
                    {"S": "BankRecipientPremium"},
                    {"S": "BankRecipientUniversal"},
                    {"S": "BankRecipientPawnshop"},
                ]
            },
        },
    )

    start_response = stepfunctions_client.start_execution(
        stateMachineArn=state_machine_arn,
        name="cli-test-run",
        input='{"SSN": "123-45-6789", "Amount": 500000, "Term": 30}',
    )
    execution_arn = start_response["executionArn"]

    time.sleep(10)

    describe_response = stepfunctions_client.describe_execution(
        executionArn=execution_arn
    )
    output_json = json.loads(describe_response["output"])

    assert "SSN" in output_json
    assert "Amount" in output_json
    assert "Term" in output_json
    assert "Credit" in output_json
    assert "Banks" in output_json
    assert "Quotes" in output_json

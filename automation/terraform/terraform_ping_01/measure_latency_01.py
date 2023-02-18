# Reference: https://github.com/awsdocs/aws-doc-sdk-examples/blob/main/python/example_code/lambda/lambda_basics.py

import io
import json
import logging
import zipfile
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

class LambdaWrapper:
    def __init__(self, lambda_client, iam_resource):
        self.lambda_client = lambda_client
        self.iam_resource = iam_resource

    def invoke_function(self, function_name, function_params, get_log=False):
        """
        Invokes a Lambda function.

        :param function_name: The name of the function to invoke.
        :param function_params: The parameters of the function as a dict. This dict
                                is serialized to JSON before it is sent to Lambda.
        :param get_log: When true, the last 4 KB of the execution log are included in
                        the response.
        :return: The response from the function invocation.
        """
        try:
            response = self.lambda_client.invoke(
                FunctionName=function_name,
                Payload=json.dumps(function_params),
                LogType='Tail' if get_log else 'None')
            logger.info("Invoked function %s.", function_name)
        except ClientError:
            logger.exception("Couldn't invoke function %s.", function_name)
            raise
        return response


regions = ['us-east-1', 'sa-east-1', 'eu-central-1', 'ap-northeast-1', 'ap-southeast-2']
whoamis = ['virginia', 'saopaulo', 'frankfurt', 'tokyo', 'sydney']

region_count = len(regions)

funcs   = []
clients = []
wrappers = []
records = []

for i in range(region_count):
    funcs.append( 'my-lambda-http-head-' + regions[i] )
    clients.append( boto3.client('lambda', region_name=regions[i]) )
    wrappers.append( LambdaWrapper(clients[i], None))

websites = ['https://www.washingtontimes.com', 'http://www.leroymerlin.com.br',
            'https://www.zalando-outlet.de' , 'https://www.docomo.ne.jp',
            'http://www.sydneymarkets.com.au']

for i in range(region_count):
    func_name = funcs[i]
    whoami =whoamis[i]

    for j in range(len(websites)):
        func_params = {'host': websites[j], 'whoami':whoami }
        response = wrappers[i].invoke_function(func_name, func_params)
        payload = response['Payload']
        result = json.loads(payload.read().decode())

        records.append(result)

        print( result )
        print()

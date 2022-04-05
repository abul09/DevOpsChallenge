#!/usr/bin/env python
import boto3
import botocore

import json
import sys

cf = boto3.client('cloudformation')

def main(stack_name, template, parameters):
    template_data = _parse_template(template)
    parameters_data = _parse_parameters(parameters)

    params = {
        'StackName': stack_name,
        'TemplateBody': template_data,
        'Parameters': parameters_data
    }

    try:
        if _stack_exists(stack_name):
            print('Updating {}'.format(stack_name))
            stack_result = cf.update_stack(**params)
            waiter = cf.get_waiter('stack_update_complete')
        else:
            print('Creating {}'.format(stack_name))
            stack_result = cf.create_stack(**params)
            waiter = cf.get_waiter('stack_create_complete')

        waiter.wait(StackName=stack_name)
    except botocore.exceptions.ClientError as ex:
        error_message = ex.response['Error']['Message']
        
        if error_message == 'No updates are to be performed.':
            print("No changes")
        else:
            raise
    else:
        print(cf.describe_stacks(StackName=stack_result['StackId']))
        # print(json.dumps(
        #     cf.describe_stacks(StackName=stack_result['StackId']),
        #     indent=2,
        #     default=json_serial
        # ))

def _parse_template(template):
    with open(template) as template_fileobj:
        template_data = template_fileobj.read()

    cf.validate_template(TemplateBody=template_data)

    return template_data

def _parse_parameters(parameters):
    with open(parameters) as parameters_fileobj:
        parameters_data = json.load(parameters_fileobj)

    return parameters_data

def _stack_exists(stack_name):
    stacks = cf.list_stacks()['StackSummaries']
    
    for stack in stacks:
        if stack['StackStatus'] == 'DELETE_COMPLETE':
            continue
        
        if stack_name == stack['StackName']:
            return True
    
    return False

# def _can_deploy_stack(stack_name):
#     stacks = cf.list_stacks()['StackSummaries']

#     if _stack_exists(stacks):
#         for stack in stacks:
#             if stack_name == stack['StackName']:
#                 if stack['StackStatus'] == 'ROLLBACK_COMPLETE':
#                     print("Stack need to be deleted")
#                     return False
#                 else:
#                     return True

#     return True

if __name__ == '__main__':
    main(*sys.argv[1:])
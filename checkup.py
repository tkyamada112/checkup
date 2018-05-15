import boto3
import argparse
import os, sys, json
from credentials import *

def get_options():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-env', '--environment',
        dest = 'aws_environment',
        nargs = '?',
        default = 'dev',
        required = False,
        type = str,
        help = 'Output instance statuses(ec2, rds).\
            Specify envrironment \"dev\" or \"prd\".\
            (default: dev)'
    )
    return parser.parse_args()

class EC2:
    def Client(accesskey, secretkey, region):
        ec2client = boto3.client('ec2',
            aws_access_key_id=accesskey,
            aws_secret_access_key=secretkey,
            region_name=region
            )
        return ec2client

    def List(client):
        stat_arr = []
        for instance_status in client.describe_instance_status()['InstanceStatuses']:
            status = instance_status.get('SystemStatus')
            if status['Status'] != 'ok':
                stat_arr.append(status['Status'])
        return stat_arr

class RDS:
    def Client(access, secretkey, region):
        rdsclient = boto3.client('rds',
            aws_access_key_id=accesskey,
            aws_secret_access_key=secretkey,
            region_name=region
            )
        return rdsclient

    def List(client):
        stat_arr = []
        for db_status in client.describe_db_instances()['DBInstances']:
            if db_status['DBInstanceStatus'] != 'available':
                stat_arr.append(db_status['DBInstanceStatus'])
        return stat_arr

opt = get_options()

if opt.aws_environment == "dev":
    accesskey = DEV_AWS_ACCESS_KEY_ID
    secretkey = DEV_AWS_SECRET_ACCESS_KEY
    region    = DEV_REGION
elif opt.aws_environment == "prd":
    accesskey = PRD_AWS_ACCESS_KEY_ID
    secretkey = PRD_AWS_SECRET_ACCESS_KEY
    region    = PRD_REGION
else:
    print("invalid argument")
    exit(1)

#accesskey = os.environ.get("AWS_ACCESS_KEY_ID")
#secretkey = os.environ.get("AWS_SECRET_ACCESS_KEY")
#region    = os.environ.get("AWS_DEFAULT_REGION")

ec2client    = EC2.Client(accesskey, secretkey, region)
compute_list = EC2.List(ec2client)
rdsclient    = RDS.Client(accesskey, secretkey, region)
db_list      = RDS.List(rdsclient)

if len(compute_list) == 0 and len(db_list) == 0:
    print("Healty!")
elif len(compute_list) == 0 and len(db_list) != 0:
    print('%d db instance is impaired.' % len(db_list))
elif len(compute_list) != 0 and len(db_list) == 0:
    print('%d compute instance is impaired.' % len(compute_list))

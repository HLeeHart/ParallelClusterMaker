################################################################################
# Name:		jumphostmaker_aux_data.py
# Author:	Rodney Marable <rodney.marable@gmail.com>
# Created On:	April 16, 2019
# Last Changed:	May 31, 2019
# Purpose:	Data structures and functions for make-pcluster-jumphost.py
################################################################################

# Function: add_security_group_rule()
# Purpose: add a rule to a security group

def add_security_group_rule(region, sec_grp, protocol, cidr, psource, pdest):
    import boto3
    ec2 = boto3.resource('ec2', region_name=region)
    sec_grp.authorize_ingress(
        IpProtocol=protocol,
        CidrIp=cidr,
        FromPort=psource,
        ToPort=pdest
    )

# Function: get_ami_info()
# Purpose: get the ID of an AWS AMI image
# Notes: http://cavaliercoder.com/blog/finding-the-latest-centos-ami.html

def get_ami_info(base_os, region):
    import boto3
    import json
    ec2client = boto3.client('ec2', region_name = region)
    ami_information = ec2client.describe_images(
        Owners=['137112412989'],
        Filters=[
          {'Name': 'name', 'Values': ['amzn2-ami-hvm-2.0.20190508-x86_64-gp2']},
          {'Name': 'architecture', 'Values': ['x86_64']},
          {'Name': 'root-device-type', 'Values': ['ebs']},
        ],
    )
    amis = sorted(ami_information['Images'],
        key=lambda x: x['CreationDate'],
        reverse=True)
    aws_ami = amis[0]['ImageId']
    return(aws_ami)

# Function: illegal_az_msg()
# Purpose: Return an error message when an invalid AZ is provided

def illegal_az_msg(az):
    import sys
    print('*** ERROR ***')
    print('"' + az + '"' + ' is not a valid Availability Zone in the selected AWS Region.')
    print('Aborting...')
    sys.exit(1)

# Function: p_val()
# Purpose: print a successful instance_parameter validation message to stdout

def p_val(p, debug_mode):
    if debug_mode == 'True' or debug_mode == 'true':
        print(p + " successfully validated")
    else:
        pass

# Function: p_fail()
# Purpose: print a failed instance_parameter validation message to stdout

def p_fail(p, q, r):
    import sys
    import textwrap
    print('')
    print("*** Error ***")
    if r == 'missing_element':
        print('"' + p + '"' + ' seems to be missing as a valid ' + q + '.')
    else:
        print('"' + p + '"' + ' is not a valid option for ' + q + '.')
        print("Supported values:")
        r = '\t'.join(r)
        print('\n'.join(textwrap.wrap(r, 78)))
    print('')
    print("Aborting...")
    sys.exit(1)

# Function print_TextHeader()
# Purpose: print a centered text header to support validation and reviewing
# of instance_parameters.

def print_TextHeader(p, action, line_length):
    print('')
    print(''.center(line_length, '-'))
    T2C = action + ' parameter values for ' + p
    print(T2C.center(line_length))
    print(''.center(line_length, '-'))

# Function: ctrlC_Abort()
# Purpose: Print an abort header, capture CTRL-C when pressed, and remove any
# orphaned state and config files created by the jumphost creation script.

def ctrlC_Abort(sleep_time, line_length, vars_file_path, instance_serial_number_file, instance_serial_number):
    import boto3
    import os
    import sys
    import time
    iam = boto3.client('iam')
    jumphost_iam_instance_policy = 'jumphostmaker-policy-' + str(instance_serial_number)
    jumphost_iam_instance_profile = 'jumphostmaker-profile-' + str(instance_serial_number)
    jumphost_iam_instance_role = 'jumphostmaker-role-' + str(instance_serial_number)
    print('')
    print(''.center(line_length, '#'))
    print('    Please type CTRL-C within 5 seconds to abort    '.center(line_length, '#'))
    print(''.center(line_length, '#'))
    print('')
    try:
        time.sleep(sleep_time)
    except KeyboardInterrupt:
        if (vars_file_path == 1) and (cluster_serial_number_file == 1):
            print('')
            print('No orphaned files or directories were found.')
            print('')
        else:
            os.remove(instance_serial_number_file)
            os.remove(vars_file_path)
            print('')
            print('Removed: ' + instance_serial_number_file)
            print('Removed: ' + vars_file_path)
            print('')
        if (instance_serial_number == 1):
            print('')
            print('No IAM role or policy exists for this jumphost.')
            print('')
        else:
            iam.remove_role_from_instance_profile(InstanceProfileName=jumphost_iam_instance_profile, RoleName=jumphost_iam_instance_role)
            iam.delete_instance_profile(InstanceProfileName=jumphost_iam_instance_profile)
            iam.delete_role_policy(RoleName=jumphost_iam_instance_role, PolicyName=jumphost_iam_instance_policy)
            iam.delete_role(RoleName=jumphost_iam_instance_role)
            print('')
            print('Deleted: ' + jumphost_iam_instance_profile)
            print('Deleted: ' + jumphost_iam_instance_policy)
            print('Deleted: ' + jumphost_iam_instance_role)
            print('')
        print('Aborting...')
        sys.exit(1)

# Function: refer_to_docs_and_quit()
# Purpose: Print an error message, refer to the AWS ParallelCluster public
# documentation, and quit with a non-successful error code.

def refer_to_docs_and_quit(error_msg):
    import sys
    print('')
    print('*** ERROR ***')
    print(error_msg)
    print('')
    print('Please refer to the ParallelCluster documentation for more information:')
    print('https://aws-parallelcluster.readthedocs.io/en/latest/index.html')
    print('')
    print('Aborting...')
    sys.exit(1)

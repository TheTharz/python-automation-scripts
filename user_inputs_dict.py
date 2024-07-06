import boto3
import sys

# Function to assume the role and get temporary credentials
def assume_role(role_arn, session_name):
    try:
        sts_client = boto3.client('sts')
        response = sts_client.assume_role(
            RoleArn=role_arn,
            RoleSessionName=session_name
        )
        return response['Credentials']
    except Exception as e:
        print(f"Error assuming role: {e}")
        sys.exit(1)

# Function to create a Route 53 record
def create_route53_record(credentials, hosted_zone_id, domain_name, record_type, ttl, ip_address):
    try:
        route53_client = boto3.client(
            'route53',
            aws_access_key_id=credentials['AccessKeyId'],
            aws_secret_access_key=credentials['SecretAccessKey'],
            aws_session_token=credentials['SessionToken']
        )

        response = route53_client.change_resource_record_sets(
            HostedZoneId=hosted_zone_id,
            ChangeBatch={
                'Changes': [
                    {
                        'Action': 'CREATE',
                        'ResourceRecordSet': {
                            'Name': domain_name,
                            'Type': record_type,
                            'TTL': ttl,
                            'ResourceRecords': [{'Value': ip_address}]
                        }
                    }
                ]
            }
        )
        print("DNS record created successfully:", response)
    except Exception as e:
        print(f"Error creating DNS record: {e}")
        sys.exit(1)

# Main function to get user inputs and create the DNS record
def main():
    print("AWS Route 53 DNS Record Automation")

    role_arn = input("Enter the IAM role ARN: ")
    session_name = input("Enter a session name for assuming the role: ")
    hosted_zone_id = input("Enter the Hosted Zone ID: ")
    domain_name = input("Enter the domain name (e.g., example.com): ")
    record_type = input("Enter the record type (e.g., A, CNAME): ")
    ttl = int(input("Enter the TTL (Time To Live) in seconds: "))
    ip_address = input("Enter the IP address: ")

    credentials = assume_role(role_arn, session_name)
    create_route53_record(credentials, hosted_zone_id, domain_name, record_type, ttl, ip_address)

if __name__ == "__main__":
    main()

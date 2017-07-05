from boto3 import boto3
from helpers import getCurrentConfigFile, writeToConfigFile


def uploadToS3(applicationName):
    configFile = getCurrentConfigFile()

    s3Client = boto3.client(
        's3',
        aws_access_key_id=configFile["s3"]["accessKey"],
        aws_secret_access_key=configFile["s3"]["secretKey"],
        region_name='eu-central-1'
    )

    print "Uploading application"
    s3Client.upload_file('applications/'+applicationName, 'k303', applicationName)
    print "Upload completed"

    return "pathToApplication"


def checkS3Access():
    s3Setup = raw_input("\nDid you already configure your AWS credentials? If not, then we can set it here. (it needs to be in our config file) [y,n]")

    if s3Setup == "y":
        s3AccessKey = raw_input("Your Access Key?\n")
        s3SecretKey = raw_input("Your Secret Key?\n")

        s3 = {
            "access": s3AccessKey,
            "secret": s3SecretKey
        }

        writeToConfigFile("update", "s3", s3)

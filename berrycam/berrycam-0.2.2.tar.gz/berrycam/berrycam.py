#!/usr/bin/env python3

import os, sys, argparse, logging, boto3
from io import BytesIO
from time import sleep
from picamera import PiCamera
from ftplib import FTP

def acquire_image(log, args):
	output_stream = BytesIO()
	camera = PiCamera()
	try:
		camera.resolution = (args.res_width, args.res_height)
		camera.start_preview()
		# Camera warm-up time
		sleep(2)
		camera.capture(output_stream, 'jpeg')
		camera.stop_preview()
		output_stream.seek(0)
		return output_stream.getvalue()
	except:
		log.fatal("Unable to obtain image from camera, two processes may be trying at the same time")
		exit()
	finally:
		camera.close()

def upload_s3(data, args):
	try:
		s3 = boto3.client(
			's3',
			endpoint_url='https://{}'.format(args.s3_endpoint),
			aws_access_key_id = args.access_key,
			aws_secret_access_key = args.secret_key
		)
		bytes_stream = BytesIO(data)
		s3.upload_fileobj(bytes_stream, args.bucket_name, args.bucket_path)
		s3.put_object_acl(ACL='public-read', Bucket=args.bucket_name, Key=args.bucket_path)
		return True
	except:
		return False

def upload_ftp(data, args):
	try:
		bytes_stream = BytesIO(data)
		ftp = FTP(args.ftp_server)
		ftp.login(args.ftp_username, args.ftp_password)
		ftp.storbinary('STOR image.jpeg', bytes_stream)
		return True
	except:
		return False

def process(log, args):
	log.info("Acquiring image...")
	image = acquire_image(log, args)

	if args.output:
		log.info("Writing image to {}".format(args.output))
		with open(args.output, 'wb') as f:
			image = image
			f.write(image)
			f.close()
	
	if args.s3:
		log.info("Writing image to {}.{}/{}".format(args.s3_endpoint, args.bucket_name, args.bucket_path))
		upload_s3(image, args)
	
	# Now we have the data acquired, we can upload it
	if args.ftp:
		log.info("Writing image to FTP {} ({})".format(args.server, args.username))
		upload_ftp(image, args)

def main():

	parser = argparse.ArgumentParser()

	# Save to file
	parser.add_argument("-o", "--output", required=True, help="file name / path")

	# Save to FTP
	parser.add_argument("--ftp", help="write captured image to ftp", action="store_true")
	parser.add_argument("--ftp-server", "-s", default="webcam.wunderground.com", help="ftp server hostname")
	parser.add_argument("--ftp-username", "-u", default=os.getenv('FTP_USERNAME', ''), help="ftp username")
	parser.add_argument("--ftp-password", "-p", default=os.getenv('FTP_PASSWORD', ''), help="ftp password")
	
	# Save to S3
	parser.add_argument("--s3", help="write captured image to s3", action="store_true")
	parser.add_argument("--s3-endpoint", default=os.getenv('S3_ENDPOINT', 'objects-us-west-1.dream.io'), help="s3 endpoint")
	parser.add_argument("--access-key", default=os.getenv('S3_ACCESS_KEY', ''), help="s3 access key")
	parser.add_argument("--secret-key", default=os.getenv('S3_SECRET_KEY', ''), help="s3 secret key")
	parser.add_argument("--bucket-name", help="s3 bucket name")
	parser.add_argument("--bucket-path", help="s3 bucket path")
	
	# General configuration
	parser.add_argument("--res-width", default=1024, help="image width")
	parser.add_argument("--res-height", default=768, help="image height")

	# Verbose mode
	parser.add_argument("--verbose", "-v", help="increase output verbosity", action="store_true")
	args = parser.parse_args()

	if args.verbose:
		logging.basicConfig(level=logging.DEBUG)
	else:
		logging.basicConfig(level=logging.INFO)
	log = logging.getLogger(__name__)

	process(log, args)

if __name__ == '__main__':
	main()
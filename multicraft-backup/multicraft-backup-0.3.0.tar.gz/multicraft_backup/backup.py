#!/usr/bin/env python3
# encoding: utf-8

import subprocess
import hashlib
import tarfile

import os
import datetime


class BackerUpper:
	def __init__(self, config, target_dir):
		self._config = config
		self._desired_dir = config['ftp']['desired_dir']
		
		self.target_dir = target_dir
	
	
	def do_it_all_everything(self):
		self.backup()
		self.checksum()
		self.tar_it_up()
	
	
	def backup(self):
		"""back up the desired directory from the server.
		make sure you stop the server first!
		"""
		
		# mkdir -p
		os.makedirs(
			os.path.join(self.target_dir, self._desired_dir),
			exist_ok=True,
		)
		
		os.chdir(self.target_dir)
		
		# TODO explain these parameters
		subprocess.run((
			'wget',
			'-P',
			'.',
			'--no-host-directories',
			'-r',
			'-N',
			'-l', 'inf',
			'--user', '{email}.{id}'.format(
				email=self._config['login']['username'],
				id=self._config['server']['id_number']
			),
			'--password', self._config['login']['password'],
			'ftp://{}/{}'.format(
				self._config['ftp']['server_ip'],
				self._desired_dir,
			),
		))
	
	
	def _mkdir_safe(self, dirname):
		try:
			os.mkdir(dirname)
		except FileExistsError:
			pass
	
	
	def checksum(self):
		"""checksum the files, and write to SHA256SUMS"""
		
		with open('SHA256SUMS', 'w') as sums:
			
			for dirname, _, filenames in os.walk(self._desired_dir):
				for filename in filenames:
					filename = os.path.join(dirname, filename)
					print('Checksumming', filename)
					sums.write(self._get_checksum_line(filename) + '\n')
	
	
	def _get_checksum_line(self, filename, hash_algorithm='sha256'):
		with open(filename, 'rb') as f:
			hasher = hashlib.new(hash_algorithm, f.read())
			return '{} {}'.format(
				hasher.hexdigest(),
				filename,
			)
	
	
	def tar_it_up(self):
		print('Tarring it up!')
		
		output_filename = datetime.datetime.now().isoformat() + '.tar.xz'
		
		with tarfile.open(output_filename) as tape_archive:
			tape_archive.add(
				self._desired_dir,
				arcname=os.path.basename(self._desired_dir)
			)
			tape_archive.add('SHA256SUMS')
		
		print('Tarred and feathered 🤠')

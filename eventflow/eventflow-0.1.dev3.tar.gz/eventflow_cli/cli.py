import click
import os
import re
import pydbus
import gi.repository
import uuid as uuidlib
import json as jsonlib

class Operation:
	uuid_pattern = r"[0-9A-Za-z_]+"
	type_pattern = r"[0-9A-Za-z-]+"
	
	def __init__(self):
		self.bus = pydbus.SystemBus()
		self.systemd = self.bus.get("org.freedesktop.systemd1")
		self.dbus = self.bus.get("org.freedesktop.DBus")
		self.systemd_path = "/etc/systemd/system"
		self.debug = False
	
	def echo(self, *args, sep=" ", end="\n", err=False, json=False):
		encoding_function = str
		if json:
			encoding_function = jsonlib.dumps
		click.echo(sep.join([ encoding_function(arg) for arg in args ]) + end, err=err, nl=False)
	
	def log(self, *args, sep=" ", end="\n"):
		if self.debug:
			self.echo(*args, sep, end, err=True)
	
	def get_streerror(self, e):
		"""Extracts error/exception message."""
		if hasattr(e, "strerror"):
			msg = e.strerror
		else:
			msg = str(e)
		if isinstance(msg, bytes):
			msg = msg.decode("utf-8", "replace")
		return msg
	
	def parse_node_file_extract_name(self, node_file):
		"""Extracts name from node-file (from 'Description'-option)."""
		# TODO: validate BindsTo, After (occurrences in both options, alias names (regex))
		try:
			with click.open_file(node_file) as f:
				return [
					re.match(r"Description(\s)*=(\s)*eventflow node (" + self.type_pattern + ")", s).group(3)
					for s in f.readlines()
					if re.match(r"Description(\s)*=(\s)*eventflow node (" + self.type_pattern + ")", s)
				][0]
		except (IOError, OSError) as e:
			# failed to open node-file
			raise click.FileError(node_file, hint=self.get_streerror(e))
		except IndexError:
			# no "Description"-option in node-file
			raise click.ClickException("Missing or malformed 'Description'-option: %s" % node_file)
	
	def copy_and_replace(self, source, target, replacements=[]):
		"""Copies 'source'-filename to 'target'-filename. While copying, replacing
		given replacements (array of 2-tuples)."""
		try:
			with click.open_file(source, mode="r") as f_i: # TODO: python3 text-mode?
				with click.open_file(target, mode="w") as f_o: # TODO: python3 text-mode?
					for line in f_i:
						for old, new in replacements:
							line = line.replace(old, new)
						f_o.write(line)
		except (IOError, OSError) as e:
			# copy failed
			raise click.ClickException("Could not copy file: %s -> %s: %s" % (source, target, self.get_streerror(e)))
	
	def remove(self, node_file_systemd):
		"""Removes 'node_file_systemd'-filename."""
		try:
			os.remove(node_file_systemd)
		except OSError as e:
			# remove failed
			raise click.ClickException("Could not remove file: %s: %s" % (node_file_systemd, self.get_streerror(e)))
	
	def reload_daemon(self):
		"""Reloads systemd daemon."""
		try:
			self.systemd.Reload()
		except gi.repository.GLib.Error as e:
			raise click.ClickException("Could not reload systemd daemon: %s" % e.message)
	
	def enable_node(self, type, node_unit):
		"""Enables the given unit file."""
		try:
			return self.systemd.EnableUnitFiles([ node_unit ], False, True)
		except gi.repository.GLib.Error as e:
			raise click.ClickException("Could not start node: %s: %s" % (type, e.message))
	
	def disable_node(self, type, node_unit):
		"""Disables the given unit file."""
		try:
			return self.systemd.DisableUnitFiles([ node_unit ], False)
		except gi.repository.GLib.Error as e:
			raise click.ClickException("Could not stop node: %s: %s" % (type, e.message))
	
	def start_node(self, type, node_unit):
		"""Starts the given unit file."""
		try:
			self.systemd.StartUnit(node_unit, "replace")
		except gi.repository.GLib.Error as e:
			raise click.ClickException("Could not start node: %s: %s" % (type, e.message))
	
	def stop_node(self, type, node_unit):
		"""Stops the given unit file."""
		try:
			self.systemd.StopUnit(node_unit, "replace")
		except gi.repository.GLib.Error as e:
			raise click.ClickException("Could not stop node: %s: %s" % (type, e.message))
	
	def list_imported(self):
		"""Returns a list of all imported node types."""
		pattern = r"ef-(" + self.type_pattern + ")@\.service"
		return [
			re.match(pattern, os.path.basename(file)).group(1)
			for file, _ in self.systemd.ListUnitFiles()
			if re.match(pattern, os.path.basename(file))
		]
	
	def list_started(self):
		"""Returns a dictionary where the keys are all started node uuids and the
		values are the types of the uuids."""
		unit_pattern = r"ef-(" + self.type_pattern + ")@(" + self.uuid_pattern + ")\.service"
		return {
			re.match(unit_pattern, unit[0]).group(2): re.match(unit_pattern, unit[0]).group(1)
			for unit in self.systemd.ListUnits()
			if unit[3] == "active" and re.match(unit_pattern, unit[0])
		}

@click.group(invoke_without_command=True)
@click.option("--systemd-path", "-s", show_default=True,
	help="SystemD-path where node files are stored.",
	default="/etc/systemd/system", type=click.Path(exists=True))
@click.option("--debug", "-d", is_flag=True, default=False,
	help="Enable debug logging on stderr.")
@click.pass_context
def cli(ctx, systemd_path, debug):
	ctx.obj = Operation()
	ctx.obj.systemd_path = os.path.abspath(systemd_path)
	ctx.obj.debug = debug
	if ctx.invoked_subcommand is None:
		ctx.obj.echo("Hello World!")

@cli.command(name="import") # explicit because "import" is a reserved statement
@click.argument("node_dir", type=click.Path(exists=True))
@click.pass_context
def _import(ctx, node_dir):
	"""Import node from path. This copies the 'node@.service'-file (which is
	located in NODE_DIR) into a global directory of systemd. Make sure that the
	path keeps existing after an import because the node-files in the
	systemd-directory point to that path.
	
	If you want to change the path unimport the node, then move the directory
	and re-import the node.
	
	Each %d specifier in a 'node@.service'-file will be replaced by the path the
	node is imported from.
	
	This command should be used to re-import a node if the 'node@.service'-file
	has changed und must be refreshed in the global systemd directory."""
	# TODO: this command needs privileges for the systemd directory
	
	# normalize paths
	node_dir = os.path.abspath(node_dir)
	node_file = os.path.join(node_dir, "node@.service")
	
	# parse name out of node-file
	ctx.obj.log("Parsing", node_file, "...")
	node_name = ctx.obj.parse_node_file_extract_name(node_file)
	
	# copy node-file to systemd-directory with node-name (prefix with 'ef-')
	node_file_systemd = os.path.join(ctx.obj.systemd_path, "ef-" + node_name + "@.service")
	ctx.obj.log("Copying", node_file, "->", node_file_systemd, "(inplace replacing %%d) ...")
	ctx.obj.copy_and_replace(node_file, node_file_systemd, [ ("%d", node_dir) ])
	
	# reload systemd daemon
	ctx.obj.log("Reloading systemd daemon ...")
	ctx.obj.reload_daemon()

@cli.command()
@click.argument("type")
@click.pass_context
def unimport(ctx, type):
	"""Un-import node by type. This removes the 'node@.service'-file from the
	global directory of systemd."""
	# TODO: expand that this command accepts a node-directory, then parses the
	# node-file and uses this as 'type'
	# TODO: stop all nodes of this type first
	# TODO: this command needs privileges for the systemd directory
	
	# normalize paths
	node_file_systemd = os.path.join(ctx.obj.systemd_path, "ef-" + type + "@.service")
	
	# remove node-file in systemd-directory
	ctx.obj.log("Removing", node_file_systemd, "...")
	ctx.obj.remove(node_file_systemd)

@cli.command(name="list-imported")
@click.pass_context
def list_imported(ctx):
	"""List imported nodes."""
	
	nodes = ctx.obj.list_imported()
	ctx.obj.echo(nodes, json=True)

@cli.command(name="list-started")
@click.pass_context
def list_started(ctx):
	"""List started nodes."""
	
	nodes = ctx.obj.list_started()
	ctx.obj.echo(nodes, json=True)

@cli.command()
@click.argument("type")
@click.pass_context
def start(ctx, type):
	"""Start node by type."""
	# TODO: improve docstring
	# TODO: this command needs privileges for the systemd directory
	
	uuid = str(uuidlib.uuid4()).replace("-", "")
	node_unit = "ef-" + type + "@" + uuid + ".service"
	ctx.obj.log("Starting", node_unit, "...")
	success, changes = ctx.obj.enable_node(type, node_unit)
	if not success:
		raise click.ClickException("Could not start node: %s: The node-file contains no enablement information (i.e. an [Install]) section" % type)
	for change_type, change_from, change_to in changes:
		ctx.obj.log("systemd:", change_type, change_from, "->", change_to)
	ctx.obj.start_node(type, node_unit)
	ctx.obj.echo(uuid, json=True)

@cli.command()
@click.argument("uuid")
@click.pass_context
def stop(ctx, uuid):
	"""Stop node by uuid."""
	# TODO: improve docstring
	# TODO: this command needs privileges for the systemd directory
	
	uuids = ctx.obj.list_started()
	try:
		type = uuids[uuid]
	except KeyError:
		raise click.ClickException("Could not determine type from given uuid: %s: The given uuid is not started." % uuid)
	node_unit = "ef-" + type + "@" + uuid + ".service"
	ctx.obj.log("Stopping", node_unit, "...")
	ctx.obj.stop_node(type, node_unit)
	changes = ctx.obj.disable_node(type, node_unit)
	for change_type, change_from, change_to in changes:
		ctx.obj.log("systemd:", change_type, change_from, "->", change_to)

@cli.command()
@click.pass_context
def connect(ctx):
	"""Not implemented."""
	raise click.ClickException("Not implemented.")

@cli.command()
@click.pass_context
def disconnect(ctx):
	"""Not implemented."""
	raise click.ClickException("Not implemented.")

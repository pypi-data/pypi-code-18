import click
import os
import re
import pydbus
import gi.repository
import uuid as uuidlib
import json as jsonlib
import time

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
			self.echo(*args, sep=sep, end=end, err=True)
	
	def get_streerror(self, e):
		"""Extracts error/exception message."""
		if hasattr(e, "strerror"):
			msg = e.strerror
		else:
			msg = str(e)
		if isinstance(msg, bytes):
			msg = msg.decode("utf-8", "replace")
		return msg
	
	def run_systemd_command(self, *args, command, error_description="Unknown error"):
		"""Runs a systemd command using the DBus API."""
		try:
			return getattr(self.systemd, command)(*args)
		except gi.repository.GLib.Error as e:
			raise click.ClickException(error_description + ": %s" % e.message)
	
	def parse_node_file(self, node_file):
		"""Reads node file line by line and return array of lines."""
		try:
			with click.open_file(node_file) as f:
				return [ line.strip() for line in f.readlines() ]
		except (IOError, OSError) as e:
			# failed to open node-file
			raise click.FileError(node_file, hint=self.get_streerror(e))
	
	def write_unit_file_parent(self, type, lines, node_dir):
		"""Writes given lines to global systemd directory. This function will
		not append a StopWhenUnneeded=yes to the file."""
		path = os.path.join(self.systemd_path, "ef-" + type + "-parent@.service")
		self.log("Writing", path, "... (StopWhenUnneeded=no)")
		try:
			with click.open_file(path, mode="w") as f: # TODO: python3 text-mode?
				for line in lines:
					print(line.replace("%d", node_dir), file=f)
		except (IOError, OSError) as e:
			# create failed
			raise click.ClickException("Could not create file: %s: %s" % (path, self.get_streerror(e)))
	
	def write_unit_file_child(self, type, lines, node_dir):
		"""Writes given lines to global systemd directory. This function will
		append a StopWhenUnneeded=yes to the file."""
		path = os.path.join(self.systemd_path, "ef-" + type + "@.service")
		self.log("Writing", path, "... (StopWhenUnneeded=yes)")
		try:
			found_unit_section = False
			stopwhenunneeded_added = False
			with click.open_file(path, mode="w") as f: # TODO: python3 text-mode?
				for line in lines:
					if "[Unit]" in line:
						found_unit_section = True
					if found_unit_section and not stopwhenunneeded_added and len(line) == 0:
						print("StopWhenUnneeded=yes", file=f)
						stopwhenunneeded_added = True
					print(line.replace("%d", node_dir), file=f)
		except (IOError, OSError) as e:
			# create failed
			raise click.ClickException("Could not create file: %s: %s" % (path, self.get_streerror(e)))
	
	def write_unit_files(self, type, lines, node_dir):
		"""Writes given lines to global systemd directory. This function
		generates two files, one with StopWhenUnneeded=yes and the other with
		StopWhenUnneeded=no."""
		self.write_unit_file_parent(type, lines, node_dir)
		self.write_unit_file_child(type, lines, node_dir)
	
	def extract_name(self, lines):
		"""Extracts name from node-file-lines (from 'Description'-option)."""
		# TODO: validate BindsTo, After (occurrences in both options, alias names (regex))
		try:
			return [
				re.match(r"Description(\s)*=(\s)*eventflow node (" + self.type_pattern + ")", line).group(3)
				for line in lines
				if re.match(r"Description(\s)*=(\s)*eventflow node (" + self.type_pattern + ")", line)
			][0]
		except IndexError:
			# no "Description"-option in node-file
			raise click.ClickException("Missing or malformed 'Description'-option: %s" % node_file)
	
	def remove(self, node_file_systemd):
		"""Removes 'node_file_systemd'-filename."""
		try:
			os.remove(node_file_systemd)
		except OSError as e:
			# remove failed
			raise click.ClickException("Could not remove file: %s: %s" % (node_file_systemd, self.get_streerror(e)))
	
	def reload_daemon(self):
		"""Reloads systemd daemon."""
		self.run_systemd_command(command="Reload", error_description="Could not reload systemd daemon")
		time.sleep(0.25)
	
	def enable_node(self, type, node_unit):
		"""Enables the given unit file."""
		return self.run_systemd_command([ node_unit ], False, True, command="EnableUnitFiles", error_description="Could not start node")
	
	def disable_node(self, type, node_unit):
		"""Disables the given unit file."""
		return self.run_systemd_command([ node_unit ], False, command="DisableUnitFiles", error_description="Could not stop node")
	
	def start_node(self, type, node_unit):
		"""Starts the given unit file."""
		self.run_systemd_command(node_unit, "replace", command="StartUnit", error_description="Could not start node")
	
	def stop_node(self, type, node_unit):
		"""Stops the given unit file."""
		self.run_systemd_command(node_unit, "replace", command="StopUnit", error_description="Could not stop node")
	
	def list_imported(self):
		"""Returns a list of all imported node types."""
		pattern = r"ef-(" + self.type_pattern + ")-parent@\.service" # match only parents
		return [
			re.match(pattern, os.path.basename(file)).group(1)
			for file, _ in self.run_systemd_command(command="ListUnitFiles")
			if re.match(pattern, os.path.basename(file))
		]
	
	def list_started(self):
		"""Returns a dictionary where the keys are all started node uuids and the
		values are the types of the uuids."""
		unit_pattern = r"ef-(" + self.type_pattern + ")-parent@(" + self.uuid_pattern + ")\.service" # match only parents
		return {
			re.match(unit_pattern, unit[0]).group(2): re.match(unit_pattern, unit[0]).group(1)
			for unit in self.run_systemd_command(command="ListUnits")
			if unit[3] == "active" and re.match(unit_pattern, unit[0])
		}
	
	def get_type_by_uuid(self, uuid):
		"""Returns the type of a given uuid."""
		return [ type for uuid_, type in self.list_started().items() if uuid_ == uuid ][0]

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
	
	# parse lines out of node-file and write unit files (StopWhenUnneeded)
	ctx.obj.log("Parsing", node_file, "...")
	node_lines = ctx.obj.parse_node_file(node_file)
	node_name = ctx.obj.extract_name(node_lines)
	ctx.obj.log("Writing unit files ...")
	ctx.obj.write_unit_files(node_name, node_lines, node_dir)
	
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
	node_file_systemd_parent = os.path.join(ctx.obj.systemd_path, "ef-" + type + "-parent@.service")
	node_file_systemd_child = os.path.join(ctx.obj.systemd_path, "ef-" + type + "@.service")
	
	# remove node-files from systemd-directory
	ctx.obj.log("Removing", node_file_systemd_parent, "...")
	ctx.obj.remove(node_file_systemd_parent)
	ctx.obj.log("Removing", node_file_systemd_child, "...")
	ctx.obj.remove(node_file_systemd_child)

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
	node_unit = "ef-" + type + "-parent@" + uuid + ".service"
	ctx.obj.log("Starting", node_unit, "...")
	success, _ = ctx.obj.enable_node(type, node_unit)
	if not success:
		raise click.ClickException("Could not start node: %s: The node-file contains no enablement information (i.e. an [Install]) section" % type)
	ctx.obj.start_node(type, node_unit)
	ctx.obj.echo(uuid, json=True)

@cli.command()
@click.argument("uuid")
@click.pass_context
def stop(ctx, uuid):
	"""Stop node by uuid."""
	# TODO: improve docstring
	# TODO: this command needs privileges for the systemd directory
	
	try:
		node_unit = "ef-" + ctx.obj.get_type_by_uuid(uuid) + "-parent@" + uuid + ".service"
	except IndexError:
		raise click.ClickException("Could not find started nodes for given uuid: %s" % uuid)
	ctx.obj.log("Stopping", node_unit, "...")
	ctx.obj.stop_node(type, node_unit)
	ctx.obj.disable_node(type, node_unit)

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

from simulagora import Simulagora
from time import sleep

client = Simulagora()

# create the folder, upload the files and get their identifiers
folder = client.create_folder('Code Aster piston test')
file_eids = client.upload_files(folder, 'piston.comm', 'piston.mmed', 'piston.export')

# get the "bash command" executable which will run the "as_run" command
executable = client.find_one('Executable', name='bash command')
params = {'command': 'as_run piston.export'}

# get the server type, create the study and the run, then start it
server_type = client.find_one('CloudServerType', name='m3.xlarge')
study = client.create_study('Code Aster piston test')
run = client.create_run(study, executable, server_type, file_eids, params)
client.start_run(run)

# check its state every 5 seconds until its crashed or completed
state = None
while state not in ('wfs_run_crashed', 'wfs_run_completed'):
    state = client.state(run)
    sleep(5)
print "Run " + state.rsplit('_', 1)[-1]

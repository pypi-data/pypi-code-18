import click, os, subprocess
from yacli.cli import pass_context, __location__
from git import Repo
from time import sleep

PATH = os.path.join(__location__, 'scripts')

@click.command('yadalog', short_help='Show last updated publish log on yada')
@click.option('--number', '-n', default=1, help='Number of repetition')
@click.option('--gap', '-g', default=1, help='Gap between two repetition in sec')
@pass_context
def cli(ctx, number, gap):
    """Show last updated publish log on yada"""

    SUCCESS="[INFO] BUILD SUCCESS" 
    FAILURE="[ERROR] After correcting the problems, you can resume the build with the command"

    cmd="bash {}/yada_publish_log.sh".format(PATH)

    for i in range(number) :
        subprocess.call(cmd.split())
        sleep(gap)




""" TODO
[INFO] ------------------------------------------------------------------------
[INFO] Reactor Summary:
[INFO] 
[INFO] actito-rest ....................................... SUCCESS [1.883s]
[INFO] actito-rest-webapp ................................ SUCCESS [2:16.346s]
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time: 2:18.393s
[INFO] Finished at: Mon May 08 16:15:52 CEST 2017
[INFO] Final Memory: 53M/370M
[INFO] ------------------------------------------------------------------------


[INFO] -------------------------------------------------------------
[INFO] ------------------------------------------------------------------------
[INFO] Reactor Summary:
[INFO] 
[INFO] actito-rest ....................................... SUCCESS [2.084s]
[INFO] actito-rest-webapp ................................ FAILURE [17.073s]
[INFO] ------------------------------------------------------------------------
[INFO] BUILD FAILURE
[INFO] ------------------------------------------------------------------------
[INFO] Total time: 19.304s
[INFO] Finished at: Mon May 08 16:06:38 CEST 2017
[INFO] Final Memory: 32M/329M
[INFO] ------------------------------------------------------------------------
[ERROR] Failed to execute goal org.apache.maven.plugins:maven-compiler-plugin:2.3.2:compile (default-compile) on project actito-rest-webapp: Compilation failure: Compilation failure:
[ERROR] /mnt/data/yada/workspace/actito-rest/actito-rest-webapp/src/main/java/be/citobi/webservices/www/dto/campaign/mail/MailDocumentInformationtDTO.java:[74,12] error: cannot find symbol
[ERROR] variable replyTo
[ERROR] /mnt/data/yada/workspace/actito-rest/actito-rest-webapp/src/main/java/be/citobi/webservices/www/dto/campaign/mail/MailDocumentInformationtDTO.java:[75,12] error: cannot find symbol
[ERROR] -> [Help 1]
[ERROR] 
[ERROR] To see the full stack trace of the errors, re-run Maven with the -e switch.
[ERROR] Re-run Maven using the -X switch to enable full debug logging.
[ERROR] 
[ERROR] For more information about the errors and possible solutions, please read the following articles:
[ERROR] [Help 1] http://cwiki.apache.org/confluence/display/MAVEN/MojoFailureException
[ERROR] 
[ERROR] After correcting the problems, you can resume the build with the command
[ERROR]   mvn <goals> -rf :actito-rest-webapp
"""


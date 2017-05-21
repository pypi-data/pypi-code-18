import os
import logging
import tempfile


logger = logging.getLogger(__name__)


def execute_cmd(code, stdin=None):
    from kibitzr.compat import sh
    logger.info("Executing Batch script")
    logger.debug(code)
    if stdin is not None:
        if not stdin.strip():
            logger.info("Skipping execution with empty content")
            return True, stdin
        stdin = stdin
    with tempfile.NamedTemporaryFile() as fp:
        logger.debug("Saving code to %r", fp.name)
        fp.write(code.encode('utf-8'))
        fp.flush()
        logger.debug("Launching script %r", fp.name)
        try:
            result = sh.Command("cmd")("/Q", "/C", fp.name, _in=stdin)
            ok = True
        except sh.ErrorReturnCode as exc:
            result = exc
            ok = False
    stdout = result.stdout
    stderr = result.stderr
    if ok:
        log = logger.debug
        report = stdout
    else:
        log = logger.error
        report = stderr
    log("Bash exit_code: %r", result.exit_code)
    log("Bash stdout: %s", stdout)
    log("Bash stderr: %s", stderr)
    return ok, report

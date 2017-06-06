import os
import re
import stat
import subprocess

def check_output(*args, **kw):
    p = subprocess.Popen(stdout=subprocess.PIPE, *args, **kw)
    result = p.communicate()[0]
    retcode = p.poll()
    if retcode:
        raise subprocess.CalledProcessError(retcode, args[0])
    return result

def finish(buildout):
    print('Stripping binaries ...')
    buildout_directory = buildout['buildout']['directory']
    file_binary = buildout['buildout'].get('file-binary', 'file')
    find_binary = buildout['buildout'].get('find-binary', 'find')
    strip_binary = buildout['buildout'].get('strip-binary', 'strip')
    do_not_strip_path = buildout['buildout'].get('do-not-strip-path', '').splitlines(False)

    def run_strip(path, *strip_args):
        mode = os.stat(path).st_mode
        writable_mode = mode | stat.S_IWUSR
        if mode != writable_mode:
            os.chmod(path, writable_mode)
        subprocess.check_call((strip_binary,) + strip_args + (path,))
        if mode != writable_mode:
            os.chmod(path, mode)

    # Same logic as Debian's dh_strip script.
    args = [find_binary, buildout_directory, '-type', 'f']
    try:
        shared_lib_list = []
        executable_list = []
        static_lib_list = []
        for path in check_output(args, universal_newlines=True).splitlines():
            if path in do_not_strip_path:
                continue
            file_name = os.path.basename(path)
            if re.match('.*\.(so(\..+)?|cmxs)$', file_name):
                args = [file_binary, path]
                result = check_output(args)
                if re.match(b'.*ELF.*shared.*not stripped', result):
                    shared_lib_list.append(path)
            elif os.stat(path).st_mode & stat.S_IEXEC:
                args = [file_binary, path]
                result = check_output(args)
                if re.match(b'.*ELF.*(executable|shared).* not stripped', result):
                    executable_list.append(path)
            elif re.match('lib.*\.a$', file_name):
                static_lib_list.append(path)
        for path in shared_lib_list:
            run_strip(path,
                '--remove-section=.comment',
                '--remove-section=.note',
                '--strip-unneeded',
            )
        for path in executable_list:
            run_strip(path,
                '--remove-section=.comment',
                '--remove-section=.note',
            )
        for path in shared_lib_list:
            run_strip(path,
                '--strip-debug',
            )
        print('Done.')
    except (OSError, subprocess.CalledProcessError) as e:
        print('Command failed: %s: %s' % (e, args))

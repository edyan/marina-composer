import click
import os
import stat
import subprocess
import sys

from marina.package_utils import get_venv_basedir
from urllib.request import urlretrieve
from urllib.error import HTTPError


def download_composer(install_dir: str, vm_name: str):
    # download composer if it's not the case
    if os.path.isfile(install_dir + '/composer') is True:
        return

    try:
        print('composer has not been downloaded yet, downloading ...')
        version = click.prompt('Please enter the version you want to download', default='1.4.2')

        url = 'https://getcomposer.org/download/{}/composer.phar'.format(version)
        urlretrieve(url, install_dir + '/composer')
        os.chmod(install_dir + '/composer', stat.S_IRWXU)
    except HTTPError as e:
        msg = "Can't download the file. Check that composer v{} exists at https://getcomposer.org/download/ ({})".format(version, e.reason)
        print(click.style(msg, fg='red'))
        sys.exit(1)
    except Exception as e:
        print(click.style('Unknown Error: {}'.format(e), fg='red'))
        sys.exit(1)


def run(marina, composer_cmd: str):
    vm_name = marina.get_vm_item('php', 'name')
    relative_dir = marina.current_dir_relative

    if relative_dir.startswith('www') is False:
        print(click.style('You can run composer only from a subdirectory of www', fg='red'))
        sys.exit(1)

    home = get_venv_basedir() + '/home/www-data'
    if os.path.isdir(home) and not os.path.isdir(home + '/bin'):
        os.mkdir(home + '/bin')

    download_composer(home + '/bin', vm_name)

    tty = 't' if sys.stdin.isatty() else ''
    cmd = ['docker', 'exec', '-u', 'www-data', '-i' + tty, vm_name]
    cmd += ['bash', '-c', '--']
    cmd += ['cd /var/' + relative_dir + '; exec /usr/bin/php ~/bin/composer {}'.format(composer_cmd)]
    subprocess.call(cmd, stdin=sys.stdin, stderr=subprocess.STDOUT)


@click.command(help="Run a composer command", context_settings=dict(ignore_unknown_options=True))
@click.pass_context
@click.argument('run_args', nargs=-1, type=click.UNPROCESSED)
def composer(ctx, run_args: tuple):
    run_args = ' '.join(run_args)

    marina = ctx.obj['MARINA']
    marina.check_vms_are_running()

    if marina.current_dir.find(marina.marina_base_dir) != 0:
        raise Exception('You are not in a sub-directory of your marina instance')

    run(marina, run_args)

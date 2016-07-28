import click
import os
import stat
import sys
import subprocess


def download_composer(install_dir: str, vm_name: str):
    # download composer if it's not the case
    if os.path.isfile(install_dir + '/composer.phar') is False:
        print('composer has not been downloaded yet, downloading ...')
        tty = 't' if sys.stdin.isatty() else ''
        base_cmd = ['docker', 'exec', '-u', 'www-data', '-i' + tty, vm_name, 'bash', '-c', '--']

        # run php commands to have composer
        cmd = ['cd ' + install_dir + ' ; exec /usr/bin/php -r "copy(\'https://getcomposer.org/installer\', \'composer-setup.php\');"']
        subprocess.call(base_cmd + cmd, stdin=sys.stdin)
        cmd = ['cd ' + install_dir + ' ; exec /usr/bin/php -r "if (hash_file(\'SHA384\', \'composer-setup.php\') === \'e115a8dc7871f15d853148a7fbac7da27d6c0030b848d9b3dc09e2a0388afed865e6a3d6b3c0fad45c48e2b5fc1196ae\') { echo \'Installer verified\'; } else { echo \'Installer corrupt\'; unlink(\'composer-setup.php\'); } echo PHP_EOL;"']
        subprocess.call(base_cmd + cmd, stdin=sys.stdin)
        cmd = ['cd ' + install_dir + ' ; exec /usr/bin/php composer-setup.php']
        subprocess.call(base_cmd + cmd, stdin=sys.stdin)
        cmd = ['cd ' + install_dir + ' ; exec /usr/bin/php -r "unlink(\'composer-setup.php\');"']
        subprocess.call(base_cmd + cmd, stdin=sys.stdin)


def run(lamp, composer_cmd: str):
    vm_name = lamp.get_vm_item('php', 'name')
    relative_dir = lamp.current_dir_relative

    download_composer('home/www-data/bin', vm_name)

    tty = 't' if sys.stdin.isatty() else ''
    cmd = ['docker', 'exec', '-u', 'www-data', '-i' + tty, vm_name]
    cmd += ['bash', '-c', '--']
    cmd += ['cd /var/' + relative_dir + '; exec /usr/bin/php ~/bin/composer.phar {}'.format(composer_cmd)]
    subprocess.call(cmd, stdin=sys.stdin, stderr=subprocess.STDOUT)


@click.command(help="Run a composer command", context_settings=dict(ignore_unknown_options=True))
@click.pass_context
@click.argument('run_args', nargs=-1, type=click.UNPROCESSED)
def composer(ctx, run_args: tuple):
    run_args = ' '.join(run_args)

    lamp = ctx.obj['LAMP']
    lamp.check_vms_are_running()

    if lamp.current_dir.find(lamp.lamp_base_dir) != 0:
        raise Exception('You are not in a sub-directory of your lamp instance')

    run(lamp, run_args)

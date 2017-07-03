import click
import os
import stat
import sys
import subprocess

from lib import command


def download_composer(install_dir: str, vm_name: str):
    # download composer if it's not the case
    if os.path.isfile(install_dir + '/composer.phar') is False:
        print('composer has not been downloaded yet, downloading ...')
        tty = 't' if sys.stdin.isatty() else ''
        base_cmd = ['docker', 'exec', '-u', 'www-data', '-i' + tty, vm_name, 'bash', '-c', '--']

        # run php commands to have composer
        cmd = ['cd ' + install_dir + ' ; exec /usr/bin/php -r "copy(\'https://getcomposer.org/installer\', \'composer-setup.php\');"']
        command.launch_cmd_displays_output(base_cmd + cmd)
        
        cmd = ['cd ' + install_dir + ' ; exec /usr/bin/php -r "if (hash_file(\'SHA384\', \'composer-setup.php\') === \'669656bab3166a7aff8a7506b8cb2d1c292f042046c5a994c43155c0be6190fa0355160742ab2e1c88d40d5be660b410\') { echo \'Installer verified\'; } else { echo \'Installer corrupt\'; unlink(\'composer-setup.php\'); } echo PHP_EOL;"']
        command.launch_cmd_displays_output(base_cmd + cmd)
        
        cmd = ['cd ' + install_dir + ' ; exec /usr/bin/php composer-setup.php']
        command.launch_cmd_displays_output(base_cmd + cmd)
        
        cmd = ['cd ' + install_dir + ' ; exec /usr/bin/php -r "unlink(\'composer-setup.php\');"']
        command.launch_cmd_displays_output(base_cmd + cmd)


def run(lamp, composer_cmd: str):
    vm_name = lamp.get_vm_item('php', 'name')
    relative_dir = lamp.current_dir_relative

    download_composer('home/www-data/bin', vm_name)

    tty = 't' if sys.stdin.isatty() else ''
    cmd = ['docker', 'exec', '-u', 'www-data', '-i' + tty, vm_name]
    cmd += ['bash', '-c', '--']
    cmd += ['cd /var/' + relative_dir + '; exec /usr/bin/php ~/bin/composer.phar {}'.format(composer_cmd)]
    command.launch_cmd_displays_output(cmd)


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

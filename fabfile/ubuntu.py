from fabric.api import hosts, run, sudo, env, cd, settings
from fabric.contrib.files import upload_template
from fabric.context_managers import prefix

env.hosts = ['root@128.199.71.132']

def apt_get(cmd, opts=[], *pkgs):
	sudo('apt-get {options} {command} {packages}'.format(
			options = ' '.join(opts), 
			packages = ' '.join(pkgs), 
			command = cmd,
		),
	)

def apt_get_install(pkg_name):
	apt_get('install', ['-y'], pkg_name)

def apt_get_update():
	apt_get(cmd='update')

def git_clone(repo, dest_dir='', *opts):
	run('git clone {options} {repo} {dir}'.format(
			repo = repo,
			dir = dest_dir,
			options = ' '.join(opts)
		)
	)

def virtualenv(dest_dir, *opts):
	run('virtualenv {options} {dir}'.format(
			options = ' '.join(opts),
			dir = dest_dir,
		)
	)

def source(filename, *args):
	env.filename = filename
	env.arguments = ' '.join(args)
	run('source {filename} {arguments}'.format(**env))

def pip_install(reqs, *opts):
	run('pip install {options} {requirements}'.format(
			requirements = reqs,
			options = ' '.join(opts),
		)
	)

def upload_nginx_config(config_filename, dj_project_root):
	upload_template(
		filename = 'nginx.conf',
		destination = '/etc/nginx/sites-available/' + config_filename,
		use_jinja = True,
		template_dir = 'fabfile',
		context = locals(),
		backup = False,
	)

def upload_gunicorn_config(repo_root, dj_settings_module, gunicorn_exe, dj_project_name):
	upload_template(
		filename = 'gunicorn.conf',
		destination = '/etc/init/gunicorn.conf',
		use_jinja = True,
		template_dir = 'fabfile',
		context = locals(),
		backup = False,
	)

def test(current_password, new_password):
	with settings(
		prompts = {
			'(current) UNIX password: ': current_password,
			'Enter new UNIX password: ': new_password,
			'Retype new UNIX password: ': new_password,
		}
	):
		run('ls')


def initialize():
	
	apt_get_update()
	apt_get_install('git')
	apt_get_install('libpq-dev')
	
	with cd('/home'), settings(warn_only=True):
		git_clone('https://github.com/ltiao/basketball-intelligence.git')
	
	virtualenv('/opt/bball_intel')
	
	with cd('/home/basketball-intelligence'), prefix('source /opt/bball_intel/bin/activate'):
		pip_install('requirements/dev_digital_ocean.txt', '-r')

	nginx_config_filename = 'bball_intel'

	upload_nginx_config(
		nginx_config_filename,
		'/home/basketball-intelligence/bball_intel',
	)

	run('rm /etc/nginx/sites-enabled/django')
	
	with cd('/etc/nginx/sites-enabled/'):
		run('ln -s /etc/nginx/sites-available/' + nginx_config_filename)

	run('sudo service nginx restart')

	upload_gunicorn_config(
		repo_root = '/home/basketball-intelligence',
		dj_settings_module = 'bball_intel.settings.staging',
		gunicorn_exe = '/opt/bball_intel/bin/gunicorn',
		dj_project_name = 'bball_intel'
	)

	run('initctl reload-configuration')
	run('service gunicorn restart')
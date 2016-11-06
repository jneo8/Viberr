from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run 
import random

# fabric doesn't support python3
REPO_URL = 'https://github.com/jneo8/Viberr.git'

def deploy():
    # site_folder = '/home/%s/viberr' % ('ubuntu')
    site_folder = '/vagrant/deploy_test'
    project_folder = site_folder + '/Viberr'
    _create_directory_structure_if_necessary(site_folder, project_folder)
    _get_latest_source(site_folder, project_folder)
    # _update_setting(project_folder)
    _update_virtualenv(site_folder, project_folder)
    _update_static_files(project_folder)
    _update_database(project_folder)

def _create_directory_structure_if_necessary(site_folder, project_folder):

    run('mkdir -p %s' % (site_folder))

def _get_latest_source(site_folder, project_folder):
    if exists(project_folder + '/.git'):
        run('cd %s && git fetch' % (project_folder,))
    else:
        run('cd %s && git clone %s' % (site_folder, REPO_URL))
    # currect_commit = local("git clone -n 1 --format=%H", capture=False)
    # run('cd %s &&git reset --hard %s' % (project_folder, currect_commit))


# update or create env
def _update_virtualenv(site_folder, project_folder):
    virtualenv_folder = site_folder+'/env'
    if not exists(virtualenv_folder+'/bin/pip'):
        run('sudo apt-get install -y python3.4-venv')
        run('cd %s && python3.4 -m venv env' % (site_folder))

    run('%s/bin/pip install -r %s/requirments.txt' % (virtualenv_folder, project_folder))

def _update_static_files(project_folder):
    run('cd %s && export DJANGO_SETTINGS_MODULE=website.settings.local &&  ../env/bin/python manage.py collectstatic --noinput'
     % (project_folder))

def _update_database(project_folder):
    run('cd %s && export DJANGO_SETTINGS_MODULE=website.settings.local &&  ../env/bin/python manage.py migrate --noinput'
     % (project_folder))
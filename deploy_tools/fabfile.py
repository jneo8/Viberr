# -*- coding:utf-8 -*-
from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random

# fabric doesn't support python3
REPO_URL = 'https://github.com/jneo8/Viberr.git'

env.hosts = ['52.196.216.28']
SITENAME='viberr'
env.user = 'ubuntu'
env.key_filename = '/vagrant/practice/key_james0910238727.pem'


def deploy():
    # home/ubuntu/sites/viberr_52.196.216.28
    site_folder = '/home/%s/sites/%s' % (env.user, SITENAME)
    # site_folder = '/vagrant/deploy_test'
    project_folder = site_folder + '/Viberr'
    _create_directory_structure_if_necessary(site_folder, project_folder)
    _get_latest_source(site_folder, project_folder)
    # _update_setting(project_folder)
    _update_virtualenv(site_folder, project_folder)
    _update_static_files(project_folder)
    _update_database(project_folder)
    _set_nginx(project_folder)


def _test():
    run('cd /home/ubuntu && mkdir d_test')


def _create_directory_structure_if_necessary(site_folder, project_folder):

    run('mkdir -p %s' % (site_folder))


def _get_latest_source(site_folder, project_folder):
    if exists(project_folder + '/.git'):
        run('cd %s && git fetch' % (project_folder,))
    else:
        run('cd %s && git clone %s' % (site_folder, REPO_URL))
    currect_commit = local('git log -n 1 --format=%H', capture=True)
    # get error if local doesn't push last commit
    run('cd %s && git reset --hard %s' % (project_folder, currect_commit))


# update or create env
def _update_virtualenv(site_folder, project_folder):
    virtualenv_folder = site_folder + '/env'
    if not exists(virtualenv_folder + '/bin/pip'):
        run('sudo apt-get install -y python3.4-venv')
        run('cd %s && python3.4 -m venv env' % (site_folder))

    run('%s/bin/pip install -r %s/requirements.txt' %
        (virtualenv_folder, project_folder))


def _update_static_files(project_folder):
    run('cd %s && export DJANGO_SETTINGS_MODULE=website.settings.production &&  ../env/bin/python manage.py collectstatic --noinput'
        % (project_folder))


def _update_database(project_folder):
    run('cd %s && export DJANGO_SETTINGS_MODULE=website.settings.production &&  ../env/bin/python manage.py migrate --noinput'
        % (project_folder))


def _set_nginx(project_folder):
    nginx_name = 'viberr_test_nginx'
    gunicorn_upstart_name = 'viberr_test_gunicorn-upstart'
    # gunicorn_conf_name = 'gunicorn_upstart_name+.conf'
    # 設定 /etc/nignx/viberr_test_nginx
    run('sed "s/SITENAME/%s/g" \
        %s/deploy_tools/nginx.template.conf | \
     sudo tee /etc/nginx/sites-available/%s' % (env.host, project_folder, nginx_name))
    # ln -s to sites-enabled
    if not exists('/etc/nginx/sites-enabled/%s' % (nginx_name)):
        run('sudo ln -s /etc/nginx/sites-available/%s /etc/nginx/sites-enabled/%s ' % (nginx_name, nginx_name))
    run('sed s/SITENAME/%s/g \
        %s/deploy_tools/gunicorn-upstart.template.conf | \
        sudo tee /etc/init/%s' % (env.host, project_folder, gunicorn_upstart_name+'.conf'))

    run('sudo service nginx reload')
    run('sudo start %s' % gunicorn_upstart_name)





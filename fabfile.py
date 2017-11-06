from fabric.api import run, cd, task, runs_once, lcd, local


@task(alias='dp')
def deploy_production():
    with cd('/web/production/'):
        run('git pull && git checkout develop && git pull')
        run("""
        . /opt/venv/production/bin/activate &&
        pip install -r requirements.txt &&
        python manage.py collectstatic --noinput &&
        python manage.py migrate
        """)
        run('supervisorctl restart uwsgi_production')


@task(alias='nr')
@runs_once
def register_deployment(git_path):
    with(lcd(git_path)):
        revision = local('git log -n 1 --pretty="format:%H"', capture=True)
        branch = local('git rev-parse --abbrev-ref HEAD', capture=True)
        local('curl https://intake.opbeat.com/api/v1/organizations/c3eb3a03ffc94916acca0329c2db5cbe/apps/b6b0bef243/releases/'
              ' -H "Authorization: Bearer 2c878bbd8c1bbb38a1d528e33c0ee70d3f821851"'
              ' -d rev="{}"'
              ' -d branch="{}"'
              ' -d status=completed'.format(revision, branch))

from fabric.api import run, env, cd, runs_once, lcd, local, task


@task(alias='dp')
def deploy_production():
    with cd('/web/production/'):
        run('git pull && git checkout develop')
        run("""
        . /opt/venv/production/bin/activate &&
        pip install -r requirements.txt &&
        python manage.py collectstatic --noinput &&
        python manage.py migrate
        """)
        run('supervisorctl restart uwsgi_production')

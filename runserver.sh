python manage.py collectstatic --no-input

python manage.py migrate
# The blow is unique to DO Apps
gunicorn --worker-tmp-dir /dev/shm djcrm.wsgi

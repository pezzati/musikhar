FROM canto_library:1.0.0
#
#RUN apt-get update && \
#    pip3 install uwsgi
#
#COPY requirements.txt /web/production/requirements.txt
RUN mkdir -p /webfiles/media/production
RUN mkdir -p /webfiles/staticfiles/production
#
#RUN mkdir -p /var/log/canto-logs/production/django
#RUN mkdir -p /var/log/canto-logs/production/uwsgi/reqlog
#RUN mkdir -p /var/log/canto-logs/production/uwsgi/errlog
#RUN touch /var/log/canto-logs/production/django/application.log
#RUN touch /var/log/canto-logs/production/django/celery.log
#RUN touch /var/log/canto-logs/production/django/errors.log

#RUN chown -R www-data:www-data /var/log/canto-logs/


#RUN pip3 install -r /web/production/requirements.txt

COPY / /web/production/
ENV DJANGO_SETTINGS_MODULE=musikhar.server_settings.production
ENV TZ_LOG_DIR=/var/log/canto/
ENV DB_USER=forat_production_user
ENV DB_PASSWORD=pDFszP59gTtExZv8u2W02ziXFh3ndMbtf
ENV SECRET_KEY=56b35e1a2894440e28ca546dbd184dfd
ENV LC_ALL='en_US.UTF-8'
ENV LANG='en_US.UTF-8'
ENV MEDIA_ROOT=/webfiles/media/production
ENV STATIC_ROOT=/webfiles/staticfiles/production

EXPOSE 3031

CMD ["uwsgi", "--ini", "/web/production/uwsgi_production.ini"]
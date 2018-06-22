# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals
import csv

import os
from datetime import datetime as dt
import jdatetime
from celery import shared_task
from django.conf import settings

from analytics.models import Tag, UserAction
from karaoke.models import Post, Karaoke, Poem, Genre
from loginapp.models import User, Artist
from mediafiles.models import AsyncTask, MediaFile
from musikhar.utils import celery_logger, app_logger


def delete_all(created_objs):
    for obj in created_objs:
        obj.delete()


@shared_task
def create_karaokes(task_id):
    task = AsyncTask.objects.get(id=task_id)
    if task.state in [AsyncTask.STATE_DONE, AsyncTask.STATE_PROCESSING, AsyncTask.STATE_ERROR]:
        return

    celery_logger.info('[CREATE_KARAOKE] task:{}'.format(task.__str__()))
    app_logger.info('[CREATE_KARAOKE] task:{}'.format(task.__str__()))

    task.state = AsyncTask.STATE_PROCESSING
    task.save(update_fields=['state'])

    abs_path = task.file.path
    try:
        rows = []
        with open(abs_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            fieldnames = reader.fieldnames
            for row in reader:
                rows.append(row)

        err_rows = []
        row_index = 0
        upload_paths = {'file': None, 'full_file': None, 'cover_photo': None}
        for row in rows:
            row_index += 1
            created_objects = []
            has_error = False

            # print('name: {}'.format(row.get('name')))
            post, created = Post.objects.get_or_create(
                name=row.get('name'),
                subclass_type=Post.KARAOKE_TYPE,
                karaoke__artist__name=row.get('artist'),
                defaults={'description': row.get('description')},
            )
            print('post created')
            # if not created:
            #     if post.karaoke:
            #         row['error'] = 'karaoke exists'
            #         err_rows.append(row)
            #         continue

            celery_logger.info('[CREATE_KARAOKE] task:{}, row:{}, POST CREATED'.format(task.__str__(), row_index))
            app_logger.info('[CREATE_KARAOKE] task:{}, row:{}, POST CREATED'.format(task.__str__(), row_index))

            created_objects.append(post)

            # Files
            file_fields = upload_paths.copy()
            for field in upload_paths:
                try:
                    if row.get(field) and '!!!ERROR!!!' not in row.get(field):
                        if field != 'cover_photo':
                            file_fields[field], trash = MediaFile.objects.get_or_create(
                                user=User.system_user(),
                                path=row.get(field),
                                type=MediaFile.KARAOKE_TYPE,
                                resource_type=MediaFile.BACKTORY_RESOURCE
                            )
                        else:
                            file_fields[field], trash = MediaFile.objects.get_or_create(
                                user=User.system_user(),
                                path=row.get(field),
                                type=MediaFile.COVER_PHOTO,
                                resource_type=MediaFile.BACKTORY_RESOURCE
                            )
                        celery_logger.info('[CREATE_KARAOKE] task:{}, row:{}, {} CREATED'.format(task.__str__(), row_index, field))
                        app_logger.info('[CREATE_KARAOKE] task:{}, row:{}, {} CREATED'.format(task.__str__(), row_index, field))

                    elif field == 'file':
                        has_error = True

                except Exception as e:
                    # print('In Upload Paths: {}'.format(str(e)))
                    has_error = True
                    row[field] = 'ERROR: {}'.format(str(e))
            if has_error:
                celery_logger.info('[CREATE_KARAOKE] task:{}, row:{}. DELETE ALL'.format(task.__str__(), row_index))
                app_logger.info('[CREATE_KARAOKE] task:{}, row:{}. DELETE ALL'.format(task.__str__(), row_index))

                delete_all(created_objects)
                err_rows.append(row)
                continue
            print('FILES ADDED')
            try:
                if file_fields['cover_photo']:
                    post.cover_photo = file_fields['cover_photo']
                    post.save()
                    print('cover photo added')
                # tags
                str_tags = row.get('tags').split('|')
                # print('tags: {}'.format(row.get('tags')))
                tags = []
                for str_tag in str_tags:
                    while str_tag and str_tag[0] == ' ':
                        str_tag = str_tag[1:]
                    if not str_tag:
                        continue
                    # print('tag: {}'.format(str_tag))
                    tag, created = Tag.objects.get_or_create(name=str_tag)
                    print('tag append')
                    tags.append(tag)
                post.add_tags(tags)
                print('add tags')
                celery_logger.info('[CREATE_KARAOKE] task:{}, row:{}, TAGS CREATED'.format(task.__str__(), row_index))
                app_logger.info('[CREATE_KARAOKE] task:{}, row:{}, TAGS CREATED'.format(task.__str__(), row_index))

                # print('genre: {}'.format(row.get('genre')))
                if row.get('genre'):
                    post.genre, trash = Genre.objects.get_or_create(name=row.get('genre'))
                    post.save()
                    celery_logger.info('[CREATE_KARAOKE] task:{}, row:{}, GENRE CREATED'.format(task.__str__(), row_index))
                    app_logger.info('[CREATE_KARAOKE] task:{}, row:{}, GENRE CREATED'.format(task.__str__(), row_index))

                # karaoke
                karaoke, created = Karaoke.objects.get_or_create(
                    post=post,
                    defaults={'file': file_fields.get('file'), 'full_file': file_fields.get('full_file')}
                )
                celery_logger.info('[CREATE_KARAOKE] task:{}, row:{}, KARAOKE CREATED'.format(task.__str__(), row_index))
                app_logger.info('[CREATE_KARAOKE] task:{}, row:{}, KARAOKE CREATED'.format(task.__str__(), row_index))

                # Artist
                # print('artists: {}'.format(row.get('artist')))
                if row.get('artist'):
                    artist, trash = Artist.objects.get_or_create(name=row.get('artist'))
                    karaoke.artist = artist
                    karaoke.save()
                    celery_logger.info('[CREATE_KARAOKE] task:{}, row:{}, ARTIST CREATED'.format(task.__str__(), row_index))
                    app_logger.info('[CREATE_KARAOKE] task:{}, row:{}, ARTIST CREATED'.format(task.__str__(), row_index))

                # lyric
                # print('lyric: {}'.format(row.get('lyric')))
                if row.get('lyric'):
                    poem_post, created = Post.objects.get_or_create(
                        name=row.get('lyric_name', 'poem_{}_by_{}'.format(post.name, row.get('artist', 'anonymous'))),
                        subclass_type=Post.POEM_TYPE
                    )
                    celery_logger.info('[CREATE_KARAOKE] task:{}, row:{}, POEM POST CREATED'.format(task.__str__(), row_index))
                    app_logger.info('[CREATE_KARAOKE] task:{}, row:{}, POEM POST CREATED'.format(task.__str__(), row_index))

                    created_objects.append(poem_post)
                    lyric, created = Poem.objects.get_or_create(
                        post=poem_post,
                        defaults={'text': row.get('lyric')}
                    )
                    celery_logger.info('[CREATE_KARAOKE] task:{}, row:{}, LYRIC CREATED'.format(task.__str__(), row_index))
                    app_logger.info('[CREATE_KARAOKE] task:{}, row:{}, LYRIC CREATED'.format(task.__str__(), row_index))

                    # lyric poet
                    # print('poet: {}'.format(row.get('lyric_poet')))
                    if row.get('lyric_poet'):
                        lyric_poet, trash = Artist.objects.get_or_create(name=row.get('lyric_poet'))
                        lyric.poet = lyric_poet
                        lyric.save()
                        celery_logger.info(
                            '[CREATE_KARAOKE] task:{}, row:{}, LYRIC POET CREATED'.format(task.__str__(), row_index))
                        app_logger.info(
                            '[CREATE_KARAOKE] task:{}, row:{}, LYRIC POET CREATED'.format(task.__str__(), row_index))

                    karaoke.lyric = lyric
                    karaoke.save()
            except Exception as e:
                celery_logger.info('[CREATE_KARAOKE_ERROR] task:{}, row:{}, loop_error:{}'.format(task.__str__(), row_index, str(e)))
                app_logger.info('[CREATE_KARAOKE_ERROR] task:{}, row:{}, loop_error:{}'.format(task.__str__(), row_index, str(e)))

                delete_all(created_objects)
                row['error'] = row['error'] + ' {}'.format(str(e))
                err_rows.append(row)

        error_path = abs_path + '.err'
        with open(error_path, 'w+', newline='') as target_csv:
            writer = csv.DictWriter(target_csv, fieldnames=fieldnames)
            writer.writeheader()
            for row in err_rows:
                writer.writerow(row)

        celery_logger.info('[CREATE_KARAOKE] task:{}, ERROR FILE CREATED'.format(task.__str__()))
        app_logger.info('[CREATE_KARAOKE] task:{}, ERROR FILE CREATED'.format(task.__str__()))

        file_name = error_path.replace(settings.MEDIA_ROOT, '/').replace('//', '/')
        if file_name[0] == '/':
            file_name = file_name[1:]
        task.error_file.name = file_name

        task.state = AsyncTask.STATE_DONE
        task.save(update_fields=['state', 'error_file'])
        celery_logger.info('[CREATE_KARAOKE] task:{}, TASK SAVED'.format(task.__str__()))
        app_logger.info('[CREATE_KARAOKE] task:{}, TASK SAVED'.format(task.__str__()))

    except Exception as e:
        celery_logger.info('[CREATE_KARAOKE_ERROR] task:{}, end_error:{}'.format(task.__str__(), str(e)))
        app_logger.info('[CREATE_KARAOKE_ERROR] task:{}, end_error:{}'.format(task.__str__(), str(e)))

        error_path = abs_path + '.err'
        with open(error_path, 'w+', newline='') as target_csv:
            target_csv.write(str(e))

        file_name = error_path.replace(settings.MEDIA_ROOT, '/').replace('//', '/')
        if file_name[0] == '/':
            file_name = file_name[1:]
        task.error_file.name = file_name
        task.state = AsyncTask.STATE_ERROR
        task.save(update_fields=['state', 'error_file'])


@shared_task
def test():
    print(os.environ)


def user_action_report(target_file):
    user_actions = UserAction.objects.all()

    csv_writer = csv.writer(target_file)
    csv_writer.writerow(
        [
            'user',
            'date',
            'time',
            'action',
            'detail',
            'session'
        ]
    )

    for action in user_actions:
        detail = action.detail
        if action.action == 'Karaoke Tapped':
            try:
                post = Post.objects.get(id=action.detail)
                detail = '{} - {}'.format(post.name, post.genre.name)
            except:
                pass

        datetime = action.datetime
        jalali_time = jdatetime.GregorianToJalali(
            gday=datetime.day,
            gmonth=datetime.month,
            gyear=datetime.year
        )
        csv_writer.writerow(
            [
                action.user.username,
                '{}-{}-{}'.format(jalali_time.jyear, jalali_time.jmonth, jalali_time.jday),
                datetime.strftime('%H:%M:%S'),
                action.action,
                detail,
                action.session

            ]
        )
    return target_file

@shared_task
def generate_report(task_id):
    task = AsyncTask.objects.get(id=task_id)
    task.state = AsyncTask.STATE_PROCESSING
    task.save(update_fields=['state'])

    filename = '{}.csv'.format(task.name)
    file_write_path = task.get_report_path().split('/')

    try:
        os.mkdir('{}/async_files'.format(settings.MEDIA_ROOT).replace('//', '/'))
    except:
        pass
    try:
        os.mkdir('{}/async_files/reports'.format(settings.MEDIA_ROOT).replace('//', '/'))
    except:
        pass
    try:
        time = dt.now()
        os.mkdir('{}/async_files/reports/{}_{}'.format(settings.MEDIA_ROOT, time.year, time.month).replace('//', '/'))
    except:
        pass

    file_path = '{}/{}/{}'.format(settings.MEDIA_ROOT, task.get_report_path(), filename).replace('//', '/')
    file_url = '/{}/{}'.format(task.get_report_path(), filename).replace('//', '/')
    target_file = open(file_path, 'w')
    if 'UserAction' in task.name:
        target_file = user_action_report(target_file)

    target_file.close()

    task.file.name = file_url
    task.state = AsyncTask.STATE_DONE
    task.save()

from __future__ import absolute_import, unicode_literals
import csv

from celery import shared_task
from django.conf import settings

from analytics.models import Tag
from karaoke.models import Post, Karaoke, Poem, Genre
from loginapp.models import User, Artist
from mediafiles.models import AsyncTask, MediaFile
from musikhar.utils import celery_logger


def delete_all(created_objs):
    for obj in created_objs:
        obj.delete()


@shared_task
def create_karaokes(task_id):
    task = AsyncTask.objects.get(id=task_id)
    if task.state in [AsyncTask.STATE_DONE, AsyncTask.STATE_PROCESSING, AsyncTask.STATE_ERROR]:
        return

    celery_logger.info('[CREATE_KARAOKE] task:{}'.format(task.__str__()))

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

            post, created = Post.objects.get_or_create(
                name=row.get('name'),
                subclass_type=Post.KARAOKE_TYPE,
                defaults={'description': row.get('description')},
            )
            if created:
                if post.karaoke:
                    row['error'] = 'karaoke exists'
                    err_rows.append(row)
                    continue

            celery_logger.info('[CREATE_KARAOKE] task:{}, row:{}, POST CREATED'.format(task.__str__(), row_index))

            created_objects.append(post)

            # Files
            file_fields = upload_paths.copy()
            for field in upload_paths:
                try:
                    if row.get(field):
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

                except Exception as e:
                    has_error = True
                    row[field] = 'ERROR: {}'.format(str(e))

            if has_error:
                celery_logger.info('[CREATE_KARAOKE] task:{}, row:{}. DELETE ALL'.format(task.__str__(), row_index))
                delete_all(created_objects)
                err_rows.append(row)
                continue
            try:
                if file_fields['cover_photo']:
                    post.cover_photo = file_fields['cover_photo']
                    post.save()
                # tags
                str_tags = row.get('tags').split('|')
                tags = []
                for str_tag in str_tags:
                    tag, created = Tag.objects.get_or_create(name=str_tag)
                    tags.append(tag)
                post.add_tags(tags)
                celery_logger.info('[CREATE_KARAOKE] task:{}, row:{}, TAGS CREATED'.format(task.__str__(), row_index))

                if row.get('genre'):
                    post.genre, trash = Genre.objects.get_or_create(name=row.get('genre'))
                    post.save()
                    celery_logger.info('[CREATE_KARAOKE] task:{}, row:{}, GENRE CREATED'.format(task.__str__(), row_index))

                # karaoke
                karaoke = Karaoke.objects.create(
                    post=post,
                    file=file_fields.get('file'),
                    full_file=file_fields.get('full_file')
                )
                celery_logger.info('[CREATE_KARAOKE] task:{}, row:{}, KARAOKE CREATED'.format(task.__str__(), row_index))

                # Artist
                if row.get('artist'):
                    artist, trash = Artist.objects.get_or_create(name=row.get('artist'))
                    karaoke.artist = artist
                    karaoke.save()
                    celery_logger.info('[CREATE_KARAOKE] task:{}, row:{}, ARTIST CREATED'.format(task.__str__(), row_index))

                # lyric
                if row.get('lyric'):
                    poem_post = Post.objects.create(
                        name=row.get('lyric_name', 'poem_{}'.format(post.name)),
                        subclass_type=Post.POEM_TYPE
                    )
                    celery_logger.info('[CREATE_KARAOKE] task:{}, row:{}, POEM POST CREATED'.format(task.__str__(), row_index))

                    created_objects.append(poem_post)
                    lyric = Poem.objects.create(
                        post=poem_post,
                        text=row.get('lyric')
                    )
                    celery_logger.info('[CREATE_KARAOKE] task:{}, row:{}, LYRIC CREATED'.format(task.__str__(), row_index))

                    # lyric poet
                    if row.get('lyric_poet'):
                        lyric_poet, trash = Artist.objects.get_or_create(name=row.get('lyric_poet'))
                        lyric.poet = lyric_poet
                        lyric.save()
                        celery_logger.info(
                            '[CREATE_KARAOKE] task:{}, row:{}, LYRIC POET CREATED'.format(task.__str__(), row_index))

                    karaoke.lyric = lyric
                    karaoke.save()
            except Exception as e:
                celery_logger.info('[CREATE_KARAOKE_ERROR] task:{}, row:{}, loop_error:{}'.format(task.__str__(), row_index, str(e)))
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

        file_name = error_path.replace(settings.MEDIA_ROOT, '/').replace('//', '/')
        if file_name[0] == '/':
            file_name = file_name[1:]
        task.error_file.name = file_name

        task.state = AsyncTask.STATE_DONE
        task.save(update_fields=['state', 'error_file'])
        celery_logger.info('[CREATE_KARAOKE] task:{}, TASK SAVED'.format(task.__str__()))

    except Exception as e:
        celery_logger.info('[CREATE_KARAOKE_ERROR] task:{}, end_error:{}'.format(task.__str__(), str(e)))
        error_path = abs_path + '.err'
        with open(error_path, 'w+', newline='') as target_csv:
            target_csv.write(str(e))

        file_name = error_path.replace(settings.MEDIA_ROOT, '/').replace('//', '/')
        if file_name[0] == '/':
            file_name = file_name[1:]
        task.error_file.name = file_name
        task.state = AsyncTask.STATE_ERROR
        task.save(update_fields=['state', 'error_file'])

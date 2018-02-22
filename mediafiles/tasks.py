from __future__ import absolute_import, unicode_literals
import csv

from celery import shared_task

from analytics.models import Tag
from karaoke.models import Post, Karaoke, Poem
from loginapp.models import User, Artist
from mediafiles.models import AsyncTask, MediaFile


def delete_all(created_objs):
    for obj in created_objs:
        obj.delet()

@shared_task
def create_karaokes(task_id):
    task = AsyncTask.objects.get(id=task_id)
    if task.state in [AsyncTask.STATE_DONE, AsyncTask.STATE_PROCESSING, AsyncTask.STATE_ERROR]:
        return

    task.state = AsyncTask.STATE_PROCESSING
    task.save(update_fields=['state'])

    abs_path = task.file.path
    rows = []
    with open(abs_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames
        for row in reader:
            rows.append(row)

    res_rows = []
    err_rows = []
    upload_paths = {'file': None, 'full_file': None, 'cover_photo': None}
    for row in rows:
        created_objects = []
        has_error = False

        post = Post.objects.create(
            name=row.get('name'),
            subclass_type=Post.KARAOKE_TYPE,
            description=row.get('description'),
        )
        created_objects.append(post)

        # Files
        file_fields = upload_paths.copy()
        for field in upload_paths:
            try:
                if row.get(field):
                    file_fields[field] = MediaFile.objects.create(
                        user=User.system_user(),
                        path=row.get(field),
                        type=MediaFile.KARAOKE_TYPE,
                        resource_type=MediaFile.BACKTORY_RESOURCE
                    )
                    created_objects.append(file_fields[field])
            except Exception as e:
                has_error = True
                row[field] = 'ERROR: {}'.format(str(e))

        if has_error:
            delete_all(created_objects)
            err_rows.append(row)
        try:
            # tags
            str_tags = row.get('tags').split('|')
            tags = [Tag.objects.get_or_create(name=tag_name) for tag_name in str_tags]
            post.add_tags(tags)

            # karaoke
            karaoke = Karaoke.objects.create(
                post=post,
                file=file_fields.get('file'),
                full_file=file_fields.get('full_file'),

            )

            # Artist
            if row.get('artist'):
                artist = Artist.objects.get_or_create(name=row.get('artist'))
                karaoke.artist = artist
                karaoke.save()

            # lyric
            if row.get('lyric'):
                poem_post = Post.objects.create(
                    name=row.get('lyric_name', 'poem_{}'.format(post.name)),
                    subclass_type=Post.POEM_TYPE
                )
                created_objects.append(poem_post)
                lyric = Poem.objects.create(
                    post=poem_post,
                    text=row.get('lyric')
                )
                # lyric poet
                if row.get('lyric_poet'):
                    lyric_poet = Artist.objects.get_or_create(name=row.get('lyric_poet'))
                    lyric.poet = lyric_poet
                    lyric.save()

                karaoke.lyric = lyric
                karaoke.save()
        except Exception as e:
            err_rows.append(str(e))


    task.state = AsyncTask.STATE_DONE
    task.save(update_fields=['state'])

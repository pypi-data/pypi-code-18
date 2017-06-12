""".. Ignore pydocstyle D400.

==========
Core views
==========

.. autofunction:: rolca.core.views.upload

"""
import io
import json
import logging
import os
import zipfile

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import (
    HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotAllowed,
)
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from django.views.decorators.csrf import csrf_exempt


from rolca.core.models import Contest, File, Photo, Theme


logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


@login_required
def download_contest(request, contest_id):
    """Download all photos of the contest as zip file."""
    contest = get_object_or_404(Contest, pk=contest_id)

    buffer = io.BytesIO()
    zip_archive = zipfile.ZipFile(buffer, mode='w')

    for theme in Theme.objects.filter(contest=contest):
        # Create empty directory
        zip_info = zipfile.ZipInfo(
            os.path.join(slugify(contest.title), slugify(theme.title)) + "/"
        )
        zip_archive.writestr(zip_info, '')

        no_title_count = 0
        for photo in Photo.objects.filter(theme=theme):
            if not photo.title:
                no_title_count += 1
            zip_file_name = '{}.jpg'.format(
                slugify('{}-{}'.format(photo.author, photo.title or no_title_count))
            )
            zip_path = os.path.join(slugify(contest.title), slugify(theme.title), zip_file_name)
            zip_archive.write(photo.photo.file.path, zip_path)

    zip_archive.close()

    response = HttpResponse(buffer.getvalue(), content_type='application/x-zip-compressed')

    slugified_title = slugify(contest.title)
    response['Content-Disposition'] = 'attachment; filename="{}.zip"'.format(slugified_title)
    response['Content-Length'] = buffer.tell()

    return response


@csrf_exempt
def upload(request):
    """Handle uploaded photo and create new File object."""
    if request.method != 'POST':
        logger.warning("Upload request other than POST.")
        return HttpResponseNotAllowed(['POST'], 'Only POST accepted')

    if not request.user.is_authenticated():
        logger.warning('Anonymous user tried to upload file.')
        return HttpResponseForbidden('Please login!')

    if request.FILES is None:
        logger.warning("Upload request without attached image.")
        return HttpResponseBadRequest('Must have files attached!')

    fn = request.FILES[u'files[]']
    logger.info("Image received.")

    file_ = File(file=fn, user=request.user)

    if file_.file.size > settings.MAX_UPLOAD_SIZE:
        logger.warning("Too big file.")
        return HttpResponseBadRequest("File can't excede size of {}KB".format(
            settings.MAX_UPLOAD_SIZE / 1024))

    max_image_resolution = settings.MAX_IMAGE_RESOLUTION
    if max(file_.file.width, file_.file.height) > max_image_resolution:
        logger.warning("Too big file.")
        return HttpResponseBadRequest("File can't excede size of {}px".format(
            settings.MAX_IMAGE_RESOLUTION))

    file_.save()

    result = []
    result.append({"name": os.path.basename(file_.file.name),
                   "size": file_.file.size,
                   "url": file_.file.url,
                   "thumbnail": file_.thumbnail.url,  # pylint: disable=no-member
                   "delete_url": '',
                   "delete_type": "POST"})
    response_data = json.dumps(result)
    return HttpResponse(response_data, content_type='application/json')

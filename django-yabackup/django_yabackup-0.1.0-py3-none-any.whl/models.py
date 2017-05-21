# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Backup(models.Model):
    title = models.CharField(blank=True, max_length=128, verbose_name=_('Title'), help_text=_('Just a title'))
    file_name = models.CharField(max_length=64, verbose_name=_('File name'), help_text=_('Date and time will be added to the file name automagically. Example: backup.zip'))
    output_directory = models.CharField(max_length=256, verbose_name=_('Output directory'), help_text=_('Where to store files localy? Example: /home/user/backups/'))
    upload = models.BooleanField(default=False, verbose_name=_('Upload to Yandex.Disk'))
    delete_after_upload = models.BooleanField(default=False, verbose_name=_('Delete after upload'))
    mysqldump = models.BooleanField(default=False, verbose_name=_('MySQL dump'), help_text=_("Create a backup of the projects's database"))
    pub_date = models.DateTimeField(blank=True, auto_now_add=True, verbose_name=_('Published'))
    description = models.TextField(blank=True, verbose_name=_('Description'))

    class Meta:
        verbose_name = _('Backup')
        verbose_name_plural = _('Backups')

    def __str__(self):
        return self.title


class Path(models.Model):
    backup = models.ForeignKey('Backup', related_name='paths', on_delete=models.CASCADE)
    path = models.CharField(max_length=256, verbose_name=_('Path'), help_text=_('Absolute path to file or folder'))

    class Meta:
        verbose_name = _('file or folder')
        verbose_name_plural = _('Files and folders')

    def __str__(self):
        return self.path



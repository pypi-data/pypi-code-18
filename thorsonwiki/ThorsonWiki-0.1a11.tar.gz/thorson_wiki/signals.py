from thorson_wiki.models import Article
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import pre_save, pre_delete, post_save
from django.dispatch import receiver
from django.utils.text import slugify

@receiver(pre_save, sender=Article)
def update_slug(sender, **kwargs):
    """
    Updates an Articles slug when the object is updated. This also results in
    updating the article permissions.
    """

    instance = kwargs['instance']
    try:
        old_instance = Article.objects.get(id=instance.id)
    except Article.DoesNotExist:
        old_instance = None

    instance.slug = slugify(instance.title)

    if old_instance is None:
        return

    if instance.slug != old_instance.slug:
        edit_permission = Permission.objects.get(
            codename='edit-article:%s' % old_instance.slug
        )

        edit_permission.codename='edit-article:%s' % instance.slug
        edit_permission.name="Can edit the article '%s'" % instance.title
        edit_permission.save()

        read_permission = Permission.objects.get(
            codename='read-article:%s' % old_instance.slug
        )

        read_permission.codename='read-article:%s' % instance.slug
        read_permission.name="Can read the article '%s'" % instance.title
        read_permission.save()

@receiver(post_save, sender=Article)
def create_article_permissions(sender, **kwargs):
    """
    Creates individual article permissions when an article is created.
    """

    instance = kwargs['instance']
    created = kwargs['created']

    slug = instance.slug
    title = instance.title

    if created:
        content_type = ContentType.objects.get_for_model(Article)
        permission = Permission.objects.create(
            codename='edit-article:%s' % slug,
            name="Can edit the article '%s'" % title,
            content_type=content_type
        )

        content_type = ContentType.objects.get_for_model(Article)
        permission = Permission.objects.create(
            codename='read-article:%s' % slug,
            name="Can read the article '%s'" % title,
            content_type=content_type
        )

@receiver(pre_delete, sender=Article)
def delete_article_permissions(sender, **kwargs):
    """
    Deletes an article's permissions when the article is deleted.
    """

    instance = kwargs['instance']

    slug = instance.slug

    Permission.objects.get(codename='edit-article:%s' % slug).delete()
    Permission.objects.get(codename='read-article:%s' % slug).delete()

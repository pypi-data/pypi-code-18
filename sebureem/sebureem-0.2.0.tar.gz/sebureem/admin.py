"""Sebureem admin functionality and blueprints

This module holds the functions that runs behind the admin views and CLI.
This functions allow admins to moderate and manage comments, sites and topics.

Warning: Authentication doesn't occurs in this module, it should be handled in
the CLI and the admin webapp.
"""
from sebureem.models import Sebuks, Sebura

def toggle_lock_topic(topic_id, status):
    """Lock or unlock a topic by name or id

    Try to lock (or unlock, depending on the status value) a topic either by
    name or by id. A locked topic doesn't allow further comment to be posted 
    on.
    
    :param str topic_id: The topic name or id
    :param bool status: The new status for the locked property
    :raises Sebuks.DoesNotExist: if the topic cannot be retrieved from db
    """
    try:
        topic_id = int(topic_id)
        topic = Sebuks.get(Sebuks.id == topic_id)
    except ValueError:
        topic = Sebuks.get(Sebuks.name == topic_id)

    topic.locked = status
    topic.save()

def toggle_publish_comments(comments_id, status):
    """Publish or hide a comment or a range of comments

    Try to publish or unpublish a single comment or a group of comments.
     
    :param list comments_id: The list of comment's id
    :param bool status: The new status for the comments list
    """
    comments = Sebura.select().where(Sebura.id << comments_id)
    for comment in comments:
        comment.published = status
        comment.save()

def add_site():
    """Add a new site to the database
    """
    pass

def remove_site():
    """Remove a site either by name or by id
    """
    pass

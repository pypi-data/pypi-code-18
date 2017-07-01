"""
Generic view document chain.
"""

import bson
import flask
import json

from manhattan.chains import Chain, ChainMgr
from mongoframes import ASC

from . import factories

__all__ = ['order_chains']


# Define the chains
order_chains = ChainMgr()

# GET
order_chains['get'] = Chain([
    'authenticate',
    'get_documents',
    'decorate',
    'render_template'
    ])

# POST
order_chains['post'] = Chain([
    'authenticate',
    'get_documents',
    'get_order_ids',
    [
        [
            'set_order',
            'redirect'
        ],
        ['redirect']
    ]
])


# Define the links
order_chains.set_link(factories.authenticate())
order_chains.set_link(factories.decorate('order'))
order_chains.set_link(factories.redirect('list'))
order_chains.set_link(factories.render_template('order'))

@order_chains.link
def get_documents(state):
    """
    Get the documents we want to be ordered.

    This link adds `documents` and `document_ids` to the state.
    """
    state.documents = state.manage_config.frame_cls.many(
        sort=[('position', ASC)]
        )
    state.document_ids = [str(i._id) for i in state.documents]

@order_chains.link
def get_order_ids(state):
    """
    Get the list of identifiers (typically Ids) passed to the view that
    determine the order we'll apply.

    This link adds a `ordered_ids` key to the the state containing the ordered
    list of Ids.
    """

    # Get the ordered Ids from the request
    raw_ordered_ids = flask.request.form.get('ordered_ids', '[]')

    # Parse the raw Ids (which are passed as a JSON list)
    try:
        ordered_ids = json.loads(raw_ordered_ids)
    except ValueError:
        ordered_ids = []

    # Convert the Ids to object Ids
    try:
        ordered_ids = [bson.objectid.ObjectId(id) for id in ordered_ids]
    except bson.errors.InvalidId:
        pass

    # Validate there's more than one document to sort and that there's an
    # ordered Id for each document being ordered.
    set_a = set(ordered_ids)
    set_b = set(i._id for i in state.documents)

    if len(ordered_ids) > 1 and set_a == set_b:
        state.ordered_ids = ordered_ids
        return True

    else:
        flask.flash('Not a valid set of Ids', 'error')
        return False

@order_chains.link
def set_order(state):
    """
    Set a new order for the set of documents given by the ordered set of Ids.
    """

    # Set the position field for each document
    for document in state.documents:
        document.position = state.ordered_ids.index(document._id)

    # Update the documents
    state.manage_config.frame_cls.update_many(state.documents, 'position')

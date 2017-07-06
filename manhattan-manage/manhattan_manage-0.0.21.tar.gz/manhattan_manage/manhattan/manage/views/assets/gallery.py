# - Display a list of asssets stored against a document field in a gallery
# - We can assume than any gallery actions will have an existing document to
#   be saved against.


"""
Generic gallery chain.

: `gallery_field`
    The field against the document that stores the gallery of assets (required).

: `gallery_projection`
    The projection used when requesting the document from the database (defaults
    to None which means the detault projection for the frame class will be
    used).

    NOTE: The `gallery_field` must be one of the project fields otherwise the
    gallery will always appear to be empty.

"""

from manhattan.chains import Chain, ChainMgr

from . import factories

__all__ = ['gallery_chains']


# Super links
super_get_document = factories.get_document('gallery')


# Define the chains
gallery_chains = ChainMgr()

# GET
gallery_chains['get'] = Chain([
    'config',
    'authenticate',
    'get_document',
    'decorate',
    'render_template'
    ])


# Define the links
gallery_chains.set_link(factories.config(gallery_field=None))
gallery_chains.set_link(factories.authenticate())
gallery_chains.set_link(factories.decorate('gallery'))
gallery_chains.set_link(factories.render_template('gallery'))

@gallery_chains.link
def get_document(state):
    super_get_document(state)

    # Ensure the gallery field values are represented as Assets (and not raw
    # dictionaries).
    document = state[state.manage_config.var_name]

    # @@ Do this but also should `order` view/chain return using the plural name
    # for the document class? probably :/
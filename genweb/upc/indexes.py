from five import grok
from plone.indexer import indexer
from plone.app.contenttypes.interfaces import IEvent


@indexer(IEvent)
def ImageFile(context):
    """Create a catalogue indexer, registered as an adapter, which can
    populate the ``context.filename`` value and index it.
    """
    return context.image.filename
grok.global_adapter(ImageFile, name='news_image_filename')

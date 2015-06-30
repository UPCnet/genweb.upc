from plone.resource.traversal import ResourceTraverser


class GenwebUPCTraverser(ResourceTraverser):
    """The bootstrap resources traverser.

    Allows traversal to /++genwebupc++<name> using ``plone.resource`` to fetch
    things stored either on the filesystem or in the ZODB.
    """

    name = 'genwebupc'

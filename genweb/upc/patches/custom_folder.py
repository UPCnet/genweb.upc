def results(self, **kwargs):
    """Return a content listing based result set with contents of the
    folder.

    :param **kwargs: Any keyword argument, which can be used for catalog
                     queries.
    :type  **kwargs: keyword argument

    :returns: plone.app.contentlisting based result set.
    :rtype: ``plone.app.contentlisting.interfaces.IContentListing`` based
            sequence.
    """
    # Extra filter
    kwargs.update(self.request.get('contentFilter', {}))
    kwargs.setdefault('portal_type', self.friendly_types)
    kwargs.setdefault('batch', True)
    kwargs.setdefault('b_size', self.b_size)
    kwargs.setdefault('b_start', self.b_start)
    kwargs.setdefault('orphan', 1)

    results = self.context.restrictedTraverse('@@folderListing')(**kwargs)
    return results

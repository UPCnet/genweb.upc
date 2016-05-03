from plone.app.layout.viewlets.content import DocumentBylineViewlet
from plone import api


class DocumentBylineViewletisReader(DocumentBylineViewlet):

    def isReader(self):
        """Check if user rol is Reader"""
        userid = api.user.get_current().id
        user = api.user.get(username=userid)
        roles = user.getRoles()
        for rol in roles:
            if rol in ['Author', 'Owner', 'Editor', 'Contributor', 'Manager', 'Reviewer', 'Site Administrator', 'WebMaster']:
                return False
            # Reader or Authenticated
            else:
                return True
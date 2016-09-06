from plone.app.layout.viewlets.content import DocumentBylineViewlet
from AccessControl import getSecurityManager


class DocumentBylineViewletisReader(DocumentBylineViewlet):

    def isReader(self):
        """Check if user rol is Reader"""
        secman = getSecurityManager()
        user = secman.getUser()
        context = self.context
        roles = user.getRolesInContext(context)
        if 'Author' in roles or 'Owner' in roles or 'Editor' in roles or 'Contributor' in roles or 'Manager' in roles or 'Reviewer' in roles or 'Site Administrator' in roles or 'WebMaster' in roles:
            return False
        # Reader or Authenticated or Member
        else:
            return True

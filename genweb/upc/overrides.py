from plone.app.layout.viewlets.content import DocumentBylineViewlet
from plone import api
from Acquisition import aq_inner, aq_chain


class DocumentBylineViewletisReader(DocumentBylineViewlet):

    def isReader(self):
        """Check if user rol is Reader"""
        userid = api.user.get_current().id
        context = aq_inner(self.context)
        for obj in aq_chain(context):
            local_roles = obj.get_local_roles()
            user_roles = [x for x in local_roles if x[0] == userid]
            if user_roles:
                roles = user_roles[0][1]
                for rol in roles:
                    if 'Editor' in rol or 'Contributor' in rol or 'Reviewer' in rol:
                        return False
                    else:
                        return True
        return False

from plone.app.layout.viewlets.content import DocumentBylineViewlet
from plone import api
from Acquisition import aq_inner, aq_chain


class DocumentBylineViewletisReader(DocumentBylineViewlet):

    def isReader(self):
        """Check if user rol is Reader"""
        userid = api.user.get_current().id
        inner_context = aq_inner(self.context)
        context = aq_chain(inner_context)
        for obj in context[:-1]:
            local_roles = obj.get_local_roles()
            user_roles = [x for x in local_roles if x[0] == userid]
            if user_roles:
                roles = user_roles[0][1]
                for rol in roles:
                    if 'Owner' in rol or 'Editor' in rol or 'Contributor' in rol or 'Reviewer' in rol:
                        return False
                    else:
                        return True
        return False

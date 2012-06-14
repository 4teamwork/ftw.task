from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView


def getUserInfos(context, userid):
    """ return a dict with userinformations, about the user """
    mt = getToolByName(context, 'portal_membership')
    user = mt.getMemberById(userid)

    if user:
        fullname = user.getProperty('fullname', '')
        if not fullname:
            fullname = userid
        return {
            'name': fullname,
            'url': '%s/author/%s' % (
                context.portal_url(),
                user.id)}

    else:
        catalog = getToolByName(context, 'portal_catalog')
        brains = catalog(dict(UID=userid))
        if len(brains):
            brain = brains[0]
            return {'name': brain.Title, 'url': brain.getPath()}
        return {'name': userid, 'url': ''}


class TaskView(BrowserView):
    """ The View, wich schow all infos about the Task """

    def getResponsibilityInfos(self, userids):
        context = self.context
        result = []
        if not userids:
            return
        elif isinstance(userids, list) or isinstance(userids, tuple):
            for userid in userids:
                result.append(getUserInfos(context, userid))
        else:
            result.append(getUserInfos(context, userids))
        return result

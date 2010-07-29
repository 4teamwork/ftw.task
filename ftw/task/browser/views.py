from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView


def getUserInfos(context, userid):
    mt = getToolByName(context, 'portal_membership')
    user = mt.getMemberById(userid)

    if user:
        return {'name': user.getProperty('fullname', ''),
                'url': '%s/author/%s' % (context.portal_url(), user.id), }
    else:
        return {'name': userid, 'url': ''}


class TaskView(BrowserView):

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

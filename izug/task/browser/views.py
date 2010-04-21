from izug.utils.users import getResponsibilityInfosFor

from Products.Five.browser import BrowserView


class TaskView(BrowserView):

    def getResponsibilityInfos(self, userids):
        context = self.context
        result = []
        if not userids:
            return
        elif isinstance(userids, list) or isinstance(userids, tuple):
            for userid in userids:
                result.append(getResponsibilityInfosFor(context, userid))
        else:
            result.append(getResponsibilityInfosFor(context, userids))
        return result

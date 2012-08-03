from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from ftw.task import taskMessageFactory as _
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from zope.component import getMultiAdapter
from zope.interface import implements


class IMyTasksPortlet(IPortletDataProvider):
    """A portlet that displays the user's tasks
    """


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IMyTasksPortlet)

    def __init__(self):
        pass

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return _(u"label_mytasks_portlet", default=u"My Tasks Portlet")


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    render = ViewPageTemplateFile('mytasks.pt')

    def __init__(self, context, request, view, manager, data):
        base.Renderer.__init__(self, context, request, view, manager, data)

        portal_state = getMultiAdapter((self.context, self.request),
                                       name=u'plone_portal_state')
        self.navroot_url = portal_state.navigation_root_url()

    @property
    def available(self):
        return True

    @property
    def items(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        mt = getToolByName(self.context, 'portal_membership')
        member = mt.getAuthenticatedMember()
        username = member.getUserId()
        tasks = catalog(portal_type="Task", getResponsibility=username)
        return tasks


class AddForm(base.NullAddForm):
    label = _(u"label_add_mytasks_portlet",
              default=u"Add My Tasks Portlet")
    description = _(u"help_add_mytasks_portlet",
                    default=u"This portlet displays the user's tasks.")

    def create(self):
        return Assignment()

from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from ftw.pdfgenerator.interfaces import ILaTeXLayout
from ftw.task import _
from ftw.workspace.interfaces import IWorkspace
from ftw.workspace.interfaces import IWorkspaceDetailsListingProvider
from zope.component import adapts
from zope.i18n import translate
from zope.interface import Interface
from zope.interface import implements


class TasksListing(object):
    implements(IWorkspaceDetailsListingProvider)
    adapts(IWorkspace, Interface, ILaTeXLayout, Interface)

    template = ViewPageTemplateFile('templates/tasks_listing.pt')

    def __init__(self, context, request, layout, view):
        self.context = context
        self.request = request
        self.layout = layout
        self.view = view

    def get_sort_key(self):
        return 30

    def get_title(self):
        return translate(_(u'latex_label_events', u'Tasks'),
                         context=self.request)

    def get_listing(self):
        return self.view.convert(self.template())

    def get_items(self):
        acl_users = getToolByName(self.context, 'acl_users')
        translation = getToolByName(self.context, 'translation_service')
        localize_time = translation.ulocalized_time

        for brain in self._brains():
            obj = brain.getObject()
            responsibility = []
            for userid in obj.getResponsibility():
                user = acl_users.getUserById(userid)
                responsibility.append(
                    user and user.getProperty('fullname', userid) or userid)

            yield {
                'title': brain.Title,
                'state': brain.review_state,
                'end': localize_time(brain.end),
                'responsibility': ', '.join(responsibility)}

    def _brains(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        query = {'path': '/'.join(self.context.getPhysicalPath()),
                 'portal_type': ['Task'],
                 'sort_on': 'end',
                 'sort_order': 'reverse'}

        return catalog(query)

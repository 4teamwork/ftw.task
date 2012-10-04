"""Definition of the Task content type
"""

from DateTime import DateTime
from Products.ATContentTypes.content import document
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATReferenceBrowserWidget import ATReferenceBrowserWidget
from Products.Archetypes import atapi
from Products.CMFCore.utils import getToolByName
from ftw.task import taskMessageFactory as _
from ftw.task.config import PROJECTNAME
from ftw.task.interfaces import ITask
from zope.interface import implements
from ftw.calendarwidget.browser.widgets import FtwCalendarWidget


TaskSchema = document.ATDocumentSchema.copy() + \
    atapi.Schema((

        atapi.TextField(
            name='text',
            searchable=True,
            required=False,
            default_content_type='text/html',
            default_output_type='text/html',
            storage=atapi.AnnotationStorage(),

            widget=atapi.RichWidget(
                label=_(u'task_label_text', default=u'Text'),
                description=_(u'task_help_text', default=u''))),

        atapi.DateTimeField(
            name='start_date',
            required=True,
            searchable=True,
            accessor='start',
            default_method='default_start_date',

            widget=FtwCalendarWidget(
                label=_(u'task_label_start_date', default=u'Start of Task'),
                description=_(u'task_help_start_date',
                              default=u'Enter the starting date and time, '
                              'or click the calendar icon and select it.'),
                visible={'edit': 'invisible', 'view': 'invisible'})),

        atapi.DateTimeField(
            name='end_date',
            required=True,
            searchable=True,
            accessor='end',
            default_method='default_end_date',

            widget=FtwCalendarWidget(
                label=_(u'task_label_end_date', default=u'End of Task'),
                description=_(u'task_help_end_date',
                              default=u'Enter the ending date and time, '
                              'or click the calendar icon and select it.'))),

        atapi.LinesField(
            name='responsibility',
            required=False,
            searchable=True,
            vocabulary_factory='ftw.task.users',

            widget=atapi.MultiSelectionWidget(
                size=4,
                format='checkbox',
                label=_(u'task_label_responsibility',
                        default=u'Responsibility'),
                description=_(u'task_help_responsibility',
                              default=u'Select the responsible person(s).'))),

        atapi.ReferenceField(
            name='related_items',
            relationship='relatesTo',
            multiValued=True,
            isMetadata=True,
            languageIndependent=False,
            index='KeywordIndex',
            schemata='default',

            widget=ATReferenceBrowserWidget.ReferenceBrowserWidget(
                allow_search=True,
                allow_browse=True,
                show_indexes=False,
                force_close_on_insert=True,
                label=_(u'task_label_related_items', default=u'Related Items'),
                description=_(u'task_help_related_items', default=u''),
                visible={'edit': 'visible', 'view': 'invisible'})),

        ))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

TaskSchema = finalizeATCTSchema(TaskSchema,
                                folderish=True,
                                moveDiscussion=False)

hide_fields = ['description',
               'effectiveDate',
               'expirationDate',
               'subject',
               'location',
               'language',
               'creators',
               'contributors',
               'rights',
               'presentation',
               'tableContents',
               'allowDiscussion',
               'excludeFromNav',
               ]


for item in hide_fields:
    TaskSchema.changeSchemataForField(item, 'default')
    TaskSchema[item].widget.visible = -1


class Task(document.ATDocument):
    """A type for tasks"""
    implements(ITask)

    portal_type = 'Task'
    schema = TaskSchema

    text = atapi.ATFieldProperty('text')

    def setResponsibility(self, value, **kwargs):
        """ set Owner role for the responsibility User"""
        me = self.portal_membership.getAuthenticatedMember().getId()
        for m in self.getResponsibility():
            if me != m:
                self.portal_membership.deleteLocalRoles(
                    obj=self, member_ids=[m])

        for m in value:
            self.portal_membership.setLocalRoles(obj=self,
                                                 member_ids=[m],
                                                 member_role='Owner')

        self.getField('responsibility').set(self, value, **kwargs)

    def default_start_date(self):
        """ Return a Standard Startday (9.00 Clock today) """

        a = DateTime()
        return DateTime(a.year(), a.month(), a.day(), 9, 00)

    def default_end_date(self):
        """ Return a Standard Startday (17.00 Clock today) """

        a = DateTime()
        return DateTime(a.year(), a.month(), a.day(), 17, 00)

    def get_fullname(self, userid):
        """return the fulname of the  """

        pas_tool = getToolByName(self, 'acl_users')
        user = pas_tool.getUserById(userid)
        if user:
            return user.getProperty('fullname', userid)
        return userid

    def canSetDefaultPage(self):
        return False

atapi.registerType(Task, PROJECTNAME)

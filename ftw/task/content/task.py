"""Definition of the Task content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import document
from Products.ATContentTypes.content.schemata import finalizeATCTSchema

from Products.CMFCore.utils import getToolByName

from Products.ATReferenceBrowserWidget import ATReferenceBrowserWidget
from DateTime import DateTime

from ftw.task import taskMessageFactory as _
from ftw.task.interfaces import ITask
from ftw.task.config import PROJECTNAME

TaskSchema = document.ATDocumentSchema.copy() + atapi.Schema((

    atapi.TextField('text',
        searchable = True,
        required = True,
        default_content_type = 'text/html',
        default_output_type = 'text/html',
        storage = atapi.AnnotationStorage(),
        widget = atapi.RichWidget(
            label = _(u"task_label_text", default=u"Text"),
            description = _(u"task_help_text", default=u""),
            ),
        ),

    atapi.DateTimeField('start_date',
        required = True,
        searchable = True,
        accessor='start',
        default_method = 'default_start_date',
        storage = atapi.AnnotationStorage(),
        widget = atapi.CalendarWidget(
            label = _(u"task_label_start_date", default=u"Start of Task"),
            description = _(u"task_help_start_date",
                default=u"Enter the starting date and time,\
                          or click the calendar icon and select it."),
            visible = {'edit': 'invisible', 'view': 'invisible'},
            ),
    ),

    atapi.DateTimeField('end_date',
        required = True,
        searchable = True,
        accessor='end',
        default_method = 'default_end_date',
        storage = atapi.AnnotationStorage(),
        widget = atapi.CalendarWidget(
            label = _(u"task_label_end_date", default=u"End of Task"),
            description = _(u"task_help_end_date",
                default=u"Enter the ending date and time, \
                          or click the calendar icon and select it."),
            ),
        ),

    atapi.LinesField('responsibility',
        required = False,
        searchable = True,
        index = 'KeywordIndex:schema',
        vocabulary_factory="ftw.task.users",
        storage = atapi.AnnotationStorage(),
        widget = atapi.MultiSelectionWidget(size = 4,
            label = _(u"task_label_responsibility",
                     default=u"Responsibility"),
            description = _(u"task_help_responsibility",
                           default=u"Select the responsible person(s)."),
            format='checkbox',
        ),
    ),
    atapi.ReferenceField('related_items',
        relationship = 'relatesTo',
        multiValued = True,
        isMetadata = True,
        languageIndependent = False,
        index = 'KeywordIndex',
        storage = atapi.AnnotationStorage(),
        schemata = 'default',
        widget = ATReferenceBrowserWidget.ReferenceBrowserWidget(
            allow_search = True,
            allow_browse = True,
            show_indexes = False,
            force_close_on_insert = True,
            label = _(u"task_label_related_items", default=u"Related Items"),
            description = _(u"task_help_related_items", default=u""),
            visible = {'edit': 'visible', 'view': 'invisible'}
            ),
        ),
))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

TaskSchema = finalizeATCTSchema(TaskSchema,
                        folderish=True,
                        moveDiscussion=False)

TaskSchema['title'].storage = atapi.AnnotationStorage()
TaskSchema['description'].storage = atapi.AnnotationStorage()
TaskSchema['description'].widget.visible = {'view': 'invisible',
                                            'edit': 'invisible'}

TaskSchema.changeSchemataForField('effectiveDate', 'settings')
TaskSchema.changeSchemataForField('expirationDate', 'settings')
TaskSchema['effectiveDate'].widget.visible = {'view': 'invisible',
                                              'edit': 'invisible'}
TaskSchema['expirationDate'].widget.visible = {'view': 'invisible',
                                               'edit': 'invisible'}

#finalize the schema
TaskSchema.changeSchemataForField('subject', 'settings')
TaskSchema.changeSchemataForField('location', 'settings')
TaskSchema['location'].widget.visible = -1
TaskSchema.changeSchemataForField('language', 'settings')
TaskSchema['language'].widget.visible = -1
TaskSchema.changeSchemataForField('creators', 'settings')
TaskSchema['creators'].widget.visible = -1
TaskSchema.changeSchemataForField('contributors', 'settings')
TaskSchema['contributors'].widget.visible = -1
TaskSchema.changeSchemataForField('rights', 'settings')
TaskSchema['rights'].widget.visible = -1


class Task(document.ATDocument):
    """A type for tasks"""
    implements(ITask)

    portal_type = "Task"
    schema = TaskSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    text = atapi.ATFieldProperty('text')
    start_date = atapi.ATFieldProperty('start_date')
    end_date = atapi.ATFieldProperty('end_date')
    responsible = atapi.ATFieldProperty('responsibility')

    def setResponsibility(self, value, **kwargs):
        """ set Owner role for the responsibility User"""
        me = self.portal_membership.getAuthenticatedMember().getId()
        for m in self.getResponsibility():
            if me != m:
                self.portal_membership.deleteLocalRoles(obj = self, member_ids=[m, ])

        for m in value:
            self.portal_membership.setLocalRoles(obj=self,
                member_ids=[m, ], member_role='Owner')

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

atapi.registerType(Task, PROJECTNAME)

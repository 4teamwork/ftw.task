"""Definition of the Task content type
"""

from zope.interface import implements, directlyProvides
from Acquisition import aq_inner, aq_parent

from Products.Archetypes import atapi
from Products.ATContentTypes.content import document
from Products.ATContentTypes.content import schemata

from Products.CMFCore.utils import getToolByName

from Products.AddRemoveWidget import AddRemoveWidget
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from DateTime import DateTime

from izug.arbeitsraum.content.utilities import finalizeIzugSchema

from izug.task import taskMessageFactory as _
from izug.task.interfaces import ITask
from izug.task.config import PROJECTNAME

from izug.utils.users import getAssignableUsers

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
                        widget = atapi.CalendarWidget(label = _(u"task_label_start_date", default=u"Start of Meeting"),
                                                      description = _(u"task_help_start_date", default=u"Enter the starting date and time, or click the calendar icon and select it."),
                                                      ),
                        ),

    atapi.DateTimeField('end_date',
                        required = True,
                        searchable = True,
                        accessor='end',
                        default_method = 'default_end_date',
                        storage = atapi.AnnotationStorage(),
                        widget = atapi.CalendarWidget(label = _(u"task_label_end_date", default=u"End of Meeting"),
                                                      description = _(u"task_help_end_date", default=u"Enter the ending date and time, or click the calendar icon and select it."),
                                                      ),
                        ),

     atapi.LinesField('responsibility',
                      required = False,
                      searchable = True,
                      index = 'KeywordIndex:schema',               
                      vocabulary = 'getAssignableUsers',
                      storage = atapi.AnnotationStorage(),
                      widget = atapi.MultiSelectionWidget(size = 4,
                                                          label = _(u"task_label_responsibility", default=u"Responsibility"),
                                                          description = _(u"task_help_responsibility", default=u"Select the responsible person(s)."),
                                                          format='checkbox',
                                                          ),
                      ),
    atapi.ReferenceField('related_items',
                         relationship = 'relatesTo',
                         multiValued = True,
                         isMetadata = True,
                         languageIndependent = False,
                         index = 'KeywordIndex',
                         accessor = 'relatedItems',
                         storage = atapi.AnnotationStorage(),
                         schemata = 'default',
                         widget = ReferenceBrowserWidget(
                                                         allow_search = True,
                                                         allow_browse = True,
                                                         show_indexes = False,
                                                         force_close_on_insert = True,
                                                         label = _(u"task_label_related_items", default=u"Related Items"),
                                                         description = _(u"task_help_related_items", default=u""),
                                                         visible = {'edit' : 'visible', 'view' : 'invisible' }
                                                         ),
                         ),

))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

TaskSchema['title'].storage = atapi.AnnotationStorage()
TaskSchema['description'].storage = atapi.AnnotationStorage()
TaskSchema['description'].widget.visible = {'view' : 'invisible', 'edit' : 'invisible'}

finalizeIzugSchema(TaskSchema, folderish=True, moveDiscussion=False)

TaskSchema.changeSchemataForField('effectiveDate','settings')
TaskSchema.changeSchemataForField('expirationDate','settings')
TaskSchema['effectiveDate'].widget.visible = {'view' : 'invisible', 'edit' : 'invisible'}
TaskSchema['expirationDate'].widget.visible = {'view' : 'invisible', 'edit' : 'invisible'}

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

    def getAssignableUsers(self):
        return getAssignableUsers(self,'Contributor')

    def setResponsibility(self, value, **kwargs):
        me = self.portal_membership.getAuthenticatedMember().getId()
        for m in self.getResponsibility():
          if me != m:
            self.portal_membership.deleteLocalRoles(obj = self, member_ids=[m,])

        for m in value:
            self.portal_membership.setLocalRoles( obj=self, member_ids=[m,], member_role='Owner')

        self.getField('responsibility').set(self,value,**kwargs)  

    
    def InfosForArchiv(self):
        return DateTime(self.CreationDate()).strftime('%m/01/%Y')

    def default_start_date(self):
        a = DateTime()
        return DateTime(a.year(), a.month(), a.day(), 9, 00 )

    def default_end_date(self):
        a = DateTime()
        return DateTime(a.year(), a.month(), a.day(), 17, 00 )

atapi.registerType(Task, PROJECTNAME)

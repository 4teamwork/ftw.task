"""Definition of the Task content type
"""

from zope.interface import implements, directlyProvides
from Acquisition import aq_inner, aq_parent

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from Products.CMFCore.utils import getToolByName

from Products.AddRemoveWidget import AddRemoveWidget
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from DateTime import DateTime

from izug.arbeitsraum.content.utilities import finalizeIzugSchema

from izug.task import taskMessageFactory as _
from izug.task.interfaces import ITask
from izug.task.config import PROJECTNAME

TaskSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    atapi.TextField('text',
                    searchable = True,
                    required = True,
                    default_content_type = 'text/html',              
                    default_output_type = 'text/html',
                    allowable_content_types = ('text/html','text/structured','text/plain'),
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
                        default_method = DateTime,
                        storage = atapi.AnnotationStorage(),
                        widget = atapi.CalendarWidget(label = _(u"task_label_start_date", default=u"Start of Meeting"),
                                                      description = _(u"task_help_start_date", default=u"Enter the starting date and time, or click the calendar icon and select it."),
                                                      ),
                        ),

    atapi.DateTimeField('end_date',
                        required = True,
                        searchable = True,
                        accessor='end',
                        default_method = DateTime,
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
                                                          label = _(u"ftw_task_label_responsibility", default=u"Responsibility"),
                                                          description = _(u"task_help_responsibility", default=u"Select the responsible person(s)."),
                                                          format='checkbox',
                                                          ),
                      ),

))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

TaskSchema['title'].storage = atapi.AnnotationStorage()
TaskSchema['description'].storage = atapi.AnnotationStorage()
TaskSchema['description'].widget.visible = {'view' : 'invisible', 'edit' : 'invisible'}

finalizeIzugSchema(TaskSchema, folderish=True, moveDiscussion=False)

class Task(folder.ATFolder):
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
        """Collect users with a given role and return them in a list.
        """
        role = 'Contributor'
        results = []
        pas_tool = getToolByName(self, 'acl_users')
        utils_tool = getToolByName(self, 'plone_utils')

        for user_id_and_roles in utils_tool.getInheritedLocalRoles(self):
            user_id = user_id_and_roles[0]
            # Make sure groups don't get included
            if not pas_tool.getGroupById(user_id):
                if role in user_id_and_roles[1]:
                    user = pas_tool.getUserById(user_id)
                    if user:
                        results.append((user.getId(), '%s (%s)' % (user.getProperty('fullname', ''), user.getId())))
                
        return (atapi.DisplayList(results))
    
    def InfosForArchiv(self):
        return DateTime(self.CreationDate()).strftime('%m/01/%Y')

atapi.registerType(Task, PROJECTNAME)

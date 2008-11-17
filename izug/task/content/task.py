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

from izug.task import taskMessageFactory as _
from izug.task.interfaces import ITask
from izug.task.config import PROJECTNAME

TaskSchema = folder.ATFolderSchema.copy() + atapi.Schema((

        atapi.TextField('text',
                        searchable = True,
                        required = False,
                        primary = False,
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
                            required = False,
                            searchable = True,
                            accessor='start',
                            default_method = DateTime,
                            storage = atapi.AnnotationStorage(),
                            widget = atapi.CalendarWidget(label = _(u"task_label_start_date", default=u"Start of Meeting"),
                                                          description = _(u"task_help_start_date", default=u"Enter the starting date and time, or click the calendar icon and select it."),
                                                          ),
                            ),
    
        atapi.DateTimeField('end_date',
                            required = False,
                            searchable = True,
                            accessor='end',
                            default_method = DateTime,
                            storage = atapi.AnnotationStorage(),
                            widget = atapi.CalendarWidget(label = _(u"task_label_end_date", default=u"End of Meeting"),
                                                          description = _(u"task_help_end_date", default=u"Enter the ending date and time, or click the calendar icon and select it."),
                                                          ),
                            ),

         atapi.LinesField('responsible',
                          required = False,
                          searchable = True,
                          index = 'KeywordIndex:schema',               
                          vocabulary = 'getAssignableUsers',
                          storage = atapi.AnnotationStorage(),
                          widget = atapi.MultiSelectionWidget(size = 4,
                                                              label = _(u"ftw_task_label_responsible", default=u"Responsible"),
                                                              description = _(u"task_help_responsible", default=u"Select the responsible person(s)."),
                                                              format='checkbox',
                                                              ),
                          ),
                          
         atapi.ReferenceField('categories',
                              required = False,
                              storage = atapi.AnnotationStorage(),
                              widget=ReferenceBrowserWidget(
                                                            label=_(u"task_label_categories", default=u"Categories"),
                                                            description=_(u"task_help_categories", default=u"Pick the categories of this item."),
                                                            allow_browse=False,
                                                            show_results_without_query=True,
                                                            restrict_browsing_to_startup_directory=True,
                                                            base_query={"portal_type": "Blog Catgory", "sort_on": "sortable_title"},
                                                            macro='category_reference_widget',
                                                            ),
                              allowed_types=('ClassificationItem',),
                              multiValued=1,
                              schemata='default',
                              relationship='blog_categories'
                              ),
    
         atapi.LinesField('tags',
                          multiValued=1,
                          storage = atapi.AnnotationStorage(),
                          vocabulary='getAllTags',
                          schemata='default',
                          widget=AddRemoveWidget(
                                                 label=_(u"task_label_tags", default=u"Tags"),
                                                 description=_(u"task_help_tags", default=u"Pick the tags of this item."),
                                                 ),
                          ),
))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

TaskSchema['title'].storage = atapi.AnnotationStorage()
TaskSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(TaskSchema, folderish=True, moveDiscussion=False)

class Task(folder.ATFolder):
    """A type for tasks"""
    implements(ITask)

    portal_type = "Task"
    schema = TaskSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    text = atapi.ATFieldProperty('text')
    categories = atapi.ATFieldProperty('categories')
    tags = atapi.ATFieldProperty('tags')

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
                    results.append((user.getId(), '%s (%s)' % (user.getProperty('fullname', ''), user.getId())))
                
        return (atapi.DisplayList(results))
        
    #returns the category uid and the parent category uid
    def getCategoryUids(self):
        cats = aq_inner(self).getCategories()
        uids = [c.UID() for c in cats]
        parent_uids = []
        for pc in cats:
            parent = aq_inner(pc).aq_parent
            puid = parent.UID()
            grand_parent = aq_inner(parent).aq_parent
            if puid not in parent_uids and grand_parent.Type()=='Blog Category':
                parent_uids.append(puid)
                DateTime(self.CreationDate()).strftime('%m/%Y')
        return parent_uids + uids
    
    def getAllTags(self):
        catalog = getToolByName(self, "portal_catalog")
        items = atapi.DisplayList(())
        for i in catalog.uniqueValuesFor("getTags"):
            if i and type(i)==type(''):
                items.add(i,i)
        return items

    def InfosForArchiv(self):
        return DateTime(self.CreationDate()).strftime('%m/01/%Y')

atapi.registerType(Task, PROJECTNAME)

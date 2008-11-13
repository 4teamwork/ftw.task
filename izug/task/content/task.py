"""Definition of the Task content type
"""

from zope.interface import implements, directlyProvides
from Acquisition import aq_inner, aq_parent

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from Products.CMFCore.utils import getToolByName

from Products.AddRemoveWidget import AddRemoveWidget
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from DateTime import DateTime

from izug.task import taskMessageFactory as _
from izug.task.interfaces import ITask
from izug.task.config import PROJECTNAME

TaskSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

        atapi.TextField('text',
                        searchable = True,
                        required = False,
                        primary = False,
                        default_content_type = 'text/html',              
                        default_output_type = 'text/html',
                        allowable_content_types = ('text/html','text/structured','text/plain'),
                        storage = atapi.AnnotationStorage(),
                        widget = atapi.RichWidget(
                                                  label = _(u"file_label_text", default=u"Text"),
                                                  description = _(u"file_help_text", default=u""),
                                                  ),
                        ),

        atapi.ReferenceField('categories',
                             required = False,
                             storage = atapi.AnnotationStorage(),
                             widget=ReferenceBrowserWidget(
                                                           label=_('Categories'),
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
                                                label=_('Tags'),
                                                ),
                         ),
))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

TaskSchema['title'].storage = atapi.AnnotationStorage()
TaskSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(TaskSchema, moveDiscussion=False)

class Task(base.ATCTContent):
    """A type for tasks"""
    implements(ITask)

    portal_type = "Task"
    schema = TaskSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    text = atapi.ATFieldProperty('text')
    categories = atapi.ATFieldProperty('categories')
    tags = atapi.ATFieldProperty('tags')

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
    
atapi.registerType(Task, PROJECTNAME)

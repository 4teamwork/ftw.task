"""Definition of the Task content type
"""

from zope.interface import implements, directlyProvides

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from izug.task import taskMessageFactory as _
from izug.task.interfaces import ITask
from izug.task.config import PROJECTNAME

TaskSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

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

atapi.registerType(Task, PROJECTNAME)

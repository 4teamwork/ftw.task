from zope import schema
from zope.interface import Interface

from zope.app.container.constraints import contains
from zope.app.container.constraints import containers

from ftw.task import taskMessageFactory as _

# -*- extra stuff goes here -*-

class ITask(Interface):
    """A type for tasks"""

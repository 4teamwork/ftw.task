from ftw.builder import builder_registry
from ftw.builder.archetypes import ArchetypesBuilder


class TaskBuilder(ArchetypesBuilder):
    portal_type = 'Task'


builder_registry.register('task', TaskBuilder)

from ftw.task.testing import ZCML_LAYER
from ftw.testing import MockTestCase
from plone.principalsource.source import PrincipalSource
from zope.component import getUtility
from zope.component import provideUtility
from zope.component import queryUtility
from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory


class AssignableUsersVocabularyFactory(object):
    implements(IVocabularyFactory)

    def __call__(self, context):
        return 'assignable users test vocabulary'


class TestAvailableUsersVocabulary(MockTestCase):

    layer = ZCML_LAYER

    def test_component_is_registered(self):
        factory = queryUtility(IVocabularyFactory, name='ftw.task.users')
        self.assertNotEqual(factory, None)
        self.assertTrue(IVocabularyFactory.providedBy(factory))

    def test_delegates_to_principalsource_users_by_default(self):
        factory = getUtility(IVocabularyFactory, name='ftw.task.users')

        context = object()
        source = factory(context)
        self.assertTrue(isinstance(source, PrincipalSource))

    def test_prefers_assignable_users_vocabulary(self):
        provideUtility(component=AssignableUsersVocabularyFactory(),
                       name='assignable_users')

        factory = getUtility(IVocabularyFactory, name='ftw.task.users')

        context = object()
        source = factory(context)
        self.assertEqual(source, 'assignable users test vocabulary')

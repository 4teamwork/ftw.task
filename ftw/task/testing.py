from ftw.builder.testing import BUILDER_LAYER
from ftw.builder.testing import functional_session_factory
from ftw.builder.testing import set_builder_session_factory
from ftw.testing.layer import ComponentRegistryLayer
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles, TEST_USER_ID, TEST_USER_NAME, login
from plone.testing import z2
from zope.configuration import xmlconfig
import ftw.task.tests.builders


class ZCMLLayer(ComponentRegistryLayer):

    def setUp(self):
        super(ZCMLLayer, self).setUp()
        import ftw.task.tests
        self.load_zcml_file('test.zcml', ftw.task.tests)


ZCML_LAYER = ZCMLLayer()


class FtwTaskLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, BUILDER_LAYER)

    def setUpZope(self, app, configurationContext):
        import plone.principalsource
        xmlconfig.file('configure.zcml', plone.principalsource,
                       context=configurationContext)

        import ftw.calendarwidget
        xmlconfig.file('configure.zcml', ftw.calendarwidget,
                       context=configurationContext)

        import ftw.task
        xmlconfig.file('configure.zcml', ftw.task,
                       context=configurationContext)

        import ftw.tabbedview
        xmlconfig.file('configure.zcml', ftw.tabbedview,
                       context=configurationContext)

        z2.installProduct(app, 'ftw.task')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'ftw.task:default')
        applyProfile(portal, 'ftw.tabbedview:default')

        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)


FTW_TASK_FIXTURE = FtwTaskLayer()
FTW_TASK_INTEGRATION_TESTING = IntegrationTesting(
    bases=(FTW_TASK_FIXTURE,), name="FtwTask:Integration")
FTW_TASK_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FTW_TASK_FIXTURE,
           set_builder_session_factory(functional_session_factory)),
    name='FtwTask:Functional')

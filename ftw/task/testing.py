from ftw.testing.layer import ComponentRegistryLayer
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import setRoles, TEST_USER_ID, TEST_USER_NAME, login
from plone.testing import z2
from zope.configuration import xmlconfig


class LatexZCMLLayer(ComponentRegistryLayer):

    def setUp(self):
        super(LatexZCMLLayer, self).setUp()
        import ftw.task.tests

        self.load_zcml_file('latex_test.zcml', ftw.task.tests)


LATEX_ZCML_LAYER = LatexZCMLLayer()


class ZCMLLayer(ComponentRegistryLayer):

    def setUp(self):
        super(ZCMLLayer, self).setUp()
        import ftw.task.tests
        self.load_zcml_file('test.zcml', ftw.task.tests)


ZCML_LAYER = ZCMLLayer()


class FtwTaskLayer(PloneSandboxLayer):

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

        z2.installProduct(app, 'ftw.task')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'ftw.task:default')

        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)


FTW_TASK_FIXTURE = FtwTaskLayer()
FTW_TASK_INTEGRATION_TESTING = IntegrationTesting(
    bases=(FTW_TASK_FIXTURE,), name="FtwTask:Integration")
FTW_TASK_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FTW_TASK_FIXTURE,), name='FtwTask:Functional')

from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from ftw.task.testing import FTW_TASK_FUNCTIONAL_TESTING
from plone.testing.z2 import Browser
from unittest2 import TestCase
import transaction


class TestTaskView(TestCase):

    layer = FTW_TASK_FUNCTIONAL_TESTING

    def setUp(self):
        super(TestTaskView, self).setUp()

        portal = self.layer['portal']
        self.task = portal.get(portal.invokeFactory('Task', 'test-task'))

        transaction.commit()

        self.browser = Browser(self.layer['app'])
        self.browser.handleErrors = False
        self.url = self.task.restrictedTraverse(
            '@@plone_context_state').view_url()

    def tearDown(self):
        super(TestTaskView, self).tearDown()

        portal = self.layer['portal']
        portal.manage_delObjects(['test-task'])

        transaction.commit()

    def test_state_is_not_in_template_when_no_workflow_is_configured(self):
        self.browser.open(self.url)
        self.assertEqual(self.browser.url, self.url)
        self.assertNotIn('State', self.browser.contents)

    def test_state_is_in_template_when_workflow_defined(self):
        wftool = getToolByName(self.task, 'portal_workflow')
        wftool.setChainForPortalTypes((self.task.portal_type,),
                                      ('one_state_workflow',))
        transaction.commit()

        self.browser.open(self.url)
        self.assertEqual(self.browser.url, self.url)
        self.assertIn('State', self.browser.contents)

    def test_text_is_in_view(self):
        self.task.setText('Hello <b>World</b>', mimetype='text/html')
        transaction.commit()

        self.browser.open(self.url)
        self.assertEqual(self.browser.url, self.url)
        self.assertIn('Hello <b>World</b>', self.browser.contents)

    def test_end_date_is_in_view(self):
        self.task.setEnd_date(DateTime('2010/05/05'))
        transaction.commit()

        self.browser.open(self.url)
        self.assertEqual(self.browser.url, self.url)
        self.assertIn('May 05, 2010', self.browser.contents)

    def test_responsibility_is_in_view(self):
        mtool = getToolByName(self.task, 'portal_membership')
        mtool.addMember('john.doe', '', ['Reader'], None, properties={
                'fullname': 'John Doe'})
        mtool.addMember('jane.doe', '', ['Reader'], None, properties={
                'fullname': 'Jane Doe'})
        mtool.addMember('hugo.boss', '', ['Reader'], None, properties={
                'fullname': 'Hugo Boss'})

        self.task.setResponsibility(['john.doe', 'hugo.boss'])
        transaction.commit()

        self.browser.open(self.url)
        self.assertEqual(self.browser.url, self.url)
        self.assertIn('John Doe', self.browser.contents)
        self.assertNotIn('Jane Doe', self.browser.contents)
        self.assertIn('Hugo Boss', self.browser.contents)

    def test_responsibility_with_single_responsible(self):
        mtool = getToolByName(self.task, 'portal_membership')
        mtool.addMember('john.doe', '', ['Reader'], None, properties={
                'fullname': 'John Doe'})

        self.task.setResponsibility('john.doe')
        transaction.commit()

        self.browser.open(self.url)
        self.assertEqual(self.browser.url, self.url)
        self.assertIn('John Doe', self.browser.contents)

    def test_responsibility_with_user_without_fullname(self):
        mtool = getToolByName(self.task, 'portal_membership')
        mtool.addMember('john.doe', '', ['Reader'], None)

        self.task.setResponsibility('john.doe')
        transaction.commit()

        self.browser.open(self.url)
        self.assertEqual(self.browser.url, self.url)
        self.assertIn('john.doe', self.browser.contents)

        # "validate" test setup: John Doe should not have a fullname:
        self.assertNotIn('John Doe', self.browser.contents)

    def test_responsibility_with_plone_object(self):
        portal = self.layer['portal']
        contact = portal.get(portal.invokeFactory('Document', 'contact',
                                                  title='Contact Object'))

        self.task.setResponsibility(contact.UID())
        transaction.commit()

        self.browser.open(self.url)
        self.assertEqual(self.browser.url, self.url)
        self.assertIn('Contact Object', self.browser.contents)

    def test_responsibility_unknown_users_fallback(self):
        self.task.setResponsibility(('Some One', 'anyone'))
        transaction.commit()

        self.browser.open(self.url)
        self.assertEqual(self.browser.url, self.url)
        self.assertIn('Some One', self.browser.contents)
        self.assertIn('anyone', self.browser.contents)

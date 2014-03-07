from DateTime import DateTime
from ftw.builder import Builder
from ftw.builder import create
from ftw.task.testing import FTW_TASK_FUNCTIONAL_TESTING
from ftw.testbrowser import browsing
from Products.CMFCore.utils import getToolByName
from unittest2 import TestCase


class TestTaskTab(TestCase):

    layer = FTW_TASK_FUNCTIONAL_TESTING

    def setUp(self):

        self.portal = self.layer['portal']

        wftool = getToolByName(self.portal, 'portal_workflow')
        wftool.setChainForPortalTypes(('Task', ),
                                      ('one_state_workflow',))

        self.john = create(Builder('user'))

        self.task = create(Builder('task')
                           .titled('My task')
                           .having(text='<p>Text</p>')
                           .having(end_date=DateTime('2010/05/05'))
                           .having(responsibility=self.john.getId()))

    @browsing
    def test_task_tab(self, browser):
        browser.login().visit(view='tabbedview_view-tasks')

        self.assertEquals(
            [['Title', 'End', 'Responsibility', 'State', 'Creator'],
             [self.task.Title(),
              '05.05.2010 00:00',
              self.john.getProperty('fullname'),
              'published',
              'test_user_1_']],
            browser.css('.listing').first.lists())

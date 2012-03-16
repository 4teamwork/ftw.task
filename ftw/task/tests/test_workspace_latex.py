from DateTime import DateTime
from Products.CMFPlone.i18nl10n import ulocalized_time
from ftw.pdfgenerator.interfaces import IHTML2LaTeXConverter
from ftw.pdfgenerator.interfaces import ILaTeXLayout
from ftw.pdfgenerator.interfaces import ILaTeXView
from ftw.task.latex.workspace import TasksListing
from ftw.task.testing import LATEX_ZCML_LAYER
from ftw.testing import MockTestCase
from ftw.workspace.interfaces import IWorkspace
from ftw.workspace.interfaces import IWorkspaceDetailsListingProvider
from mocker import ANY
from zope.component import getMultiAdapter


class TranslationServiceStub(object):

    def __init__(self, context):
        self.context = context

    def ulocalized_time(self, *args, **kwargs):
        kwargs['context'] = self.context
        return ulocalized_time(*args, **kwargs)


class TestTasksListing(MockTestCase):

    layer = LATEX_ZCML_LAYER

    def setUp(self):
        MockTestCase.setUp(self)

        self.context = self.providing_stub(IWorkspace)
        self.expect(self.context.getPhysicalPath()).result(
            ['', 'path', 'to', 'workspace'])

        self.layout = self.stub_interface(ILaTeXLayout)
        self.expect(self.layout.use_package(ANY))

        self.view = self.stub_interface(ILaTeXView)

        def convert(*args, **kwargs):
            return getMultiAdapter(
                (self.context, self.request, self.layout),
                IHTML2LaTeXConverter).convert(*args, **kwargs)

        self.expect(self.view.convert).result(convert)

        self.response = self.stub()
        self.expect(self.response.getHeader(ANY))
        self.expect(self.response.setHeader(ANY, ANY))
        self.request = self.create_dummy(debug=True,
                                         response=self.response)
        self.expect(self.context.REQUEST).result(self.request)

        portal_catalog = self.stub()
        self.mock_tool(portal_catalog, 'portal_catalog')

        self.tasks = []
        def get_catalog_result(query):
            for obj in self.tasks:
                yield self.create_dummy(getObject=lambda x=obj: obj,
                                        **obj.__dict__)

        self.expect(portal_catalog(
                {'path': '/path/to/workspace',
                 'portal_type': ['Task'],
                 'sort_on': 'end',
                 'sort_order': 'reverse'})).call(get_catalog_result)

        self.acl_users = self.stub()
        self.mock_tool(self.acl_users, 'acl_users')
        self._mock_user('john.doe', 'John Doe')
        self._mock_user('hugo.boss', 'Hugo Boss')
        self._mock_user('jane.doe', 'Jane Doe')

        self.translation_service = TranslationServiceStub(self.context)
        self.mock_tool(self.translation_service, 'translation_service')

        self.portal_properties = self.stub()
        self.mock_tool(self.portal_properties, 'portal_properties')
        self.expect(self.portal_properties.site_properties).result(
            self.create_dummy(localLongTimeFormat='%d.%m.%Y %H:%M',
                              localTimeFormat='%d.%m.%Y',
                              localTimeOnlyFormat='%H:%M'))

    def _mock_user(self, userid, fullname):
        self.expect(self.acl_users.getUserById(userid).getProperty(
                'fullname', userid)).result(fullname)

    def test_component_is_registered(self):
        self.replay()
        listing = getMultiAdapter(
            (self.context, self.request, self.layout, self.view),
            IWorkspaceDetailsListingProvider,
            name='tasks-listing')

        self.assertEqual(type(listing), TasksListing)

    def test_implements_interface(self):
        self.replay()
        self.assertTrue(IWorkspaceDetailsListingProvider.implementedBy(
                TasksListing))

    def test_get_sort_key(self):
        self.replay()
        listing = getMultiAdapter(
            (self.context, self.request, self.layout, self.view),
            IWorkspaceDetailsListingProvider,
            name='tasks-listing')
        self.assertEqual(listing.get_sort_key(), 30)

    def test_get_title(self):
        self.replay()
        listing = getMultiAdapter(
            (self.context, self.request, self.layout, self.view),
            IWorkspaceDetailsListingProvider,
            name='tasks-listing')
        self.assertEqual(listing.get_title(), 'Tasks')

    def test_get_items(self):
        self.tasks = [
            self.create_dummy(
                # brain access:
                Title='a serious task',
                review_state='open',
                end=DateTime('05/23/2010'),
                # obj access:
                getResponsibility=lambda: ['john.doe', 'hugo.boss'])]

        self.replay()
        listing = getMultiAdapter(
            (self.context, self.request, self.layout, self.view),
            IWorkspaceDetailsListingProvider,
            name='tasks-listing')

        self.assertEqual(list(listing.get_items()), [
                {'title': 'a serious task',
                 'state': 'open',
                 'end': '23.05.2010',
                 'responsibility': 'John Doe, Hugo Boss'}])

    def test_rendering(self):
        self.tasks = [
            self.create_dummy(
                # brain access:
                Title='delightful task',
                review_state='open',
                end=DateTime('07/15/2015'),
                # obj access:
                getResponsibility=lambda: ['john.doe', 'hugo.boss']),

            self.create_dummy(
                # brain access:
                Title='a disastrous task',
                review_state='closed',
                end=DateTime('06/12/2013'),
                # obj access:
                getResponsibility=lambda: ['jane.doe', 'john.doe']),
            ]

        self.replay()
        listing = getMultiAdapter(
            (self.context, self.request, self.layout, self.view),
            IWorkspaceDetailsListingProvider,
            name='tasks-listing')

        latex = listing.get_listing()
        self.assertIn(r'\begin{tabular}', latex)

        self.assertIn(r'15.07.2015', latex)
        self.assertIn(r'open', latex)
        self.assertIn(r'delightful task', latex)
        self.assertIn(r'John Doe, Hugo Boss', latex)

        self.assertIn(r'12.06.2013', latex)
        self.assertIn(r'closed', latex)
        self.assertIn(r'a disastrous task', latex)
        self.assertIn(r'Jane Doe, John Doe', latex)

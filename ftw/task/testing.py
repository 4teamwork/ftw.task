from ftw.testing.layer import ComponentRegistryLayer


class LatexZCMLLayer(ComponentRegistryLayer):
    """A layer which only sets up the zcml, but does not start a zope
    instance.
    """

    def setUp(self):
        super(LatexZCMLLayer, self).setUp()
        import ftw.task.tests

        self.load_zcml_file('latex_test.zcml', ftw.task.tests)


LATEX_ZCML_LAYER = LatexZCMLLayer()

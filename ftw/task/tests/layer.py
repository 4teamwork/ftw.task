from Products.PloneTestCase import ptc
from collective.testcaselayer import common
from collective.testcaselayer import ptc as tcl_ptc


class Layer(tcl_ptc.BasePTCLayer):
    """Install ftw.task """

    def afterSetUp(self):
        ptc.installPackage('ftw.task')
        self.addProfile('ftw.task:default')

layer = Layer([common.common_layer])

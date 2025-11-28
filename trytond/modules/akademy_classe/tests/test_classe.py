from trytond.tests.test_tryton import ModuleTestCase, with_transaction

class ClassesTestCase(ModuleTestCase):
    "Classes Test Case"
    module = 'akademy_classe'

    @with_transaction()
    def test_method(self):
        "Test method"
        self.assertTrue(True)

del ModuleTestCase

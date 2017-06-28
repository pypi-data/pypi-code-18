import inspect
import unittest
from ..di import Container

class ClassService(object):
    def test(self):
        return 'test'

def FunctionService():
    def test():
        return 'func'
    return {"test": test}

def FunctionWithDependencies(ClassService, FunctionService):
    def test():
        return ClassService.test() + FunctionService.test()
    return {"test": test}

class ClassWithDependencies(object):
    def __init__(self, FunctionWithDependencies):
        self.service = FunctionWithDependencies

    def test(self):
        return self.service.test() + "ok"

di = Container()
di.register(ClassService, 'ClassService')
di.register(FunctionService, 'FunctionService')
di.register(FunctionWithDependencies, 'FunctionWithDependencies')
di.register(ClassWithDependencies, 'ClassWithDependencies')

class DITest(unittest.TestCase):
    def test_get_dependency(self):
        self.assertEqual(di.get('ClassService').test(), 'test')

    def test_name_does_not_exist(self):
        with self.assertRaises(Exception) as context:
            di.get('UnknownService')

        self.assertTrue(
            'Can not find' in str(context.exception),
            'Di does not throw error in case of get unknown service'
        )

    def test_function_as_a_service_provider(self):
        self.assertEqual(di.get('FunctionService').test(), 'func')

    def test_service_with_dependencies(self):
        self.assertEqual(di.get('FunctionWithDependencies').test(), 'testfunc')

    def test_service_class__with_dependencies(self):
        self.assertEqual(di.get('ClassWithDependencies').test(), 'testfuncok')

class ImpelemtationsTest(unittest.TestCase):
    def test_different_impementations(self):
        def Database(container):
            implementation = container.get('Config').getKey('Database')
            return container.getImplementation('Database', implementation)

        def Postgres():
            def test():
                return 'postgres'
            return {"test": test}

        def MySql():
            def test():
                return 'mysql'
            return {"test": test}

        def Config():
            config = {}
            def getKey(key):
                return config.get(key, None)
            def updateKey(key, name):
                config[key] = name
            return {'getKey': getKey, 'updateKey': updateKey}

        container = Container()
        container.register(Config, 'Config')
        container.get('Config').updateKey('Database', 'Postgres')
        container.registerFactory(Database, 'Database')
        container.register(Postgres, 'Database-Postgres')
        container.register(MySql, 'Database-MySql')

        self.assertEqual(container.get('Database').test(), 'postgres')


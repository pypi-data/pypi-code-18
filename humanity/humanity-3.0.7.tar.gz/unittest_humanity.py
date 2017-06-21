#! /usr/bin/python3
'''
Checks humanity module on different errors.
If we know, that in some method must be an error -
we can use @unittest.expectedFailure decorator.

Revision: 8
'''


import unittest
from humanity import *




testclass_variants = 'list', 'tuple', 'str'  # we'll create TestHumlist, TestHumtuple, etc classes
testclass = """

class TestHum{0}(unittest.TestCase):
	classname = 'hum{0}'  # for testing by comparing to self.__class__ and creating objects
	
	def setUp(self):
		self.i = self.create_sequence((1,2,3,4,5,6,7,8,9), TestHum{0}.classname)
		
	def tearDown(self):
		del self.i
	
	
	def create_sequence(self, sequence, classname):  # чтобы несколько раз не писать
		'''Creates and returnes object of needed type
		from -inputed sequence data- and -classname-.
		'''
		
		if sequence.__class__ == tuple:	
			return eval("{{0}}{{1}}".format(classname, str(sequence)))  # результат всегда в скобках
		else:
			if classname == 'humstr':
				return eval("{{0}}{{1}}".format(classname, '('+str(sequence)+')'))  # результат всегда в скобках
			else:
				return eval("{{0}}{{1}}".format(classname, '('+str(sequence)+',)'))  # результат всегда в скобках
	
	
	def create_object(self, value, classname):
		if classname == 'humlist' or classname == 'humtuple':
			return value
		elif classname == 'humstr':
			return str(value)
	
	
	
	
	def test_sequence_slices_1(self):
		'''Весь вперед.'''
		self.assertEqual( self.i[1:9:1], self.create_sequence((1,2,3,4,5,6,7,8,9), self.classname) )
	
	def test_sequence_slices_2(self):
		'''Часть вперед.'''
		self.assertEqual( self.i[2:4], self.create_sequence((2,3,4), self.classname) )
	
	def test_sequence_slices_3(self):
		'''С середины до конца с выходом за правый край.'''
		self.assertEqual( self.i[2:100], self.create_sequence((2,3,4,5,6,7,8,9), self.classname) )
	
	def test_sequence_slices_5(self):
		'''Срез. Выход за оба края.'''
		self.assertEqual( self.i[0:100], self.create_sequence((1,2,3,4,5,6,7,8,9), self.classname) )
	
	def test_sequence_slices_6(self):
		'''Весь вперед с шагом.'''
		self.assertEqual( self.i[1:9:2], self.create_sequence((1,3,5,7,9), self.classname) )
	
	def test_sequence_slices_7(self):
		'''Шаг равен нулю.'''
		with self.assertRaises(ValueError):
			self.i[1:9:0]
	
	def test_sequence_slices_8(self):
		'''Обратный порядок.'''
		self.assertEqual( self.i[9:1:-1], self.create_sequence((9,8,7,6,5,4,3,2,1), self.classname) )
	
	def test_sequence_slices_9(self):
		'''Обратный порядок. Другой шаг.'''
		self.assertEqual( self.i[9:1:-2], self.create_sequence((9,7,5,3,1), self.classname) )
	
	def test_sequence_slices_10(self):
		'''Обратный порядок. Выход за левую границу.'''
		self.assertEqual( self.i[10:1:-2], self.create_sequence((9,7,5,3,1), self.classname) )
	
	def test_sequence_slices_11(self):
		'''Обратный порядок. Выход за обе границы.'''
		self.assertEqual( self.i[10:0:-2], self.create_sequence((9,7,5,3,1), self.classname) )
	
	def test_sequence_slices_12(self):
		'''Обратный порядок. Выход за обе границы. Другой шаг.'''
		self.assertEqual( self.i[10:0:-1], self.create_sequence((9,8,7,6,5,4,3,2,1), self.classname) )
	
	def test_sequence_slices_13(self):
		'''Обратный порядок. Шаг равен нулю.'''
		with self.assertRaises(ValueError):
			self.i[9:1:0]
	
	def test_sequence_slices_14(self):
		'''Обратный порядок. Шаг равен размеру массива.'''
		self.assertEqual( self.i[9:1:-9], self.create_sequence(9, self.classname) )  # запятая для теста
	
	
	def test_sequence_slices_15(self):
		'''Обратный порядок. Без шага.'''
		self.assertEqual(self.i[9:1:], hum{0}(), self.classname)
	
	
	
		
	def test_sequence_classname(self):
		'''Имя класса проверяем.'''
		self.assertEqual( self.i.__class__, eval(self.classname) )
		
	def test_sequence_get_1(self):
		'''Проверяем метод .get().'''
		self.assertEqual( self.i.get(3), self.create_object(3, self.classname) )
		
	def test_sequence_get_2(self):
		'''Проверяем метод .get(). Выход за пределы.'''
		self.assertEqual( self.i.get(18), None )
	
	
	
	
	# specific for humstr:
		
	def test_humstr_find_1(self):
		'''Проверяет метод find.
		'''
		if self.classname == 'humstr':
			self.assertEqual( self.i.find('7'), 7 )
	
	def test_humstr_find_2(self):
		'''Проверяет метод find.
		'''
		if self.classname == 'humstr':
			self.assertEqual( self.i.find('abc'), -1 )
	
	
	def test_humstr_rfind_1(self):
		'''Проверяет метод rfind.
		'''
		if self.classname == 'humstr':
			self.assertEqual( self.i.rindex('7'), 7 )
	
	def test_humstr_rfind_2(self):
		'''Проверяет метод rfind.
		'''
		if self.classname == 'humstr':
			self.assertEqual( self.i.rfind('abc'), -1 )
	
	
	
	
	def test_humstr_index_1(self):
		'''Проверяет метод index.
		'''
		if self.classname == 'humstr':
			self.assertEqual( self.i.index('7'), 7 )
	
	def test_humstr_index_2(self):
		'''Проверяет метод index.
		'''
		if self.classname == 'humstr':
			with self.assertRaises(ValueError):
				self.i.index('abc')
	
	
	def test_humstr_rindex(self):
		'''Проверяет метод rindex.
		'''
		if self.classname == 'humstr':
			self.assertEqual( self.i.rindex('7'), 7 )
	
	def test_humstr_rindex_2(self):
		'''Проверяет метод rindex.
		'''
		if self.classname == 'humstr':
			with self.assertRaises(ValueError):
				self.i.rindex('abc')
"""	

for variant in testclass_variants:  # чтобы несколько раз не писать
	exec(testclass.format(variant))  # создали несколько классов с одинаковыми проверками








class TestHumdict(unittest.TestCase):
	def setUp(self):
		self.i = humdict({'df':'3242345'})
	def tearDown(self):
		del self.i
	
	
	def test_get_1(self):
		self.assertEqual( self.i['df'], '3242345' )
		
	def test_assign_2(self):
		def test_func():
			self.i['333'] = 444
			return self.i['333']
		self.assertEqual( test_func(), 444 )
		
	def test_classname(self):
		self.assertEqual( self.i.__class__, humdict )
	
	def test_get(self):
		self.assertEqual( self.i.get('4'), None )
		
	def test_get_2(self):
		self.assertEqual( self.i.get('df'), '3242345' )








class TestHumrange(unittest.TestCase):
	def setUp(self):
		pass
	def tearDown(self):
		pass
	
	
	def test_humrange_1(self):
		self.assertEqual( list(humrange(4, 4, 1)), [4] )
		
	def test_humrange_2(self):
		with self.assertRaises(ValueError):
			list(humrange(4, 4, -1))
	
	def test_humrange_3(self):
		self.assertEqual( list(humrange(4, 4)), [4] )
	
	def test_humrange_4(self):
		with self.assertRaises(ValueError):
			list(humrange(4, 4, 0))
	
	def test_humrange_5(self):
		self.assertEqual( list(humrange(4, 8)), [4, 5, 6, 7, 8] )
	
	def test_humrange_6(self):
		self.assertEqual( list(humrange(0, 2)), [0, 1, 2] )
	
	def test_humrange_7(self):
		with self.assertRaises(ValueError):
			list(humrange(4, 2))
	
	def test_humrange_8(self):
		self.assertEqual( list(humrange(4, 2, -1)), [4, 3, 2] )
	
	def test_humrange_9(self):
		self.assertEqual( list(humrange(4, 2, -2)), [4, 2] )
	
	def test_humrange_10(self):
		self.assertEqual( list(humrange(1, -1, -2)), [1, -1] )
	
	def test_humrange_11(self):
		self.assertEqual( list(humrange(1, -1, -1)), [1, 0, -1] )
	
	def test_humrange_12(self):
		with self.assertRaises(ValueError):
			list(humrange(4, 2, 1))
	
	def test_humrange_13(self):
		with self.assertRaises(ValueError):
			list(humrange(0))
	
	def test_humrange_14(self):
		self.assertEqual( list(humrange(1)), [1] )
	
	def test_humrange_15(self):
		self.assertEqual( list(humrange(2)), [1, 2] )








class Testhumdrange(unittest.TestCase):
	def setUp(self):
		pass
	def tearDown(self):
		pass
	
	
	
	def test_humdrange_1(self):
		self.assertEqual( list(humdrange(4, 4, 1)), [4] )
		
	def test_humdrange_2(self):
		self.assertEqual( list(humdrange(4, 4, -1)), [4] )
	
	def test_humdrange_8(self):
		self.assertEqual( list(humdrange(4, 2, -1)), [4, 3, 2] )
	
	def test_humdrange_9(self):
		self.assertEqual( list(humdrange(4, 2, -2)), [4, 2] )
	
	def test_humdrange_10(self):
		self.assertEqual( list(humdrange(1, -1, -2)), [1, -1] )
	
	def test_humdrange_11(self):
		self.assertEqual( list(humdrange(1, -1, -1)), [1, 0, -1] )
	
	def test_humdrange_13(self):
		self.assertEqual( list(humdrange(4, 3, '-0.5')), [4, 3.5, 3] )
	
	def test_humdrange_14(self):
		self.assertEqual( list(humdrange(3, 4, '0.5')), [3, 3.5, 4] )
	
	def test_humdrange_17(self):
		self.assertEqual( len(humdrange(4, 3, '-0.5')), 3 )
	
	def test_humdrange_18(self):
		self.assertEqual( len(humdrange(1, 3, '0.2')), 11 )
	
	def test_humdrange_22(self):
		self.assertEqual( list(humdrange('1', 3, '0.4')), 
			[Decimal('1'), Decimal('1.4'), Decimal('1.8'), 
			Decimal('2.2'), Decimal('2.6'), Decimal('3.0')] )
	
	
	
	def test_humdrange_errors_1(self):
		with self.assertRaises(ValueError):
			list(humrange(4, 4, 0))
	
	def test_humdrange_errors_2(self):
		with self.assertRaises(ValueError):
			list(humdrange(4, 2, 1))
	
	def test_humdrange_errors_3(self):
		with self.assertRaises(ValueError):
			list(humdrange(4, 3, '0.5'))
	
	def test_humdrange_errors_4(self):
		with self.assertRaises(ValueError):
			list(humdrange(3, 4, '-0.5'))
	
	def test_humdrange_errors_5(self):
		with self.assertRaises(TypeError):
			humdrange(0.5, 3, 1)
	
	def test_humdrange_errors_6(self):
		with self.assertRaises(TypeError):
			humdrange(5, 3.1, 1)
	
	def test_humdrange_errors_7(self):
		with self.assertRaises(TypeError):
			humdrange(5, 3, 0.1)
	
	
	
	def test_humdrange_types_1(self):
		self.assertEqual( list(humdrange(1, -2, '-0.5', 'dec')[5:1:-2]), [Decimal('-1.0'), Decimal('0.0'), 
			Decimal('1.0')] )
	
	def test_humdrange_types_2(self):
		self.assertEqual( list(humdrange(1, -2, '-0.5', 'float')[5:1:-2]), [-1.0, 0.0, 1.0] )
	
	def test_humdrange_types_3(self):
		self.assertEqual( list(humdrange(1, -2, '-0.5', 'str')[5:1:-2]), ['-1.0', '0.0', '1.0'] )
	
	def test_humdrange_types_4(self):
		self.assertEqual( list(humdrange(1, -2, '-0.5', 'int')[5:1:-2]), [-1, 0, 1] )
	
	def test_humdrange_types_5(self):
		self.assertEqual( list(humdrange(3, 4, '0.2', 'int')[-1:1:-1]), [4, 3, 3, 3, 3, 3] )
	
	
	
	def test_humdrange_types_errors_1(self):
		with self.assertRaises(ValueError):  # because of zero passed to slice
			humdrange(3, 4, '0.2', 'other')
	
	def test_humdrange_types_errors_2(self):
		with self.assertRaises(TypeError):  # because of zero passed to slice
			humdrange(3, 4, '0.2', 423)
	
	
	
	def test_humdrange_indexes_1(self):
		self.assertEqual( humdrange(4, 4, 1)[-1], 4 )
	
	def test_humdrange_indexes_1_a(self):
		self.assertEqual( humdrange(4, 8, 1)[-1], 8 )
	
	def test_humdrange_indexes_1_b(self):
		self.assertEqual( humdrange(4, 8, 1)[-5], 4 )
	
	def test_humdrange_indexes_2(self):
		self.assertEqual( humdrange('1', 3, '0.4')[2], Decimal('1.4'))
	
	def test_humdrange_indexes_3(self):
		self.assertEqual( humdrange('3', 1, '-0.4')[2], Decimal('2.6'))
	
	def test_humdrange_indexes_4(self):
		self.assertEqual( humdrange('3', 1, '-0.4')[1], Decimal('3.0'))
	
	def test_humdrange_indexes_5(self):
		self.assertEqual( humdrange('8', 0, '-0.1')[4], Decimal('7.7'))
	
	
	
	def test_humdrange_indexes_errors_1(self):
		with self.assertRaises(IndexError):  # because of zero passed to slice
			humdrange(5, 3, '-0.1')[0]
	
	
	
	def test_humdrange_slices_1(self):
		self.assertEqual( list(humdrange('3', 1, '-0.4')[1:3]), [Decimal('3.0'), Decimal('2.6'), Decimal('2.2')] )
	
	def test_humdrange_slices_2(self):
		self.assertEqual( list(humdrange('1', 2, '0.5')[1:]), [Decimal('1.0'), Decimal('1.5'), Decimal('2.0')])
	
	def test_humdrange_slices_3(self):
		self.assertEqual( list(humdrange('1', 2, '0.5')[:3]), [Decimal('1.0'), Decimal('1.5'), Decimal('2.0')])
	
	def test_humdrange_slices_4(self):
		self.assertEqual( list(humdrange('1', 2, '0.5')[:]), [Decimal('1.0'), Decimal('1.5'), Decimal('2.0')])
	
	def test_humdrange_slices_5(self):
		self.assertEqual( list(humdrange('1', 2, '0.5')[1:3:2]), [Decimal('1.0'), Decimal('2.0')])
	
	def test_humdrange_slices_6(self):
		self.assertEqual( list(humdrange('1', 2, '0.5')[::2]), [Decimal('1.0'), Decimal('2.0')])
	
	def test_humdrange_slices_7(self):
		self.assertEqual( list(humdrange(5, 3, '-0.1')[1::2]) , [Decimal('5.0'), Decimal('4.8'), 
			Decimal('4.6'), Decimal('4.4'), Decimal('4.2'), Decimal('4.0'), Decimal('3.8'), 
			Decimal('3.6'), Decimal('3.4'), Decimal('3.2'), Decimal('3.0')] )
	
	def test_humdrange_slices_8(self):	
		self.assertEqual( list(humdrange(5, 3, '-0.1')[1::-2]), [5] )
	
	def test_humdrange_slices_12(self):
		self.assertEqual( list(humdrange(4, 3, '-0.2')[::1]), [Decimal('4.0'), Decimal('3.8'), Decimal('3.6'),
			Decimal('3.4'), Decimal('3.2'), Decimal('3.0')] )
	
	def test_humdrange_slices_13(self):
		self.assertEqual( list(humdrange(3, 4, '0.2')[::1]), [Decimal('3.0'), Decimal('3.2'), Decimal('3.4'), 
			Decimal('3.6'), Decimal('3.8'), Decimal('4.0')] )
	
	def test_humdrange_slices_14(self):
		self.assertEqual( list(humdrange(3, 4, '0.2')[-1:1:-1]), [Decimal('4.0'), Decimal('3.8'), Decimal('3.6'),
			Decimal('3.4'), Decimal('3.2'), Decimal('3.0')] )
	
	def test_humdrange_slices_15(self):
		self.assertEqual( list(humdrange(3, 4, '0.2')[-1:1:-2]), [Decimal('4.0'), Decimal('3.6'),
			Decimal('3.2')] )
	
	def test_humdrange_slices_16(self):
		self.assertEqual( list(humdrange(3, 4, '0.2')[-1:-3:-2]), [Decimal('4.0'), Decimal('3.6')] )
	
	def test_humdrange_slices_17(self):
		self.assertEqual( list(humdrange(3, 4, '0.2')[1:-3:2]), [Decimal('3.0'), Decimal('3.4')] )
	
	def test_humdrange_slices_18(self):
		self.assertEqual( list(humdrange(-2, 1, '0.5')[1:3:1]), [Decimal('-2.0'), Decimal('-1.5'), 
			Decimal('-1.0')] )
	
	def test_humdrange_slices_19(self):
		self.assertEqual( list(humdrange(-2, 1, '0.5')[1:3:2]), [Decimal('-2.0'), Decimal('-1.0')] )
	
	def test_humdrange_slices_20(self):
		self.assertEqual( list(humdrange(1, -2, '-0.5')[1:5:2]), [Decimal('1.0'), Decimal('0.0'), 
			Decimal('-1.0')] )
	
	def test_humdrange_slices_21(self):
		self.assertEqual( list(humdrange(1, -2, '-0.5')[1:5:2]), [Decimal('1.0'), Decimal('0.0'), 
			Decimal('-1.0')] )
	
	def test_humdrange_slices_21_a(self):
		self.assertEqual( list(humdrange(1, -2, '-0.5')[5:1:-2]), [Decimal('-1.0'), Decimal('0.0'), 
			Decimal('1.0')] )
	
	def test_humdrange_slices_22_a(self):
		self.assertEqual( list(humdrange(1, -2, '-0.5')[1:1:-2]), [Decimal('1.0')] )
	
	def test_humdrange_slices_22_b(self):
		self.assertEqual( list(humdrange(1, -2, '-0.5')[1:1:2]), [Decimal('1.0')] )
	
	
	
	def test_humdrange_slices_errors_1(self):
		with self.assertRaises(IndexError):  # because of zero passed to slice
			humdrange(3, 5, '0.1')[0:2:-2]
	
	def test_humdrange_slices_errors_2(self):
		with self.assertRaises(IndexError):  # because of zero passed to slice
			humdrange(5, 3, '-0.1')[1:0:-2]
	
	def test_humdrange_slices_errors_3(self):
		with self.assertRaises(ValueError):  # because of zero passed to slice
			humdrange(3, 5, '0.1')[1:2:0]








class Testdrange(unittest.TestCase):
	def setUp(self):
		pass
	def tearDown(self):
		pass
	
	
	
	def test_drange_indexes_1(self):
		self.assertEqual( drange(1, 8, 1, 'int')[4], 5 )
	
	def test_drange_indexes_1_a(self):
		self.assertEqual( drange(1, 8, 1, 'int')[0], 1 )
	
	def test_drange_indexes_1_b(self):
		self.assertEqual( drange(1, 8, 1, 'int')[7], 8 )
	
	def test_drange_indexes_2(self):
		self.assertEqual( drange(1, 8, 1, 'int')[-3], 6 )
	
	def test_drange_indexes_2_a(self):
		self.assertEqual( drange(1, 8, 1, 'int')[-1], 8 )
	
	def test_drange_indexes_2_b(self):
		self.assertEqual( drange(1, 8, 1, 'int')[-8], 1 )
	
	
	
	def test_drange_slices_1(self):  
		'''Весь вперед.'''
		self.assertEqual(list(drange(1, 8, 1, 'int')[0:8:1]), [1,2,3,4,5,6,7,8])

	def test_drange_slices_2(self):
		'''Часть вперед.'''
		self.assertEqual(list(drange(1, 8, 1, 'int')[2:4]), [3,4])
	
	def test_drange_slices_2_a(self):
		'''Часть назад.'''
		self.assertEqual(list(drange(1, 8, 1, 'int')[4:2:-1]), [5,4])

	def test_drange_slices_3(self):
		'''Весь вперед с шагом.'''
		self.assertEqual( list(drange(1, 8, 1, 'int')[0:8:2]), [1,3,5,7] )
	
	def test_drange_slices_4(self):
		'''Обратный порядок.'''
		self.assertEqual( list(drange(1, 8, 1, 'int')[7::-1]), [8,7,6,5,4,3,2,1] )

	def test_drange_slices_4_a(self):
		'''Обратный порядок. Другой шаг.'''
		self.assertEqual( tuple(drange(1, 8, 1, 'int')[7::-2]), (8,6,4,2) )

	def test_drange_slices_4_b(self):
		'''Обратный порядок. Выход за левую границу.'''
		self.assertEqual( tuple(drange(1, 8, 1, 'int')[7:0:-2]), (8,6,4,2) )
	
	def test_drange_slices_4_c(self):
		'''Обратный порядок. Выход за левую границу.'''
		self.assertEqual( tuple(drange(1, 8, 1, 'int')[7:0:-1]), (8,7,6,5,4,3,2) )
	
	def test_drange_slices_5(self):
		'''Обратный порядок. Выход за левую границу.'''
		self.assertEqual( tuple(drange(1, 8, 1, 'int')[7:1:-1]), (8,7,6,5,4,3) )
	
	def test_drange_slices_5_b(self):
		'''Обратный порядок. Выход за левую границу.'''
		self.assertEqual( tuple(drange(1, 8, 1, 'int')[:1:-1]), (8,7,6,5,4,3) )
	
	def test_drange_slices_5_c(self):
		'''Обратный порядок. Выход за левую границу.'''
		self.assertEqual( tuple(drange(1, 8, 1, 'int')[::-1]), (8,7,6,5,4,3,2,1) )
	
	def test_drange_slices_6(self):
		'''Обратный порядок. Шаг равен размеру массива (все как и в стандартном Python-e).'''
		self.assertEqual( tuple(drange(1, 8, 1, 'int')[7::-7]), (8,1))
	
	
	
	def test_drange_slices_errors_1(self):
		'''С середины до конца с выходом за правый край.'''
		with self.assertRaises(IndexError):
			drange(1, 8, 1, 'int')[2:100]
	
	def test_drange_slices_errors_1_a(self):
		'''Срез. Выход за правый край.'''
		with self.assertRaises(IndexError):
			drange(1, 8, 1, 'int')[0:100]
	
	def test_drange_slices_errors_2(self):
		'''Шаг равен нулю.'''
		with self.assertRaises(ValueError):
			drange(1, 8, 1, 'int')[0:8:0]
	
	def test_drange_slices_errors_2_a(self):
		'''Обратный порядок. Шаг равен нулю.'''
		with self.assertRaises(ValueError):
			drange(1, 8, 1, 'int')[7:1:0]
	
	def test_drange_slices_errors_3(self):
		'''A > B при прямом порядке.'''
		with self.assertRaises(ValueError):
			drange(1, 8, 1, 'int')[7:1:1]
	
	def test_drange_slices_errors_3_c(self):
		'''A < B при обратном порядке.'''
		with self.assertRaises(ValueError):
			drange(1, 8, 1, 'int')[5:6:-1]
	
	def test_drange_slices_errors_4(self):
		'''B выходит за пределы - второй индекс берется не включительно при обр. порядке.'''
		with self.assertRaises(IndexError):
			drange(1, 8, 1, 'int')[1:7:-1]
	
	def test_drange_slices_errors_4_a(self):
		'''B выходит за пределы - второй индекс берется не включительно при обр. порядке.'''
		with self.assertRaises(IndexError):
			drange(1, 8, 1, 'int')[7:7:-1]
	
	def test_drange_slices_5(self):
		'''Обратный порядок. Выход за левую границу.'''
		with self.assertRaises(IndexError):
			drange(1, 8, 1, 'int')[10:0:-1]
	
	def test_drange_slices_5_a(self):
		'''Прямой порядок порядок без шага (в прямом ошибок не будет).'''
		with self.assertRaises(IndexError):
			drange(1, 8, 1, 'int')[7:0:]








if __name__ == "__main__":
	unittest.main()

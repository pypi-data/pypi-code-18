from . import PromisePay

import json
import copy

class Wallet(PromisePay):
	
	def __init__(self,user_id):
		PromisePay.__init__(self)
		self.status='success'
		self.error_message = ''
		self.user_id= user_id
		
		self.g = self.get_one(path='/users/'+self.user_id+'/wallet_accounts/')
		
		print self.g
		if self.g.has_key('errors'):
			self.status='failed'
			self.error_message = self.g['errors']
		else:

			self.before_clean = copy.deepcopy(self.g)
			del self.g['wallet_accounts']['links']
			self.__dict__.update(json.loads(json.dumps(self.g['wallet_accounts'],sort_keys=True, indent=4)))
			self.__dict__.update(json.loads(json.dumps(self.before_clean['wallet_accounts']['links'],sort_keys=True, indent=4)))



	def deposit(self,account_id,amount):
		self.account_id= account_id
		self.amount = amount
		x = self.add_one(path='/wallet_accounts/'+self.id+'/deposit',data={'account_id':self.account_id,\
				'amount':str(int(self.amount))})

		if x.has_key('errors'):
			self.status='failed'
			try:
				self.error_message = x['errors']['transaction'][0]
			except:
				self.error_message = x['errors']

		return x


	def withdraw(self,target,amount):
		self.account_id= target
		self.amount = amount
		x = self.add_one(path='/wallet_accounts/'+self.id+'/withdraw',data={'account_id':self.account_id,\
				'amount':str(int(self.amount))})

		if x.has_key('errors'):
			self.status='failed'
			try:
				self.error_message = x['errors']['transaction'][0]
			except:
				self.error_message = x['errors']

		return x



class PromisePayCardAccount(PromisePay):
	
	def __init__(self,card_id=None):
		
		PromisePay.__init__(self)
		self.status='success'
		self.error_message = ''

		if card_id:
			self.card_id= card_id
			self.g = self.get_one(path='/card_accounts/'+self.card_id)
			
			if self.g.has_key('errors'):
				self.status='failed'
				self.error_message = self.g['errors']
			else:
				self.before_clean = copy.deepcopy(self.g)
				del self.g['card_accounts']['links']
				del self.g['card_accounts']['card']

				self.__dict__.update(json.loads(json.dumps(self.g['card_accounts'],sort_keys=True, indent=4)))
				self.__dict__.update(json.loads(json.dumps(self.before_clean['card_accounts']['links'],sort_keys=True, indent=4)))
				self.__dict__.update(json.loads(json.dumps(self.before_clean['card_accounts']['card'],sort_keys=True, indent=4)))


	def delete_card(self):
		self.g = self.delete_one(path='/card_accounts/',id=self.card_id)
		
		if self.g.has_key('errors'):
			self.status='failed'
			self.error_message = self.g['errors']
		

	def get_user_card(self,user_id):
		self.user_id= user_id
		self.g = self.get_one(path='/users/'+self.user_id+'/card_accounts/')
		
		if self.g.has_key('errors'):
			self.status='failed'
			self.error_message = self.g['errors']
		else:
			self.before_clean = copy.deepcopy(self.g)
			del self.g['card_accounts']['links']
			del self.g['card_accounts']['card']


			self.__dict__.update(json.loads(json.dumps(self.g['card_accounts'],sort_keys=True, indent=4)))
			self.__dict__.update(json.loads(json.dumps(self.before_clean['card_accounts']['links'],sort_keys=True, indent=4)))
			self.__dict__.update(json.loads(json.dumps(self.before_clean['card_accounts']['card'],sort_keys=True, indent=4)))



	def generate_token(self,user_id):

		promise_pay_token = ''

		try:
			k = self.add_one(path='token_auths',data={'token_type':'card','user_id':user_id})
			promise_pay_token = k["token_auth"]["token"]

			if k.has_key('errors'):
				self.status='failed'
				self.error_message = x['errors']
	
		except:
			self.status='failed'
			self.error_message = "Something went wrong"

		return promise_pay_token





class PromisePayBankAccount(PromisePay):
	
	def __init__(self,bank_id=None):
		
		PromisePay.__init__(self)
		self.status='success'
		self.error_message = ''

		if bank_id:
			self.bank_id= bank_id
			self.g = self.get_one(path='/bank_accounts/'+self.bank_id)
			
			if self.g.has_key('errors'):
				self.status='failed'
				self.error_message = self.g['errors']
			else:
				self.before_clean = copy.deepcopy(self.g)
				del self.g['bank_accounts']['links']
				del self.g['bank_accounts']['bank']

				self.__dict__.update(json.loads(json.dumps(self.g['bank_accounts'],sort_keys=True, indent=4)))
				self.__dict__.update(json.loads(json.dumps(self.before_clean['bank_accounts']['links'],sort_keys=True, indent=4)))
				self.__dict__.update(json.loads(json.dumps(self.before_clean['bank_accounts']['bank'],sort_keys=True, indent=4)))



	def get_user_bank(self,user_id):
		self.user_id= user_id
		self.g = self.get_one(path='/users/'+self.user_id+'/bank_accounts/')
		
		if self.g.has_key('errors'):
			self.status='failed'
			self.error_message = self.g['errors']
		else:
			self.before_clean = copy.deepcopy(self.g)
			del self.g['bank_accounts']['links']
			del self.g['bank_accounts']['bank']

			self.__dict__.update(json.loads(json.dumps(self.g['bank_accounts'],sort_keys=True, indent=4)))
			self.__dict__.update(json.loads(json.dumps(self.before_clean['bank_accounts']['links'],sort_keys=True, indent=4)))
			self.__dict__.update(json.loads(json.dumps(self.before_clean['bank_accounts']['bank'],sort_keys=True, indent=4)))

	
	def delete_bank(self):
		self.g = self.delete_one(path='/bank_accounts/',id=self.bank_id)
		
		if self.g.has_key('errors'):
			self.status='failed'
			self.error_message = self.g['errors']
		


	def generate_token(self,user_id):

		promise_pay_token = ''

		try:
			k = self.add_one(path='token_auths',data={'token_type':'bank','user_id':user_id})
			promise_pay_token = k["token_auth"]["token"]

			if k.has_key('errors'):
				self.status='failed'
				self.error_message = x['errors']
	
		except:
			self.status='failed'
			self.error_message = "Something went wrong"

		return promise_pay_token








class PromisePayUser(PromisePay):
	
	def __init__(self,user_id=None):
		PromisePay.__init__(self)
		self.status='success'
		self.error_message = ''
		
		if user_id:
			self.user_id= user_id
			self.g = self.get_one(path='/users/'+self.user_id)
			
			if self.g.has_key('errors'):
				self.status='failed'
				self.error_message = self.g['errors']
			
			else:
				self.before_clean = copy.deepcopy(self.g)
				del self.g['users']['links']
				del self.g['users']['related']
				self.__dict__.update(json.loads(json.dumps(self.g['users'],sort_keys=True, indent=4)))
				self.__dict__.update(json.loads(json.dumps(self.before_clean['users']['links'],sort_keys=True, indent=4)))


	def all(self,limit=10,offset=0):
		self.limit = limit
		self.offset=offset
		datas = self.get_list(path='/users/',limit=self.limit,offset=self.offset)['users']
		data_list = []

		for user in json.loads(json.dumps(datas,sort_keys=True, indent=4)):
			print user
			u = PromisePayUser(user['id'])
			data_list.append(u)

		return data_list


	def create(self,**kwargs):
		
		x = self.add_one(path='users',data=kwargs)
		
		if x.has_key('errors'):
			self.status='failed'
			self.error_message = x['errors']
		
		if self.status=='success':
			return PromisePayUser(x['id'])
		
		else:
			return self.error_message


	def update(self,**kwargs):

		if self.user_id:
			x = self.edit_one(path='users',id=self.user_id,data=kwargs)

			try:
				if x.json().has_key('errors'):
					self.status='failed'
					self.error_message = x.json()['errors']
				else:
					return PromisePayUser(self.user_id)
			
			except:
				self.status='failed'
				self.error_message = "Something went wrong"

			return x
		
		else:
			self.status='failed'
			self.error_message = 'User ID is required'



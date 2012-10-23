from django.contrib.auth.backends import ModelBackend

class AccountsBackend(ModelBackend):
	def authenticate(self, username= None, password= None):
		return super(AccountsBackend, self).authenticate(username , password )

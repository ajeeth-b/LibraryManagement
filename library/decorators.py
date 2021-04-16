def enclose_with_hash(func):
	def wrapper(*args, **kwargs):
		print('\n'+'##'*15)
		func(*args, **kwargs)
		print('##'*15,'\n')
	return wrapper

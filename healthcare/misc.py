
		# user = authenticate(request, username=username, password=password)
		# if user is not None:
		# 	login(request, user)
		# 	messages.success(request, ("You have successuflly logged in!!"))
		# 	return redirect('home')
		# else:
		# 	messages.success(request, ("There was an error while logging in!!"))
		# 	return redirect('login')


		
	# 	username =  request.POST['username']
	# 	password = encrypt_pwd(request.POST['password'])

	# 	cursor = connections['default'].cursor()
	# 	queryDup = 'SELECT name FROM healthcare_user WHERE name = %s AND password = %s;'	
	# 	row = cursor.execute(queryDup, (username, password))

	# 	if row == 0:
	# 		messages.success(request, ("There was an error while logging in!"))
	# 		global authenticateUser 
	# 		authenticateUser = False
	# 		return redirect('login')
	# 	else:
	# 		messages.success(request, ("You have successuflly logged in!!"))
	# 		global authenticateUser
	# 		authenticateUser = True
	# 		return redirect('home')
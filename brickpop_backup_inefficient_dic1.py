
'''
C:\Python27\python.exe C:\Users\groveh\Documents\Brickpop\brickpop.py
'''
import time

def measure_efficiency():
	#run with Bd_measure.txt
	build_board_start = time.time()
	global board
	
	for x in range(100):
		build_board()
		print x/4
	temp_board = board
	assign_pieces_start = time.time()
	for x in range(100):
		assign_pieces()
		print x/4+25
	fall_start = time.time()
	for x in range(100):
		board = temp_board
		fall()
		print x/4+50
	shift_start = time.time()
	for x in range(100):
		board = temp_board
		shift()
		print x/4+75
	end = time.time()
	print "build_board():",(assign_pieces_start - build_board_start)
	print "assign_pieces():",(fall_start - assign_pieces_start)
	print "fall():",(shift_start - fall_start)
	print "shift():",(end - shift_start)

def print_board():
	print 
	for x in board:
		print x
	#print board_as_string

def build_board():
	global board,board_as_string
	board_as_string = ''
	_file = open("C:\Users\groveh\Documents\Brickpop\Bd5.txt",'r')
	for line in _file:
		#print line
		board.append(line.strip())
		board_as_string += line.strip()
		if len(board) == 10:
			break

def build_string():
	global board_as_string
	board_as_string = ''
	for x in board:
		board_as_string+=x

def bd(tuple_coor):
	return board[tuple_coor[0]][tuple_coor[1]]

def next_to(cor1,cor2):
	if(cor1[0] == cor2[0] and abs(cor1[1]-cor2[1]) == 1):
		return True
	if(cor1[1] == cor2[1] and abs(cor1[0]-cor2[0]) == 1):
		return True
	return False




def assign_pieces():
	global f
	pieces = []
	piece_coors = []
	current_coors = 0,0
	current_letter = bd(current_coors)
	piece = []
	start = time.time()
	for vertical in range(10):
		for horizontal in range(10): 
			current_letter = board[vertical][horizontal]
			if(current_letter== '.'):
				continue
			current_coors = (vertical,horizontal)
			pieces.append([current_coors])
	separated_pieces = True
	bef = time.time()
	g = 0
	while(separated_pieces):
		g+=1
		mid1 = time.time()
		temp = pieces
		pieces = []
		for x in temp:
			if(x!=[]):
				pieces.append(x)
		should_delete = False
		mid2 = time.time()
		for x in pieces:
			should_delete = False
			mid3 = time.time()
			for y in x:
				mid4 = time.time()
				for w in range(len(pieces)):
					if(len(pieces[w])>0 and len(x)>0 and pieces[w][0] == x[0]):
						continue
					mid5 = time.time()
					for v in pieces[w]:
						if(next_to(y,v) and bd(y) == bd(v)):
							should_delete=True
					if(should_delete):
						for g in range(len(pieces[w])):
							x.append(pieces[w][g])
						pieces[w]= []
						break
					mid6 = time.time()
				if(should_delete):
					break
			if(should_delete):
				break
			mid7 = time.time()

		if(should_delete == False):
			separated_pieces = False
		mid8 = time.time()
	mid9 = time.time()
	'''
	print "before:",(bef-start)
	print "mid1:",(mid2-mid1)
	print "mid2:",(mid3-mid2)
	print "mid3:",(mid4-mid3)
	print "mid4:",(mid5-mid4)
	print "mid5:",(mid6-mid5)
	print "mid6:",(mid7-mid6)
	print "mid7:",(mid8-mid7)
	print "mid8:",(mid9-mid8)
	print 
	print 'overall mids'
	print "while:",(mid9-bef)
	print 'in while loop',g,'times'

	
	s = 0
	for x in pieces:
		print x
		s+=(len(x))

	print s
	'''

	#print len(possible_boards.keys())
	return pieces

def fall():
	global board
	blocks_need_to_fall = True
	while(blocks_need_to_fall):
		falling = False
		for x in range(1,10):
			for y in range(10):
				if(board[x][y] == '.'):
					for h in range(x):
						if(board[h][y]!='.'):
							falling = True
							for g in range(x,0,-1):
								new_line_one = ''
								new_line_two = ''
								for m in range(10):
									if(m==y):
										new_line_one += board[g-1][m]
									else:
										new_line_one += board[g][m]
								for m in range(10):
									if(m==y):
										new_line_two += '.'
									else:
										new_line_two += board[g-1][m]
								board[g] = new_line_one
								board[g-1] = new_line_two
							break
					if(falling):
						break
			if(falling):
				break
		if(falling == False):
			blocks_need_to_fall = False
	#print_board()

def shift():
	global board
	blocks_need_to_shift = True
	while(blocks_need_to_shift):
		column = -1
		shifting = False
		for x in range(10):
			if(board[9][x] == '.'):
				shifting = False
				for g in range(x,10):
					if(board[9][g]!='.'):
						shifting = True
						break
				if(shifting):
					column = x
		if(column!=-1):
			new_board = []
			for row in range(10):
				new_line = ''
				for index in range(11):
					if(index == column):
						'nothing'
					elif(index == 10):
						new_line+='.'
					else:
						new_line+=board[row][index]
				new_board.append(new_line)
			board = new_board


		if(shifting == False):
			blocks_need_to_shift = False

	#print_board()

def anything_on_board():
	for x in board:
		for y in x:
			if(y!='.'):
				return True
	return False

def step_by_step_replay():
	global board
	for x in moves:
		pick_piece(x)
		#print_board()
		if(anything_on_board==False):
			break


def pick_piece(piece):
	global board
	new_board = []
	for x in range(10):
		new_line = ''
		for g in range(10):
			if((x,g) in piece):
				new_line += '.'
			else:
				new_line += board[x][g]
		new_board.append(new_line)
	board = new_board
	fall()
	shift()
	#print_board()

def play():
	global board,moves,f,possible_boards
	print len(possible_boards.keys())
	build_board()
	print_board()
	pieces = assign_pieces()
	build_string()
	possible_boards[board_as_string] = pieces
	temp_board = board
	for x in pieces[::-1]:
		board = temp_board
		won = False
		f.write('\n========================================'+str(x))
		if(len(x)>1):
			pick_piece(x)
			won = play_helper(x)
		if(won):
			board = temp_board
			print_board()
			moves.append(x)
			break
		else:
			moves = []
	board = temp_board
	#print_board()
	
	


def play_helper(piece):
	global board,moves,f
	temp_board = board
	build_string()
	pieces = []
	if(board_as_string in possible_boards):
		global total
		total +=1
		#print total
		#start = time.time()
		pieces = possible_boards[board_as_string]
		#end = time.time()
		#print "time retrieving from dictionary =",end-start
	else:
		#start = time.time()
		pieces = assign_pieces()
		possible_boards[board_as_string] = pieces
		#end = time.time()
		#print "time assigning pieces and adding to dic",end-start

	s=0
	for x in pieces:
		s+=len(x)
	if(s==0):
		return True
	if(s==len(pieces)):
		return False
	for x in pieces:
		board = temp_board
		won = False
		if(len(x)>1):
			#moves.append(x)
			pick_piece(x)
			won = play_helper(x)
		if(won):
			board = temp_board
			print_board()
			#moves.append(x)
			return True
	return False

board = []
moves = []
possible_boards = {}
board_as_string = ''
total = 0
f = open("C:\Users\groveh\Documents\Brickpop\write.txt",'w+')
if __name__ == "__main__":
	start = time.time()
	play()
	end = time.time()
	print 'Total Time:',end-start


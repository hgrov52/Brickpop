
'''
C:\Python27\python.exe C:\Users\groveh\Documents\AI_Comp\Bomberman.py
'''
import time

def print_board():
	print 
	for x in board:
		print x

def build_board():
	global board
	_file = open("C:\Users\groveh\Documents\Brickpop\Bd5.txt",'r')
	for line in _file:
		#print line
		board.append(line.strip())
		if len(board) == 10:
			break

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
	for vertical in range(10):
		for horizontal in range(10): 
			current_letter = board[vertical][horizontal]
			if(current_letter== '.'):
				continue
			current_coors = (vertical,horizontal)
			pieces.append([current_coors])
	separated_pieces = True
	while(separated_pieces):
		temp = pieces
		pieces = []
		for x in temp:
			if(x!=[]):
				pieces.append(x)
		should_delete = False
		for x in pieces:
			should_delete = False
			for y in x:
				for w in range(len(pieces)):
					if(len(pieces[w])>0 and len(x)>0 and pieces[w][0] == x[0]):
						continue
					for v in pieces[w]:
						if(next_to(y,v) and bd(y) == bd(v)):
							should_delete=True
					if(should_delete):
						for g in range(len(pieces[w])):
							x.append(pieces[w][g])
						pieces[w]= []
						break
				if(should_delete):
					break
			if(should_delete):
				break
		if(should_delete == False):
			separated_pieces = False
	'''	
	s = 0
	for x in pieces:
		print x
		s+=(len(x))

	print s
	'''
	return pieces

#return board next state after blocks fall	
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
		shifting = False
		column = -1
		for x in range(10):
			empty_column = False
			if(board[0][x] == '.'):
				empty_column = True
				for y in range(10):
					if(board[y][x] != '.'):
						empty_column = False

				if(empty_column):
					really_is_empty = True
					#see if any blocks to right of column
					for r in range(10):
						for e in range(x,10):
							if(board[r][e]!='.'):
								really_is_empty=False
					if(not really_is_empty):
						shifting = True
						column = x
						break

			if(empty_column):
				break
		if(shifting):
			new_board = []
			for row in board:
				new_line = ''
				for index in range(11):
					if(index == column):
						'nothing'
					elif(index == 10):
						new_line+='.'
					else:
						new_line+=row[index]
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
	global board,moves,f
	build_board()
	print_board()
	pieces = assign_pieces()
	temp_board = board
	for x in pieces:
		print 'new piece'
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
	pieces = assign_pieces()
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
	#print len(pieces)
	return False

board = []
moves = []
f = open("C:\Users\groveh\Documents\Brickpop\write.txt",'w+')
if __name__ == "__main__":
	
	start = time.time()
	play()
	end = time.time()
	print 'Total Time:',end-start

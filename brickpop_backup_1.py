
'''
C:\Python27\python.exe C:\Users\groveh\Documents\AI_Comp\Bomberman.py
'''


def print_board():
	print 
	for x in board:
		print x

def build_board():
	global board
	_file = open("C:\Users\groveh\Documents\Brickpop\Bd2.txt",'r')
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
		for x in pieces:
			for y in x:
				for w in range(len(pieces)):
					if(len(pieces[w])>0 and len(x)>0 and pieces[w][0] == x[0]):
						continue
					should_delete = False
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
	print '\n',len(pieces),'pieces'
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

def pick_a_piece():
	pieces = assign_pieces()
	for x in pieces:
		if(len(x)>1):
			pick_piece(x)
			break


def pick_piece(piece):
	global board
	new_board = []
	fall()
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
	print_board()

def play():

	while(can_play_this_config):
		pick_a_piece()
		print_board()

		s=0
		for x in pieces:
			s+=len(x)
		if(s==0 or s==len(pieces)):
			can_play_this_config = False

board = []
#f = open("C:\Users\groveh\Documents\Brickpop\write.txt",'w+')
if __name__ == "__main__":
	build_board()
	print_board()
	

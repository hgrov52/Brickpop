
'''
C:\Python27\python.exe C:\Users\groveh\Documents\Brickpop\brickpop.py

for practice game:
https://apps-1769985943218931.apps.fbsbx.com/instant-bundle/1016115198509508/1147233995391307/index.html?source=fbinstant-1769985943218931

'''
import time
from random import shuffle
from PIL import Image
import pyscreenshot as ImageGrab

def measure_efficiency():
	#run with Bd_measure.txt
	build_board_start = time.time()
	global board
	
	
	build_board()
	
	temp_board = board
	assign_pieces_start = time.time()
	for x in range(100):
		assign_pieces()
		print x
	fall_start = time.time()
	for x in range(100):
		board = temp_board
		fall()
	shift_start = time.time()
	for x in range(100):
		board = temp_board
		shift()
	end = time.time()
	print "build_board():",(assign_pieces_start - build_board_start)
	print "assign_pieces():",(fall_start - assign_pieces_start)
	print "fall():",(shift_start - fall_start)
	print "shift():",(end - shift_start)

def print_board():
	print 
	for x in board:
		print x

def build_board():
	global board
	'''Facebook'''
	#im=ImageGrab.grab(bbox=(735,330,1165,760))
	'''Facebook at left half'''
	#im=ImageGrab.grab(bbox=(265,345,705,760))
	'''Practice'''
	#im=ImageGrab.grab(bbox=(635,225,1290,865))
	'''Practice at left half'''
	im=ImageGrab.grab(bbox=(170,225,800,865))
	
	#im=im.resize((1000,1000))
	#im.show()
	im = im.resize((100, 100))  

	pix = im.load()
	x=5
	while(x<100):
		y=5
		line = ''
		while(y<100):
			if(pix[y,x][0] > 250):
				if(pix[y,x][2] >110 and pix[y,x][2] <120):
					line+='r'
				else:
					line+='y'
			elif(pix[y,x][0] <20):
				line+='g'
			elif(pix[y,x][0] > 75 and pix[y,x][0]<85):
				line+='b'
			elif(pix[y,x][0] >175 and pix[y,x][0]<185):
				line+='p'
			elif(pix[y,x][0] >145 and pix[y,x][0]<155):
				line+='n'
			else:
				line+='.'
			y+=10
		board.append(line)
		x+=10
	#print_board()


def bd(tuple_coor):
	return board[tuple_coor[0]][tuple_coor[1]]

def next_to(cor1,cor2):
	if(cor1[0] == cor2[0] and abs(cor1[1]-cor2[1]) == 1):
		return True
	if(cor1[1] == cor2[1] and abs(cor1[0]-cor2[0]) == 1):
		return True
	return False

def cant_win():
	color_keys = {}
	for x in board:
		for y in x:
			if y in color_keys:
				color_keys[y]+=1
			else:
				color_keys[y] = 1
	for x in color_keys:
		if color_keys[x] == 1:
			return True
	return False



def visit(x,y,piece):
	global new_board
	if(x<0 or y<0 or x>9 or y>9 or new_board[x][y][1] == True):
		return piece
	new_board[x][y] = (board[x][y],True)
	
	if(x>0 and board[x][y] == board[x-1][y]):
		piece = visit(x-1,y,piece)
	if(x<9 and board[x][y] == board[x+1][y]):
		piece = visit(x+1,y,piece)
	if(y>0 and board[x][y] == board[x][y-1]):
		piece = visit(x,y-1,piece)
	if(y<9 and board[x][y] == board[x][y+1]):
		piece = visit(x,y+1,piece)

	if(board[x][y] != '.'):
		piece.append((x,y))
	return piece

def assign_pieces_rec():
	global new_board
	new_board = []
	for x in range(10):
		new_board.append([])
		for y in range(10):
			new_board[x].append((board[x][y],False))

	pieces = []
	for x in range(10):
		for y in range(10):
			piece = visit(x,y,[])
			if(piece!=[]):
				pieces.append(piece)


	return pieces


def assign_pieces():
	start = time.time()
	return assign_pieces_rec()
	end = time.time()
	global assign_pieces_sum
	assign_pieces_time=(end-start)
	#if(assign_pieces_time!=0.0):
	assign_pieces_sum[0]+=assign_pieces_time
	assign_pieces_sum[1]+=1

#return board next state after blocks fall	
def fall():
	start = time.time()
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
	end = time.time()
	global fall_sum
	fall_time=(end-start)
	if(fall_time!=0.0):
		fall_sum[0]+=fall_time
		fall_sum[1]+=1
	#print_board()

def shift():
	start = time.time()
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
	end = time.time()
	global shift_sum
	shift_time=(end-start)
	if(shift_time!=0.0):
		shift_sum[0]+=shift_time
		shift_sum[1]+=1

	#print_board()

def anything_on_board():
	for x in board:
		for y in x:
			if(y!='.'):
				return True
	return False
def dist(x,y):
	return sqrt((abs(x[0]-y[0]))*(abs(x[0]-y[0]))+(abs(x[1]-y[1]))*(abs(x[1]-y[1])))

def single_decision():
	pieces = assign_pieces()
	colors = []
	for piece in pieces:
		if(len(piece)==1 and board[piece[0][0]][piece[0][1]] not in colors):
			colors.append(board[piece[0][0]][piece[0][1]])
		elif(board[piece[0][0]][piece[0][1]] in colors):
			colors.remove(board[piece[0][0]][piece[0][1]])
	if(len(colors)>1):
		best = 200,'.'
		for c in colors:
			single_pieces = []
			x_color_pieces = []
			for x in pieces:
				if(len(x)==1):
					single_pieces.append(x)
				if(board[piece[0][0]][piece[0][1]] == c):
					x_color_pieces.append(x)
			sum_times = [0,0]
			for single in single_pieces:
				for x in x_color_pieces:
					for cor in x:
						sum_times[0]+=dist(cor,single)
						sum_times[1]+=1
			if(sum_times[0]/sum_times[1]<best):
				best = sum_times[0]/sum_times[1],c
		print "remove",c,"blocks please, then retry "

		#which color is best
	if(len(colors)==1):
		return "remove",board[piece[0][0]][piece[0][1]],"blocks please, then retry"
	






def step_by_step_replay():
	global board
	for x in moves:
		pick_piece(x)
		#print_board()
		if(anything_on_board==False):
			break

def pick_winning_piece(piece):
	global board,f
	for x in range(10):
		new_line = ''
		for g in range(10):
			if((x,g) in piece):
				new_line += '#'
			else:
				new_line += board[x][g]
		print new_line
		f.write('\n'+str(new_line))
	f.write('\n')
	print 



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
	global board,moves,f,estop
	build_board()
	print_board()
	temp_board = board
	pieces = assign_pieces()
	shuffle(pieces)
	estop[0] = time.time()
	for x in pieces:
		print 'new piece'
		if(estop[1]-estop[0]>.3):
			print 'ebrake'
			return False
		board = temp_board
		won = False
		f.write('\n========================================'+str(x))
		if(len(x)>1):
			pick_piece(x)
			won = play_helper(x)
		if(won):
			board = temp_board
			#print_board()
			moves.append(x)
			break
		else:
			moves = []
	board = temp_board

	#print_board()
	
	


def play_helper(piece):
	global board,moves,f,estop
	temp_board = board
	pieces = assign_pieces()
	shuffle(pieces)
	estop[1] = time.time()
	if(estop[1]-estop[0]>.3):
		print 'ebrake'
		return False
	s=0
	for x in pieces:
		s+=len(x)
	if(s==0):
		return True
	if(s==len(pieces)):
		return False
	for x in pieces:
		if(cant_win()):
			continue
		board = temp_board
		won = False
		if(len(x)>1):
			pick_piece(x)
			won = play_helper(x)
		if(won):
			board = temp_board
			#print_board()
			moves.append(x)
			return True
	#print len(pieces)
	return False

board = []
moves = []
new_board = []
estop = [0,0]
fall_sum,shift_sum,assign_pieces_sum = [0,0],[0,0],[0,0]
f = open("C:\Users\groveh\Documents\Brickpop\write.txt",'w+')
if __name__ == "__main__":
	

	start = time.time()
	finished = play()
	if(finished == False):
		single_decision()
	end = time.time()
	print 'Total Time:',end-start
	
	print moves
	print_board()
	print 
	if(finished == True and len(moves)==0):
		print "CANNOT BE SOLVED"
	for x in moves[::-1]:
		pick_winning_piece(x)
		pick_piece(x)
	print 'Total Time:',end-start

	'''

	global shift_sum,fall_sum
	print "Avg Fall:",fall_sum[0]/fall_sum[1],"over",fall_sum[1],"times"
	print "Avg shift:",shift_sum[0]/shift_sum[1],"over",shift_sum[1],"times"
	print "Avg assign_pieces:",assign_pieces_sum[0]/assign_pieces_sum[1],"over",assign_pieces_sum[1],"times"
	'''

'''
C:\Python27\python.exe C:\Users\groveh\Documents\Brickpop\brickpop.py

for practice game:
https://apps-1769985943218931.apps.fbsbx.com/instant-bundle/1016115198509508/1147233995391307/index.html?source=fbinstant-1769985943218931

'''
import time
from random import shuffle
from PIL import Image
from PIL import ImageGrab
import multiprocessing
import pyautogui

def measure_efficiency():
	#run with Bd_measure.txt
	build_board_start = time.time()
	global board
	
	
	build_board(True)
	
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

def build_board(full):
	global board

	partial_board = []
	'''Facebook'''
	im=ImageGrab.grab(bbox=(720,345,1180,805))
	'''Facebook at left half'''
	#im=ImageGrab.grab(bbox=(245,360,705,755))
	'''Practice'''
	#im=ImageGrab.grab(bbox=(635,225,1290,895))
	'''Practice at left half'''
	#im=ImageGrab.grab(bbox=(150,250,810,910))
	
	
	im.show()
	#im = Image.open('C:\Users\groveh\Documents\Brickpop\image2.png')
	#im.show()
	im = im.resize((100, 100))  
	#im.show()
	pix = im.load()
	x=5
	while(x<100):
		y=5
		line =''
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
		if(full==False):
			partial_board.append(line)
		else:
			board.append(line)
		x+=10

	if(full):
		for x in board:
			for y in x:
				if(y=='.'):
					print_board()
					raise Exception("Build Failed")
	else:
		return partial_board

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
	return assign_pieces_rec()
	
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

def anything_on_board():
	for x in board:
		for y in x:
			if(y!='.'):
				return True
	return False
def dist(x,y):
	return sqrt((abs(x[0]-y[0]))*(abs(x[0]-y[0]))+(abs(x[1]-y[1]))*(abs(x[1]-y[1])))



def step_by_step_replay():
	global board
	for x in moves:
		pick_piece(x)
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
'''
def solve():
	queue = multiprocessing.Queue()
	processes = [
		multiprocessing.Process(target=play_helper,args=(piece))
		for piece in assign_pieces()
	]

	for p in processes:
		p.start()

	found = False
	while(True):
		print queue.get()
'''



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

def play():
	global board,moves,f,estop,solution_score

	temp_board = board
	pieces = assign_pieces()
	shuffle(pieces)
	estop[0] = time.time()
	for x in pieces:
		#print 'new piece'
		if(estop[1]-estop[0]>5):
			#print 'ebrake'
			return False
		board = temp_board
		won = False
		f.write('\n========================================'+str(x))
		if(len(x)>1):
			pick_piece(x)
			won = play_helper(x)
		if(won):
			board = temp_board
			moves.append(x)
			solution_score+= len(x)*len(x)-len(x)
			return True
		else:
			moves = []
	board = temp_board

	
	


def play_helper(piece):
	global board,moves,f,estop,solution_score
	temp_board = board
	pieces = assign_pieces()
	shuffle(pieces)
	estop[1] = time.time()
	if(estop[1]-estop[0]>5):
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

			moves.append(x)
			solution_score+= len(x)*len(x)-len(x)
			return True
	return False

def check():
	partial_board = build_board(False)
	
	
	if(board!=partial_board):
		

		for y in partial_board:
			print y
		print
		print_board()
		raise Exception("Something went wrong")


def automate(moves):
	width, height = pyautogui.size()
	print (width,height)
	practice_l=(150,250,810,910)
	real_l=(245,360,705,760)
	real=(720,345,1180,805)

	box_l = real

	x_range = box_l[2]-box_l[0]
	y_range = box_l[3]-box_l[1]

	if(len(moves)==0):
		raise Exception("CANNOT BE SOLVED")
	print_board()
	print
	for piece in moves[::-1]:
		
		pick_winning_piece(piece)
		coor=piece[0]
		print '\n',(coor[0],coor[1])
		pyautogui.moveTo((coor[1])*y_range/9+box_l[0]+(10-2*coor[1]),(coor[0])*x_range/9+box_l[1]+(10-2*coor[0]),duration=2)
		
		pyautogui.click()
		check()

		

		pick_piece(piece)
		




pyautogui.FAILSAFE=True
pyautogui.PAUSE=0
board = []
moves = []
new_board = []
estop = [0,0]
solution_score = 0

f = open("C:\Users\groveh\Documents\Brickpop\write.txt",'w+')
if __name__ == "__main__":
	
	while(True):
		board = []
		new_board = []
		solutions = []

		finished = False
		start = time.time()
		global estop,solution_score
		analyzing_time_start = time.time()
		analyzing_time_end = time.time()
		security_counter = 0

		build_board(True)
		print_board()
		while(analyzing_time_end-analyzing_time_start<5 or len(solutions)==0):
			analyzing_time_broken = time.time()
			print 'analyzing...',analyzing_time_end-analyzing_time_start
			if(analyzing_time_end-analyzing_time_start>25):
				raise Exception("Dont know why this happens.. Try again")
			estop = [0,0]
			moves = []
			solution_score = 0
			finished = play()
			if(finished==True):
				print "found a solution -",solution_score
				solutions.append((moves,solution_score))
			analyzing_time_end = time.time()
			if(analyzing_time_end - analyzing_time_broken<.1):
				security_counter+=1
				if(security_counter>100):
					raise Exception("broken")

		best = 0,0
		for x in solutions:
			if(x[1]>best[1]):
				best = x
		moves = best[0]		
		print 
		
		automate(moves)
		print "waiting for title screen..."
		temp_time_s=time.time()
		temp_time_e=time.time()
		while(temp_time_e-temp_time_s<10):
			temp_time_e=time.time()
	
		

'''
score = len(piece)*len(piece)-len(piece)

'''
	
	

	
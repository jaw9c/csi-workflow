from clint.textui import prompt
from trello import TrelloClient
from config import TRELLO_API_KEY, TRELLO_API_SECRET
from clint.textui import colored, puts
import config 
class doit:
	board_id = config.BOARD_ID

	def intialise_trello(self): 
		self.trello_client = TrelloClient(
			api_key=TRELLO_API_KEY,
			api_secret=TRELLO_API_SECRET
		)

	def get_board(self):
		boards = self.trello_client.list_boards()
		for i in range(len(boards)):
			print(str(i) + ': ' + boards[i].name)
		done = False 
		while not done:
			board_number = int(prompt.query('Board number: '))
			puts(colored.yellow('Confirm board: ' + boards[board_number].name))
			if prompt.query('Confirm: y/n: ') == 'y':
				self.board = boards[board_number]
				self.board_id = self.board.id
				puts(colored.green(self.board.name + ' confimed'))
				done = True
	
	def get_ticket_number(self):
		ticket_number = prompt.query('Ticket Number: ') 
		puts(colored.yellow('Confirm ticket #' + str(ticket_number)))
		if prompt.query('Confirm: y/n: ') == 'y':
			self.ticket_number = ticket_number
			puts(colored.green('#' + str(ticket_number) + ' confirmed!'))
		else: 
			self.get_ticket_number()

	def get_trello_board(self):
		print('hi')


	def do(self):
		self.intialise_trello()
		self.get_board()

maindo = doit()
maindo.do()


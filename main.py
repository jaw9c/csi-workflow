from clint.textui import prompt
from trello import TrelloClient
from config import TRELLO_API_KEY, TRELLO_API_SECRET
from clint.textui import colored, puts
import config
import subprocess
import os

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
			self.ticket_number = int(ticket_number)
			puts(colored.green('#' + str(ticket_number) + ' confirmed!'))
		else: 
			self.get_ticket_number()

	def get_trello_board(self):
		print('hi')

	def send_pr(self, pr_title):
		os.system("git pr")
 
	def get_card(self):
		for card in self.trello_client.get_list(config.BACKLOG_LIST_ID).list_cards():
			if card.short_id == self.ticket_number:
				self.card = card
				self.card_title = card.name.split(") ", 1)[1] 
				return
		puts(colored.red('Card not found in backlog with number: #' + str(self.ticket_number)))
	def process(self): 
		for i in range(len(config.PROCESS_LIST_IDS[1:])):
			list = self.trello_client.get_list(config.PROCESS_LIST_IDS[i+1])
			input = prompt.query('Move to: ' + list.name + '? y/n')
			if input == 'y':
				self.card.change_list(list.id)
				self.card.set_pos('bottom')
				puts(colored.green('Moved!'))
				if list.id == config.PR_LIST_ID:
					puts(colored.yellow('Submitting PR'))
					self.pull_request()
					puts(colored.green('Submitted!')) 
	def pull_request(self):
		os.system("git push")
		master_command = "hub pull-request -m \"" + self.card_title + "\" -h `git rev-parse --abbrev-ref HEAD` -b master -l \"master\""
		staging_command = "hub pull-request -m \"" + self.card_title + "\" -h `git rev-parse --abbrev-ref HEAD` -b staging -l \"staging\"" 

		master = subprocess.check_output(master_command, shell=True)
		staging = subprocess.check_output(staging_command, shell=True)

		self.master_pr = str(master)[2:].split("\\")[0]
		self.staging_pr = str(staging)[2:].split("\\")[0]
		
		puts(colored.green('Master link: ' + self.master_pr))
		puts(colored.green('Staging link: ' + self.staging_pr))
			
	
	def do(self):
		self.intialise_trello()
		self.get_ticket_number()
		self.get_card()
		self.process()

maindo = doit()
maindo.do()


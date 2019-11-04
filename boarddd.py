class Board:
#Note1:
#ban co bieu dien bang mang 1 chieu nhu sau
# Player 1 side:
#	|| slot[11](slot quan) || slot[10] | slot[9] | slot[8] | slot[7] | slot[6] |                    
#                           | slot[0]  | slot[1] | slot[2] | slot[3] | slot[4] || slot[5](slot quan) ||
#Player 2 side:
#Note2:
#slot quan bieu dien nhu sau: quan* dan 
#   VD: 0* 6 la khong co quan va co 6 dan 
#       1* 2 la co 1 quan va 2 dan
#Note3: rai soi theo 2 huong
#	huong +1: theo chieu tang slot index
#   huong -1: theo chieu giam slot index
	def __init__(self):
		self.dan  =  [5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 0] # luu so dan tung o 
		self.quan =  [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0] # luu so quan
		self.move_num = 0                                 # count number of turns
		self.diemdan = [0, 0] 							  # so dan an duoc of 2 players
		self.diemquan = [0, 0]							  # so quan an duoc of 2 players
		self.vay = [0, 0]								  # so lan vay quan of 2 players

	@property
	def diem(self): # so dan quy doi of 2 players
		return [x + 5 * y for x, y in zip(self.diemdan, self.diemquan)] # dan quy doi = dan + quan * 5
	def score(self): #so diem (tinh ca vay) of 2 players
		return [self.diem[i] - self.vay[i] * 5 + self.vay[(i+1)%2] * 5] # diem = dan - đi vay * 5 + cho vay * 5 
	def __repr__(self): #show state of board & players
		layout = '--------------'+ str(self.move_num) + '---------------\n'	
		layout += 'P1: ' + str(self.diem[1]) + '      4 <-- 0   \n       |'
		layout += str(self.quan[11]) + '* ' + str(self.dan[11]) + '|'
		for p in reversed(self.dan[6: 11]):
			layout += str(p) + ' '
		layout += '|                    \n\n            |'
		for p in self.dan[0:5]:
			layout += str(p) + ' '
		layout += '|' + str(self.quan[5]) + '* ' + str(self.dan[5]) 
		layout += '|\n         0 --> 4      P0: ' + str(self.diem[0]) + '\n--------------------------------'	
		return layout

	def empty(self, slot): #kiem tra slot empty
		if self.dan[slot] > 0 or self.quan[slot] > 0:
			return 0
		return 1

	def distributecheck(self, slot, direction): #kiem tra xem co rai soi nextslot theo luat duoc khong
		nextslot = (slot + direction)%12
		if not (nextslot % 6 == 5) and not self.empty(nextslot):
			return 1
		return 0

	def distribute(self, slot, direction): #rai soi theo luat
		hand = self.dan[slot]
		self.dan[slot] = 0
		while hand:
			slot = (slot + direction)%12
			self.dan[slot] += 1
			hand -= 1
		return slot

	def capturecheck(self, slot, direction): #kiem tra xem co an slot theo luat duoc khong
		nextslot = (slot + direction)%12
		nextnextslot = (nextslot + direction)%12
		if (self.empty(nextslot) and not self.empty(nextnextslot)):
			return 1
		return 0

	def capture(self, slot, player): #an slot theo luat
		self.diemdan[player] += self.dan[slot] 
		self.diemquan[player] += self.quan[slot] 
		self.dan[slot] = 0
		self.quan[slot] = 0

	def emptysidecheck(self, player): #kiem tra het quan tai ca 5 o phia player
		for i in range(5):
			if(self.dan[i + player * 6]):
				return 0
		return 1
	def emptyside(self, player): #lay 5 dan da an de rai cho 5 o trong / vay 5 quan de rai cho 5 o trong/ neu khong vay duoc coi nhu het luot
		print(self)
		print('P' + str(player) + ' het quan')
		if self.diemdan[player] >= 5:
			print('Lay quan P' + str(player))
			self.diemdan[player] -= 5
			for i in range(5):
				self.dan[i + player * 6] = 1
		elif self.diemdan[(player+1)%2] >= 5:
			print('Vay quan P' + str((player+1)%2))
			self.diemdan[(player+1)%2] -= 5
			for i in range(5):
				self.dan[i + player * 6] = 1
			self.vay[player] += 1
	def hetquantanquancheck(self): #kiem tra "het quan, tan quan" 
		if self.quan[5] > 0 or self.quan[11] > 0 or self.dan[5] and self.quan[5]==0:
			return 1
		return 0
	def hetquantanquan(self): #thuc hien het quan, tan quan, chia dan cho  2 ben
			print('Het quan tan quan')
			for i in range(5):
				self.diemdan[0] += self.dan[i + 0 * 6]
				self.diemdan[1] += self.dan[i + 1 * 6]
			for i in range(12):
				self.dan[i] = 0
			print(self)

	def move(self, player, slot, direction): #mot luot choi, nhan tham so: o bat dau (0->5), huong di(+1, -1)
		print('player: {}, slot {}, direction {}'.format(player,slot,direction))
		slot = slot + player * 6
		slot = self.distribute(slot, direction)      # rai het soi tu 1 o
		while self.distributecheck(slot, direction): # rai tiep soi
			slot = (slot + direction)%12
			slot = self.distribute(slot, direction)
		while self.capturecheck(slot, direction):	 # an soi (co the tu nhieu o)
			slot = (slot + 2 * direction)%12
			self.capture(slot, player)               # an soi tu 1 o
			if self.hetquantanquancheck():           #sau moi luot an, kiem tra het quan tan quan
				self.hetquantanquan()
				return 
		self.move_num += 1
		if self.emptysidecheck((player+1)%2):        #truoc khi ket thuc luot, kiem tra opponent co het soi ca 5 slots khong
			self.emptyside((player+1)%2)
		print(self)

game = Board()
print(game)
# player = int(input())
# slot = int(input())
# direction = int(input())

game.move(0, 2, 1) #player 1 di nuoc boc soi slot 2 va rai sang phai
#game.move(0, 2, 1)
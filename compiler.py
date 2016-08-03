import string
from collections import OrderedDict
from copy import deepcopy
position = 1
state_list_goto = []
finalstates = OrderedDict()
list_of_parse_table =[]
checking_final_state=OrderedDict()
map_Reduce = [OrderedDict([('Sp', ['S.'])]),OrderedDict([('S', ['CC.'])]),OrderedDict([('C', ['cC.'])]),OrderedDict([('C', ['d.'])])]
#this first contains 2 functions is_terminal and compute_follow
#here going to compute first set
grammer = OrderedDict([('S',['CC']),('C',['cC', 'd']) ])
# OrderedDict([('He', True), ('will', True), ('be', True), ('the', True), ('winner', True)])
augmented_grammer = OrderedDict([('Sp',['S']),('S',['CC']),('C',['cC', 'd'])])
augmented_grammer1 = {'Sp':['S'],'S':['CC'],'C':['cC','d']}
def is_terminal(character):
	#check if input character is smaller letter of not
	if character in ['a','b','c','d','$']:
		return True
	else:
		return False
def compute_first(X): # computing first for the grammar
	first = []
	
	if X=="":
		return X
	if is_terminal(X[0]):
			
			first.append(X[0])
			return first
	# print X
	for i in grammer[X[0]]:
		# print i
		next_term = i[0]
		if is_terminal(next_term):
			# print "here"
			if not(next_term in first):
				first.append(next_term)
		
		else:
			compute_first(next_term)
	return first

def compute_follow(X): #calculating follow ..not required in our case
	follow = []
	if X == "S":
		follow.append('$')
		return follow
	for j in grammer.keys():
		for i in grammer[j]:		
			if X in i:
				#X vetyo yaha vitra cha
				# print X, i.index(X), len(i)
				if i.index(X)==len(i)-1:
					# print "lst"
					temp_follow = compute_follow(j)
					# print temp_follow
					for k in temp_follow:
						if not(k in follow):
							follow.append(k)
				
					continue
				temp_first = compute_first(i[i.index(X)+1])				
				
				for k in temp_first:
					if not ( k in follow):
						follow.append(k)
	return follow

# 5 february 2016
# now what we are going to do is compute a closure
def add_dot(): #adding the dots in AG 
	#here going to add a dot in augmented grammer
	#yo keys ko order le garnu garyo
	for j in augmented_grammer.keys():
		for i in range(0,len(augmented_grammer[j])):
			augmented_grammer[j][i] = "." + augmented_grammer[j][i] 

def is_final(statement): #checking if the state is final one 
	for key,value in statement.iteritems():
			if type(value) == type([]):
				for i in value:
					dot_index = i.index('.')
				if dot_index == len(i) -1:
					return True 
			else:		
				dot_index = value.index('.')
				if dot_index == len(value)-1 :
					#the dot is in final position
					 return True
	return False
def compute_lookahead(statement,purano_lookahead=None): #return lookahead for state
	#find dot value and then first of the rest of the part is the item set
	prev_value=[]
	lookahead=[]	
	lookahead_dict = OrderedDict()
	prev_lookahead = None
	for key,value in statement.iteritems():
		lookahead_dict[key] = [[],[]]
		lookahead= []
		for i in value:

			#key ko previous position nikanle
			if key == "Sp":
				lookahead.append("$")
				lookahead_dict[key]=[[i],lookahead]
				prev_lookahead = lookahead
				
				continue
			else:
				#here key is not Sp vanepachi prevLoop ko value huncha
				if not(purano_lookahead == None):
					
					lookahead = purano_lookahead
					# lookahead_dict[key]=[[i],lookahead]
					lookahead_dict[key] = [value,lookahead]
					# lookahead_dict[key][0].append(value)
					# lookahead_dict[key][1].append(lookahead)
					prev_lookahead = lookahead
					purano_lookahead = None
					
				for j in prev_value:
					
					j = j[j.index('.')+1:]
				
					if key in j:
						#ket is same so 2 times printed autai ho
						
						new_look = ""
						for look in prev_lookahead:
							new_look = new_look + look
						# print compute_first(j[j.index(key)+1:]+new_look)
						lookahead = compute_first(j[j.index(key)+1:]+new_look)
						# print "keys" + str(lookahead_dict.keys())
						# lookahead_dict[key][0]value
						lookahead_dict[key][0].append(i)
						lookahead_dict[key][1]=lookahead
						# print lookahead_dict
				prev_lookahead = lookahead
			
		prev_value = value
	return lookahead_dict,lookahead		

def characters_after_dot(statement): #return the first character after dots 
	characters = []
	for key,value in statement.iteritems():
		if type(value) == type([]): 
			for i in value:
				# print i
				dot_index = i.index('.')
				if(dot_index == len(i)-1):
					characters = []
					return characters
				characters.append(i[dot_index+1])
		else:
			characters.append(value[value.index('.')+1])
	return characters

def get_look_aheads(statement,cad): #return lookahead
	character_lookahead_dict = OrderedDict()
	# print cad
	# print statement
	for key, value in statement.iteritems():
		#this value is in from of [[],[]] where second one is lookaheads
		
		for i in value[0]:
			

			dot_index = i.index('.')
			if dot_index == len(i) -1 :
				return character_lookahead_dict
			for j in cad:
				if i[dot_index+1] == j:
					#it matches now get the lookahead for this key and pair it with the character OK!!!
					character_lookahead_dict[j]=value[1]
	
	return character_lookahead_dict		
	
def compute_closure(given_statement,given_character):  
	#should shift the . 1 position
	#along with the shifted output return also the ones after dot
	
	for key, value in given_statement.iteritems():
		# print value
		#swap value[0][dot_index] and value[0][dot_index+1]
		
		for i in value:
			dot_index = i.index('.')
			
			# print given_character
			# print dot_index
			if (i[dot_index+1] == given_character):
				# print "yes"
				break
		else:
			continue
				
		i= i[:dot_index]+i[dot_index+1]+i[dot_index]+i[dot_index+2:]
		dot_index = dot_index +1  
		diction = OrderedDict()
		diction[key] = [i]
		if is_final(diction):
			#final ko case ma send a final tag to denote
			#now here should compute the lr1 item set and return
			
			return diction, "final"
		
		if not(is_terminal(i[dot_index+1])):
			
			# print i ,dot_index
			#esma after the . operation not terminal
			#now add the derivatives of nonterminal one
			# print value, dot_index,key
			diction[key] = [i]
			if value[0][dot_index+1]==key:
				for l in augmented_grammer[key]:
					diction[key].append(l)				 
			else:	
				diction[value[0][dot_index+1]]=augmented_grammer[value[0][dot_index+1]]				 
			# print diction
			return diction, characters_after_dot(diction)
						 	 	 
		else:
			return diction,[value[0][dot_index+1]]
		
def create_goto(): # creating goto for the state
	global position
	#here we are going to create a goto table
	#for that first we are going create a closure for grammer S : .S'
	add_dot()
	states = []
	states_with_lookahead = []
	toGoto = []
	character_lookahead_pairs = []
	# compute_lookahead(deepcopy(augmented_grammer))
	# compute_lookahead(OrderedDict([('S', ['C.C']),('C', ['c.C','.d'])]),['$'])
	# compute_lookahead(OrderedDict([('S', ['S.'])]),['$'])
	# od = OrderedDict([('C', ['c.C', '.cC', '.d'])])
	# return 
	states.append(deepcopy(augmented_grammer))	
	
	toGoto.append(characters_after_dot(deepcopy(augmented_grammer)))
	d1,d2=compute_lookahead(states[0])
	states_with_lookahead.append(d1)
	character_lookahead_pairs.append(get_look_aheads(states_with_lookahead[0],toGoto[0]))
	#characters_after_dot(augmented_grammer) use these keys to map with look aheads
	print "Grammar"
	print "S -> .CC"
	print "C -> .cC"
	print "C -> .d"
	print
	print
	print "state[",position-1,"]",states_with_lookahead
	
	# print toGoto
	marker = 0
	for key,i in enumerate(states):
		marker = marker+1
			
		# print key,i
		if(is_final(i)):
			continue
		lookahead_pair = character_lookahead_pairs[marker-1]	
		j = toGoto[key]
		
		
		for k in j:
			# print i , k	
			state,toGoto_value = compute_closure(deepcopy(i),k)
			# print lookahead_pair
			state_with_lookahead,dummy_lookahead = compute_lookahead(state,lookahead_pair[k])
			#yo state ko chahi computelookahead garera
			if not(state_with_lookahead in states_with_lookahead):
                                
				
				#print "state[",position-1,"]",states_with_lookahead
                                                     
				print
				print
				                            	
				key1 =[]
				key1.append(key)
				key1.append(k)
				key1.append(position)
				print "key:",key
				print "goto:",k
				state_list_goto.append(key1)
				print "State[",position,"]" , state_with_lookahead,toGoto_value, lookahead_pair[k]	

				
				position = position + 1
				states.append(deepcopy(state))
				states_with_lookahead.append(deepcopy(state_with_lookahead))
				toGoto.append(deepcopy(toGoto_value))
				character_lookahead_pairs.append(get_look_aheads(state_with_lookahead,toGoto_value))
				if toGoto_value == "final":
					# checking_final_state.append(position-1)
					checking_final_state[position-1] = dummy_lookahead
					#print "final state ",state_with_lookahead
					finalstates[position-1] = deepcopy(state)
			else:
				indexing = states_with_lookahead.index(state_with_lookahead)
				
				key1 =[]
				key1.append(key)
				key1.append(k)
				key1.append(indexing)
				print
				print
				
				print "key:",key
				print "goto:",k
				print "state already present"
				print "previous indexing",indexing
				
				state_list_goto.append(key1)
			#yesma pass garne look ahead kasari rakhne
			#print "returned" , state_with_lookahead,toGoto_value, lookahead_pair[k]
			
	# print augmented_grammer
	# print compute_closure(augmented_grammer,'c')			
	# # print augmented_grammer
	# print compute_closure(augmented_grammer)
	# print compute_closure(OrderedDict([('S',['.dAaB'])]))


create_goto()
print
print
print "state_list_goto:",state_list_goto
print
print "final state",finalstates
print
print "checking final state",checking_final_state
print

print "Parsing Table"
print
print " State           Action             Goto"
print
print "         c        d         $           S         C "
x =['c','d','$','S','C']
dic ={}

for i in state_list_goto: #this loop append all the final state iteritems
	if (dic.has_key(i[2])):
		hello = []
		hello.append(i[0])
		hello.append(i[1])
		dic[i[2]].append(hello)

	else:
		hello = []
		hello.append(i[0])
		hello.append(i[1])
		dic[i[2]]=[hello]

for i in range(0,10): #creating parse table 
    

	print i,

	for j in x:
		boolean = True
		print "     ",
	
		if i in checking_final_state.keys():

			# for j in checking_final_state[i]:
			# 	print i,j,"=R",i
			
			
			if j in checking_final_state[i]:
				if [i,j]== [1,'$']:
					
					print "acc",
				else:
					print "R",map_Reduce.index(finalstates[i])+1,
					dummy = 'R' + str(map_Reduce.index(finalstates[i])+1)
					list_of_parse_table.append([str(i)+str(j),dummy])
			else:
				print " --",
		else:
			for key,value in dic.iteritems():
				
				# print "[i,j]",i,j
				if ([i,j]in value):
					if not(is_terminal(j)):
						boolean = False
						print key,
						list_of_parse_table.append([str(i)+str(j),key])
					else:
						boolean = False
						print "S",key,
						dummy = 'S' + str(key)
						list_of_parse_table.append([str(i)+str(j),dummy])		
				
			if boolean == True:
				print "--  ",

	print 
print
# print "dictionary:",dic
# print "AG:",augmented_grammer
# print
# print "index",map_Reduce.index(finalstates[1])
# print "index",map_Reduce.index(finalstates[4])




# print "list_of_parse_table",list_of_parse_table

def get_action (combination): #return action for the command
	for i in range(0,len(list_of_parse_table)) :
		# print "list",list_of_parse_table[i][0]
		if list_of_parse_table[i][0]== combination :
			# print "action:",list_of_parse_table[i][1]
			return list_of_parse_table[i][1]
		



def index_of_rule(number): #returns production 
	rule_no = 0
	for A, productions in augmented_grammer.iteritems():
		for production in productions:
			rule_no += 1
			if rule_no == number:
				return A,production

				
			
			
			
		
		
		
		
# print "index_of_rule",index_of_rule(4)			


stack = ['0']
#input_text =['c','d','d','$']
input_text = list(raw_input("Enter string: "))
input_text.append('$')
print "Given String :",input_text
print "%-30s " %("Simulation for given string")

while not(str(stack[-1])+str(input_text[0])=='1$'): ##creating the simulation loop
	# print "str('0')+input_text[0]",str('0')+input_text[0]
	# print "get_action(str('0')+input_text[0][0]:",get_action(str('0')+input_text[0])
	# print "action:",get_action(str(stack[-1])+str(input_text[0]))
	# print "Combination of stck and input",str(stack[-1]),str(input_text[0])
	print "Action:",get_action(str(stack[-1])+str(input_text[0])[0])
	if (get_action(str(stack[-1])+str(input_text[0])[0])[0] == 'S'):
		# print "appender",get_action(str(stack[-1])+str(input_text[0])[0])[1]
		appender = get_action(str(stack[-1])+str(input_text[0])[0])[1]
		stack.append(input_text[0])
		stack.append(str(appender))
		input_text.pop(0)
		print "%-30s %-30s" %(stack,input_text),
		# print "stack:",stack,"        ",
		# print "input:",input_text,"        ",
	elif (get_action(str(stack[-1])+str(input_text[0]))[0] == 'R'):
		
		remover= []
		A = index_of_rule(int(get_action(str(stack[-1])+str(input_text[0]))[1]))[0]
		B =index_of_rule(int(get_action(str(stack[-1])+str(input_text[0]))[1]))[1]
		B_determinant = (len(B)-1)
		# print "A:",A
		# print "B:",B
		# print "B_determinant:",B_determinant
		stack = stack[:len(stack)-B_determinant*2]
		# print "stack after reduction :",stack
		S_dash = stack[-1]
		# print "S_dash",S_dash
		stack.append(A)
		# print "append c:",stack
		# print "combo",get_action(str(S_dash)+str(A))
		stack.append(get_action(str(S_dash)+str(A)))
		print "%-30s %-30s" %(stack,input_text),
		# print "stack:",stack,"        ",
		# print "input:",input_text,"        ",
		# input_text.pop(0

else:
	print "Accepted"




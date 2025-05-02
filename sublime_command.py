import sublime
import sublime_plugin

def remove_element(target_array,list_value):
	for index, value in enumerate(target_array):
		if value in list_value:
			target_array.pop(index)
			# break
	return target_array

def loop_select_word(view):
	for p in view.sel():
		word = view.word(p)
		if word and (p.begin() == p.end()) :
			if p.contains(word):
				return
			a = word.begin()
			b = word.end()
			view.sel().add( sublime.Region( a,b ) )
			view.show( first_selection )

def isAfter( a, b ):
	return a.begin() > b.begin()

# Default (Windows).sublime-keymap
# { "keys": ["ctrl+d"], "command": "select_next_variable" },

class select_next_variable(sublime_plugin.TextCommand):
	def run(self,edit):
		not_a_variable = False #
		no_selection = False
		string_scope = False
		view = sublime.active_window().active_view()
		list_variables = view.find_by_selector("variable")
		str_variables = map( lambda x: view.substr(x), view.find_by_selector("variable") ) # list_variables muted by "remove_element"
		first_selection = view.sel()[-1]
		current_selection = { "text": view.substr(first_selection) }
		slice_selection = remove_element( list_variables , view.sel() )
		scope = view.scope_name( first_selection.begin() )

		loop_select_word(view)

		# h = list(map( lambda x : { "text": view.substr(x), "position":x } , slice_selection ))
		# h = list(filter( lambda x: x["text"] == current_selection["text"], h ))
		# if( len(h) != 0 ):
		# 	h.pop(0)
		# print( current_selection["text"], first_selection )
		# print(*h,sep="\n")

		# if( len( view.sel() ) > 1 ):
		# 	print("multi-selection")
		# 	if "string" in view.scope_name( view.sel()[0].begin() ):
		# 		print("in a string scope")
		# 	else:
		# 		print("not in a string scope")

		if( ( first_selection.begin() == first_selection.end() ) and len(view.sel()) == 1 ):
			no_selection = True

		if not current_selection["text"] in str_variables :
			not_a_variable = True

		if "string" in scope:
			not_a_variable = True

		if not_a_variable :
			# print( "Not a variable" )
			next_position = view.find( current_selection["text"], first_selection.end() )
			if next_position.begin() == -1:
				return
			# if next_position in list_variables:
			# 	return
			a = next_position.begin()
			b = next_position.end()
			view.sel().add( sublime.Region( a,b ) )
			view.show( first_selection )
			return

		# print( "Is a variable", current_selection["text"], first_selection )
		# print( *str_variables )
		# print( *slice_selection )
		# print( *list(filter( lambda x: x == current_selection["text"], str_variables )) )

		for object_position in slice_selection:
			text = view.substr(object_position)
			if ( current_selection["text"] == text and isAfter( object_position , first_selection ) ):
				a = object_position.begin()
				b = object_position.end()
				view.sel().add( sublime.Region( a,b ) )
				view.show( object_position )
				break

# { "keys": ["è"], "command": "add_backtick" },

class add_backtick(sublime_plugin.TextCommand):
	def run(self,edit):
		view = sublime.active_window().active_view()
		first_selection = view.sel()[0]
		a = first_selection.begin()
		b = first_selection.end()
		self.view.insert( edit, a , "`" )
		self.view.insert( edit, b+1 , "`" )

"""

# def get_command_name(caption):
# 	commands = sublime.load_resource("Packages/User/Default.sublime-commands")
# 	commands = sublime.decode_value(commands)
# 	return commands
# 	for command in commands:
# 		if command["caption"] == caption:
# 			return command["command"]
# 	return None

# class HelloWorldCommand(sublime_plugin.TextCommand):
# 	def run(self, edit):
# 		caption = "[RegReplace] Format : Space arround parenthesis and brackets"
# 		command_name = get_command_name(caption)
# 		if command_name:
# 			sublime.active_window().run_command( command_name[0]["command"] , command_name[0]["args"] )
# 			self.view.insert( edit, self.view.sel()[0].begin(), "hello world" )

"""

# class HelloWorldCommand(sublime_plugin.TextCommand):
# 	def run(self, edit):
# 		self.view.insert(edit, self.view.sel()[0].begin(), "hello world")

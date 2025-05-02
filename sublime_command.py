import sublime
import sublime_plugin

def remove_element(target_array,list_value):
	for index, value in enumerate(target_array):
		if value in list_value:
			target_array.pop(index)
			# break
	return target_array

def find_closest_variable(cursor_position,variables):
	closest_variable = None
	closest_distance = float("inf")

	for variable in variables:
		variable_position = variable.begin()
		distance = abs( cursor_position - variable_position )
		if distance < closest_distance:
			closest_variable = variable
			closest_distance = distance

	return closest_variable

# Default (Windows).sublime-keymap
# { "keys": ["ctrl+d"], "command": "select_next_variable" },

class select_next_variable(sublime_plugin.TextCommand):
	def run(self,edit):
		view = sublime.active_window().active_view()
		list_variables = view.find_by_selector("variable")
		str_variables = map( lambda x: view.substr(x), view.find_by_selector("variable") ) # list_variables muted by "remove_element"
		first_selection = view.sel()[-1]
		current_selection = { "text": view.substr(first_selection) }
		slice_selection = remove_element( list_variables , view.sel() )
		print( *view.sel() )

		if( first_selection.begin() == first_selection.end() ):
			print("No selection")
			cursor_position = first_selection.begin()
			closest = find_closest_variable(cursor_position,list_variables)
			print( closest )
			a = closest.begin()
			b = closest.end()
			view.sel().add( sublime.Region( a,b ) )
			view.show( first_selection )
			return

		if not current_selection["text"] in str_variables :
			print( "Not a variable", current_selection["text"] )
			next_position = view.find( current_selection["text"], first_selection.end() )
			if next_position.begin() == -1:
				return
			print( next_position )
			a = next_position.begin()
			b = next_position.end()
			view.sel().add( sublime.Region( a,b ) )
			view.show( first_selection )
			return

		# print( *str_variables )
		for object_position in slice_selection:
			text = view.substr(object_position)
			if ( current_selection["text"] == text ):
				a = object_position.begin()
				b = object_position.end()
				view.sel().add( sublime.Region( a,b ) )
				view.show( object_position )
				# print( text, object_position )
				remove_element( list_variables, [object_position] )
				break

# Default (Windows).sublime-keymap
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

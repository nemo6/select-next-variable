import sublime
import sublime_plugin

def remove_element(target_array,list_value):
	for index, value in enumerate(target_array):
		if value in list_value:
			target_array.pop(index)
			# break
	return target_array

# Default (Windows).sublime-keymap
# { "keys": ["ctrl+d"], "command": "select_next_variable" },

class select_next_variable(sublime_plugin.TextCommand):
	def run(self,edit):
		view = sublime.active_window().active_view()
		list_variables = view.find_by_selector("variable")
		first_selection = view.substr(view.sel()[0])
		current_selection = { "text": first_selection }
		slice_variables = remove_element( list_variables , view.sel() )
		for object_position in slice_variables:
			text = view.substr(object_position)
			if ( current_selection["text"] == text ):
				a = object_position.begin()
				b = object_position.end()
				view.sel().add( sublime.Region( a,b ) )
				view.show( object_position )
				print( text, object_position )
				remove_element( list_variables, [object_position] )
				break

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

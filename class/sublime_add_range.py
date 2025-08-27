
class add_range(sublime_plugin.WindowCommand):

	def run(self):
        print("add_range")
		self.window.show_input_panel(
			"", 
			"",  # Default text
			self.on_done,    # Callback when done
			self.on_change,  # Callback while typing
			self.on_cancel   # Callback if cancelled
		)

	def on_done( self, value ):
		view = self.window.active_view()
		view.run_command( 'ryyln3vsrzwo', { "value": value } )
	
	def on_change(self, value):
		# print("Current input:", value)
		pass
	
	def on_cancel(self):
		# print("Input cancelled")
		pass

class ryyln3vsrzwo( sublime_plugin.TextCommand ): # command only lower case
	def run(self, edit, value=None ):
		print( value )
		# view = self.view
		# region = view.sel()[0]
		# max = len( view.sel() )
		# m = range( int(value), int(value) + max )
		# for index,region in enumerate(view.sel()):
		# 	self.view.insert( edit, region.begin(), str(m[index]) )

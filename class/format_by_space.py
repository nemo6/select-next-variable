# to do : add format by "\t" too

def get_column( n ):
	m = []
	for x in lines:
		try:
			m.append( x[n] )
		except:
			pass
	return m

class format_by_space(sublime_plugin.TextCommand):
	def run(self, edit):
		global view
		global lines
		view = self.view
		selection = view.sel()[0]
		str_selection = to_str(selection)
		lines = str_selection.split("\n")
		lines = list( map( lambda x: x.split("    ") , lines ) )
		column = {}
		len_range = max ( list( map( lambda x: len(x) , lines ) ) )
		# print( get_column(5) )
		for x in range( 0, len_range ):
			column[x] = max ( list( map( lambda y: len(y) , get_column(x) ) ) )
		for i,x in enumerate(lines):
			for ii,y in enumerate(x):
				lines[i][ii] = lines[i][ii].ljust( column[ii] )
		lines = list( map( lambda x: " ".join(x) , lines ) )
		content = "\n".join(lines)
		# print( lines[0] )
		view.replace( edit, selection , content )

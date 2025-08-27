
# F2
class select_next_after_comma(sublime_plugin.TextCommand):

	def run(self,edit):
		global view
		view = self.view
		selection = view.sel()[-1]
		start = selection.end()
		b = line_end(start)
		# result_comma = filter_by_region( m_comma, sublime.Region( start,b-1 ) )
		# result_comma = list_region_split( result_comma, " " )
		# for region in result_comma:
		# 	view.sel().add( region )
		line = range( start , b-1 )
		line = list( map( lambda x: sublime.Region(x,x+1) , line ) )
		line = list_region_split( line , " " )[0]
		if len(line) > 0:
			line = add_empty_cursor(line)
		line = list( filter( lambda x: to_str(x) != "," , line ) )
		print( list( map( lambda x: f_ord(view.substr(x)), line ) ) )
		if len(line) > 0:
			view.sel().add( line[0] )

# ...

def line_start(point):
	global view
	line_selection = view.line(point)
	return line_selection.begin()

def line_end(point):
	global view
	line_selection = view.line(point)
	return line_selection.end()+1

# ...

def f_ord(char):
	if isinstance( char, str) and len(char) > 0:
		return ord(char)
	else:
		return None

# ...

def add_empty_cursor(m):
	w = [m[0]]
	max = len(m)
	p = range( 1, max )
	i=1
	while i < max:
		w.append( m[i] )
		if to_str(m[i-1]) == "," and to_str(m[i]) == "," :
			w.append( sublime.Region( m[i-1].end(), m[i-1].end() ) )
		i+=1
	if to_str(m[-1]) == ",":
		w.append( sublime.Region( m[-1].end(), m[-1].end() ) )
	return w

def list_region_split( m, value ):
	w = [ [] ]
	for x in m:
		# print(to_str(x))
		if to_str(x) == value:
			w.append([])
			continue
		w[-1].append(x)
	return w

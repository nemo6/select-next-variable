
class expand_or_trim_scope(sublime_plugin.TextCommand):

	scope_not_open = False
	scope_is_open = False

	def is_valid( self, char ):
		return not( re.search( r"\\n|\\t| " , char ) )

	def a_region_b( self , region ):
		result = view.substr(region).strip()
		a = region.begin()
		b = region.end()
		before = sublime.Region( a-1,a )
		after = sublime.Region( b,b+1 )
		# pattern = re.compile( "\\n|\\t| " )
		before = to_str(before)
		after = to_str(after)
		obj = { "before":self.is_valid(before), "after":self.is_valid(after) }
		if( obj["before"] ):
			result = " " + result
		if( obj["after"] ):
			result = result + " "
		return result

	def run(self,edit):
		global view
		scope_not_open = False
		scope_is_open = False
		if( len( self.view.sel() ) == 1 ):
			view = self.view
			selection = view.sel()[0]
			start = selection.begin()
			end   = selection.end()
			before = before_selection( start )
			after  = after_selection( end )

			if( to_str(after) != " " ):
				print("scope not open")
				scope_not_open = True
			else:
				print("scope is open")
				scope_is_open = True

			if to_str(before) not in ["[","{","("]:
				return

			a = line_start(start)
			b = line_end(start)
			line = range( start , b-1 ) # to_str( sublime.Region( start,b ) )
			line = list( map( lambda x: sublime.Region(x,x+1) , line ) )
			result = find_end_scope( line , before )
			[a,b] = result
			result.reverse()
			# print( self.a_region_b(a) )
			# print( self.a_region_b(b) )
			if scope_is_open:
				view.erase( edit, before_selection( b.begin() ) )
				view.erase( edit, after )
			if scope_not_open:
				for region in result:
					view.replace( edit, region, self.a_region_b(region) )
				view.sel().clear()
				view.sel().add( selection )

# ...

def to_str(region):
	return view.substr(region)

def find_end_scope( line, start_scope ):

	end_scope = ""
	char = to_str(start_scope)
	if char not in ["[","{","("]:
		return

	obj= {
	"[" : "]",
	"{" : "}",
	"(" : ")",
	}
	next = obj[char]
	level = 0
	i = 0
	for region in line:
		char_region = to_str(region)
		if( is_string_or_regex_scope(region) ):
			continue

		if( char_region == char ):
			level += 1 # print after, view.sel().add after
			# print( to_str(region), level )

		if( char_region == obj[char] and level == 0 ):
			# return [ start_scope, region ]
			end_scope = region
			break

		if( level > 0 and char_region == obj[char] ):
			# print( to_str(region), level )
			level -= 1 # print before, view.sel().add before

	return [ start_scope , end_scope ]

def before_selection( start ):
	return sublime.Region( start-1,start )

def after_selection( end ):
	return sublime.Region( end,end+1 )

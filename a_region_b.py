
def a_region_b(region):
	result = view.substr(region).strip()
	a = region.begin()
	b = region.end()
	before = sublime.Region( a-1,a )
	after = sublime.Region( b,b+1 )
	pattern = re.compile( "\\n|\\t" )
	before = to_str(before)
	after = to_str(after)
	obj = { "before":is_Not_new_line_or_tab(before), "after":is_Not_new_line_or_tab(after) }
	# return obj
	if( obj["before"] ):
		result = " " + result
	if( obj["after"] ):
		result = result + " "
	return [result]

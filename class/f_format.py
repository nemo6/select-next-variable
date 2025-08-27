
class f_format(sublime_plugin.TextCommand):

	def run(self,edit):
		if( len( self.view.sel() ) == 1 ):
			view = self.view
			selection = view.sel()[0]
			start = selection.begin()
			end = selection.end()
			# pattern = re.escape( view.substr(selection) )
			# print( selection )
			# print( list( map( lambda x: view.substr(x), result ) ) )

			# m_semicolon = view.find_all( r';' )
			# result_semicolon = filter_by_region( m_semicolon, selection )
			# result_semicolon.reverse()
			# for region in result_semicolon:
			# 	view.erase( edit, region )

			# m_quote = view.find_all( "'" )
			# result_quote = filter_by_region( m_quote, selection )
			# print(m_quote)
			# result_quote.reverse()
			# for region in result_quote:
			# 	view.replace( edit, region, "\"" )

			m_space = view.find_all( r" +" )
			result_space = filter_by_region( m_space, selection )
			result_space = list( filter( lambda x: not is_string_scope(view,x) , result_space ) )
			print( result_space )

			# result_quote.reverse()
			# for region in result_quote:
			# 	view.replace( edit, region, "\"" )

def is_string_scope(view,region):
	if "string" in view.scope_name( region.begin() ):
		return True
	else:
		return False

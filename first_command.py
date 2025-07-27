import sublime
import sublime_plugin
import math
import re

view = None
max_lines = None

open_scope  = ["{","[","("]
close_scope = ["}","]",")"]

def remove_element(target_array,list_value):
    for index, value in enumerate(target_array):
        if value in list_value:
            target_array.pop(index)
            # break
    return target_array

def loop_select_word(view):
    for p in view.sel():
        word = view.word(p)
        if word and ( p.begin() == p.end() ) :
            if p.contains(word):
                continue
            a = word.begin()
            b = word.end()
            view.sel().add( sublime.Region( a,b ) )
            view.show( word )

def isAfter( a, b ):
    return a.begin() > b.begin()

# Default (Windows).sublime-keymap
# { "keys": ["ctrl+d"], "command": "select_next_variable" },

class select_next_variable(sublime_plugin.TextCommand):
    def run(self,edit):
        not_a_variable = False
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
        #   h.pop(0)
        # print( current_selection["text"], first_selection )
        # print( *h,sep="\n" )

        if( len( view.sel() ) > 1 ):
            # print("multi-selection")
            if "string" in view.scope_name( view.sel()[0].begin() ):
                # print("in a string scope")
                not_a_variable = True

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
            #   return
            a = next_position.begin()
            b = next_position.end()
            view.sel().add( sublime.Region( a,b ) )
            view.show( first_selection )
            return

        # print( *list(filter( lambda x: x == current_selection["text"], str_variables )) )
        # print( "Is a variable" )
        # print( *str_variables )
        # print( *slice_selection )

        for object_position in slice_selection:
            text = view.substr(object_position)
            if ( current_selection["text"] == text and isAfter( object_position , first_selection ) ):
                a = object_position.begin()
                b = object_position.end()
                view.sel().add( sublime.Region( a,b ) )
                view.show( object_position )
                break

class add_cursor_comma(sublime_plugin.TextCommand):
    def run(self,edit):
        global view
        view = sublime.active_window().active_view()
        cursor_selection = view.sel()[-1]
        cursor_pos = view.sel()[0].begin()
        print( cursor_pos, reverse_get_line( view.sel()[0] ) )
        a = view.sel()[0].begin()
        b = view.sel()[0].end()
        next_char = view.substr( sublime.Region( cursor_pos , cursor_pos + 1 ) )
        after_comma = { "region": sublime.Region( a + 1 , b + 2 ) , "word": view.word( sublime.Region( a + 1 , b + 2 ) )}
        # print( "next_char", next_char )
        # print( "after_comma", *list( map( lambda x : ord(x) , view.substr(after_comma["word"]) ) ) )
        if( len(next_char) != 0 and next_char == "," ):
            word = view.word(cursor_pos)
            word_text = view.substr(word)[:-1]
            if( word_text.isspace() ):
                return
            if word:
                a = word.begin()
                b = word.end()
                view.sel().add( sublime.Region( a,b ) )
                view.show( word )
            if( view.substr(after_comma["word"])[0] != "," ):
                a = after_comma["word"].begin()
                b = after_comma["word"].end()
                view.sel().add( sublime.Region( a,b ) )
                view.show( word )

            new_cursor_pos = cursor_pos + 1
            view.sel().add(sublime.Region(new_cursor_pos))
        # else:
        #     print(None)

class add_scope_function(sublime_plugin.TextCommand):
    def run(self,edit):
        region = self.view.sel()[0] # Get the first selection region
        # a = region.sel()[0].begin()
        # b = region.sel()[0].end()
        start_pos = region.begin()
        end_pos   = region.end()
        length = region.end() - region.begin()
        # Work in reverse to prevent offset issues
        if( length != 0 ):
            self.view.insert( edit, end_pos, " })" )
            self.view.insert( edit, start_pos, ";( () => { " )

class add_arrow(sublime_plugin.TextCommand):
    def run(self,edit):
        if( len(self.view.sel()) == 2 ):
            a,b = self.view.sel()
            start_pos = a.begin()
            end_pos   = b.begin()
            self.view.insert( edit, end_pos, " <=" )
            self.view.insert( edit, start_pos, " =>" )

def line_start(point):
    global view
    line_region = view.line(point)
    return line_region.begin()

def line_end(point):
    global view
    line_region = view.line(point)
    return line_region.end()+1

def find_line_number(view, point):
    line_number = view.rowcol(point)[0]
    return line_number+1

def get_indentation_level( line_region ):
    global view
    line_text = view.substr(line_region)
    spaces_count = len(line_text) - len(line_text.lstrip(' '))
    tabs = len(line_text) - len(line_text.lstrip('\t'))
    space_width = view.settings().get( 'tab_size' )
    spaces = int(spaces_count / space_width)
    if( tabs == 0 ):
        tabs = spaces
    m = [spaces,tabs]
    # print( math.modf( spaces_count / space_width ) )
    if( math.modf( spaces_count / space_width )[0] == 0.0 ):
        return max( m )
    else:
        return None

def get_line_region(n):
    n = n - 1
    global view
    line_point = view.text_point( n, 0 ) # line 5 : view.text_point( 5, 0 )
    # line_region = view.full_line(line_point)
    line_region = view.line(line_point)
    return line_region

def get_line_content(n):
    global view
    line_point = view.text_point( ( n - 1 ) , 0 ) # line 5 : view.text_point( 5, 0 )
    line_region = view.line(line_point)
    # line_content = view.substr( line_region)
    a = line_region.begin()
    b = line_region.end()
    # result = re.sub( r"\r\n|\n", "" , line_content )
    return {
    "number": n,
    "level": get_indentation_level( line_region ),
    "not_empty": (b-a) != 0,
    "region": line_region
    }

def find_scope( n,self,edit ):

    current_line = get_line_content(n)
    line_region = get_line_region(n)

    global view
    global max_lines
    start = None
    end   = None
    obj = { "start": None, "end": None }
    key1  = None
    key2  = None
    last_char = ""

    if( current_line["level"] == 0 ):

        capture_line = view.substr(line_region)
        # remove block comment
        capture_line = re.sub( r"\/\*.*?\*\/", "" , capture_line )

        if( len(capture_line) > 0 ):
            last_char = capture_line[-1]

        if last_char in open_scope:
            key1 = "start"
            key2 = "end"

        if last_char in close_scope:
            key1 = "end"
            key2 = "start"

        obj[key1] = current_line
        
    if( key1 == "start" ):
        obj[key2] = find_down(n+1)
    elif( key1 == "end" ):
        obj[key2] = find_up(n)
    else:
        obj = { "start": find_up(n), "end": find_down(n) }

    list_substr2_start = view.substr(obj["start"]["region"])
    list_substr2_end = view.substr(obj["end"]["region"])

    # remove block comment
    list_substr2_start = re.sub( r"\/\*.*?\*\/", "" , list_substr2_start )
    list_substr2_end = re.sub( r"\/\*.*?\*\/", "" , list_substr2_end )

    if( len(list_substr2_start) > 0 ):
        char = get_last_char(list_substr2_start)
        if char not in open_scope:
            return None
    if( len(list_substr2_end) > 0 ):
        char = get_last_char(list_substr2_end)
        if char not in close_scope:
            return None

    point_end = obj["end"]["region"].end()
    char_toggle = view.substr(obj["end"]["region"])[-4:]

    if( char_toggle == "})()" ):
        erase_region = sublime.Region( point_end-2 , point_end )
        view.erase( edit, erase_region )
        self.view.insert( edit, obj["end"]["region"].end() - 2 , "/*()*/" )

    if( char_toggle == "()*/" ):
        erase_region = sublime.Region( point_end-6 , point_end )
        view.erase( edit, erase_region )
        self.view.insert( edit, obj["end"]["region"].end() - 6 , "()" )

    return obj

def get_last_char(char):
    if( len(char) > 0 ):
        return char[-1]
    else:
        return ""

def find_up(n):
    m = list( range( 0, n ) )
    m.reverse()
    for x in m:
        obj = get_line_content(x)
        if( obj["level"] == 0 and obj["not_empty"] ):
            return obj
    return "find_up X"

def find_down(n):
    global max_lines
    for x in range( n, max_lines+1 ):
        obj = get_line_content(x)
        if( obj["level"] == 0 and obj["not_empty"] ):
            return obj
    return "find_down X"

def reverse_get_line(region):
    global view
    line_number = view.rowcol( region.begin() )[0] + 1
    return line_number

def get_function_params_start(max_lines):
    global view
    function_styles = [
        r';\( async \(\) => {',  # Standard function
    ]
    for style in function_styles:
        result = view.find_all( style )
        # print( function_def )
        # region = sublime.Region( function_def )
        for region in result[0:1]:
            print( reverse_get_line( region, max_lines ) )
        # print( function_def[0] )

class toggle_scope(sublime_plugin.TextCommand):

    def run(self, edit):

        global view
        global max_lines
        view = self.view
        point = view.sel()[0].begin()
        n = find_line_number( view, point )
        line_region = view.line(point)
        # current_line_text = view.substr(line_region)
        max_lines = view.rowcol(view.size())[0]+1
        # w = map( lambda x: x["number"], find_scope( n, self, edit ).values() )
        # print( *w )
        print( find_scope( n, self, edit ) )

# self.view.insert( edit, a, "/* ... */" )
# self.view.insert( edit, b, "/* ... */" )

# for x in range( 1, 5+1 ):
# { "keys": ["è"], "command": "add_backtick" },
# C:\Users\Miguel\AppData\Roaming\Sublime Text\Packages\User\Default (Windows).sublime-keymap

"""
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
#   commands = sublime.load_resource("Packages/User/Default.sublime-commands")
#   commands = sublime.decode_value(commands)
#   return commands
#   for command in commands:
#       if command["caption"] == caption:
#           return command["command"]
#   return None

# class HelloWorldCommand(sublime_plugin.TextCommand):
#   def run(self, edit):
#       caption = "[RegReplace] Format : Space arround parenthesis and brackets"
#       command_name = get_command_name(caption)
#       if command_name:
#           sublime.active_window().run_command( command_name[0]["command"] , command_name[0]["args"] )
#           self.view.insert( edit, self.view.sel()[0].begin(), "hello world" )
#
# class HelloWorldCommand(sublime_plugin.TextCommand):
#   def run(self, edit):
#       self.view.insert(edit, self.view.sel()[0].begin(), "hello world")

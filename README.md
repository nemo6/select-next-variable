	.../AppData/Roaming/Sublime Text/Packages/User/Default.sublime-commands
```
[
	{
		"caption": "add arrow (command)",
		"command": "add_arrow",
	},

	{
		"caption": "range (command)",
		"command": "add_range",
	},

	{
		"caption": "input range 0-X (command)",
		"command": "input_list_range",
		"args": { "value": 0 }
	},

	{
		"caption": "input range 1-X (command)",
		"command": "input_list_range",
		"args": { "value": 1 }
	},

	{
		"caption": "slash (command)",
		"command": "reg_replace",
		"args": { "replacements": ["format_slash"] },

	},

	{
		"caption": "unslash (command)",
		"command": "reg_replace",
		"args": { "replacements": ["format_unslash"] },

	},

	{
		"caption": "format (command)",
		"command": "f_format",

	}
]
```
	.../AppData/Roaming/Sublime Text/Packages/User/Default (Windows).sublime-keymap

```
{ "keys": ["f1"], "command": "favorite_files_open" },
{ "keys": ["f2"], "command": "add_cursor_comma" },
{ "keys": ["f3"], "command": "add_scope_function" },
{ "keys": ["f4"], "command": "toggle_scope" },
```

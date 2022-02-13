# Utility to query a user's public gists

## Usage:

`show_pub_lists <user> <option>`

Where 
`<user>` is the Github user's username and `<option>` can be 'l' for lists only and 'd' for detailed list

When the user is quried for the first time, it will save the user's latest gist date and time in a file named `/tmp/show_pub_lists.<user>` and either list public gists or list public gists with contents of gists as per option. On subsequent runs it will compare the datetime and show gists if there are new gists added by user.

To reset a user's query, delete `/tmp/show_pub_gists.<user>`.
To reset all queries, delete `/tmp/show_pub_gists.*`

## Requirements

* Python 3 or higher
* Apply modules in setup.txt

## Exit codes

* User not found: 255
* User has not published any gists: 1
* Success (first or subsequent queries): 0

## License

GNU General Public License v3.0

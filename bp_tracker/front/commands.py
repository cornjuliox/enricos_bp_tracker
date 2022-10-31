import argparse

# NOTE: I don't know what the types are for the subparsers? or any of the parsers for that matter. 
# TODO: This could be organized better, I think
parser = argparse.ArgumentParser()
parser.add_argument(
    "filepath",
    type=str,
    help="Full/relative path to the database file. If it doesn't exist it will be created."
)
subparser = parser.add_subparsers(help="sub-commands", dest="command")

#####################
add_command = subparser.add_parser(
    "add",
    help="Adds an entry to the log"
)
add_command.add_argument(
    "sys",
    type=int,
    help="Systolic pressure, read from the machine, needs to be a number."
)
add_command.add_argument(
    "dia",
    type=int,
    help="Diastolic pressure, read from the machine, needs to be a number."
)
add_command.add_argument(
    "pulse",
    type=int,
    help="Pulse value, read from the machine, needs to be a number."
)
add_command.add_argument(
    "notes",
    type=str,
    help="Any important notes you'd like to add. Has to be a string wrapped in double quotes.",
    default="",
    nargs="?"
)
#####################
#####################
remove_command = subparser.add_parser(
    "remove",
    help="Removes an entry from the log."
)
remove_command.add_argument(
    "timestamp",
    type=int,
    help="Every entry matching that timestamp will be removed."
)
##################### 
##################### 
latest_command = subparser.add_parser(
    "latest",
    help="Shows the latest N items, by default 10, use --limit to specify how many."
)
latest_command.add_argument(
    "--raw_timestamps",
    action="store_true"
)
latest_command.add_argument(
    "--limit",
    type=int,
    help="How many items would you like to see?"
)
#####################
#####################
by_month = subparser.add_parser(
    "month",
    help="View all entries for a specific month, pass in an integer from 1-12."
)
by_month.add_argument(
    "month_int",
    type=int,
    help="Integer representing a month - January -> 1, Feburary -> 2, so on so forth.",
    choices=range(1, 13)
)
by_month.add_argument(
    "year_int",
    type=int,
    help="Integer representing a 4-digit year, e.g '1998', '2002', etc"
)
#####################
#####################
by_date_range = subparser.add_parser(
    "range",
    help="View all entries for a specific date range."
)
by_date_range.add_argument(
    "start_date",
    type=str,
    help="Start date, in the format YYYY-MM-DD."
)
by_date_range.add_argument(
    "end_date",
    type=str,
    help="End date, in the format YYYY-MM-DD."
)
by_date_range.add_argument(
    "--report",
    action="store_true"
)
#####################
cli_args = parser.parse_args()

# NOTE: There is apparently no way to do this within argparse.
# NOTE: This workaround will serve until I find a better one.
if cli_args.command is None:
    parser.error("Need to specify a subcommand, run with -h flag to see the list of subcommands.")

# About
I use this file to track current issues with development and to record my thoughts and shit. Think of it as a sort of 'blog' but in a github repo.

# Report Generation
## NOV 1, 2022
The last bit of functionality I need to build out for this thing is the ability to generate reports. Back in the day, Google Sheets was enough - you'd just hit "export" and download it as a PDF and you've got a nice, handy list to hand to your Doctor. If you so choose, you could even use Sheets' ability to generate line graphs to see trends and other related stuff. I don't know how much value line graphs provide to a doctor but it can't hurt to have that ability on hand, right?

The data's already available as a `list[dict[str, str]]`, and I've already got prototype code in that writes it to an HTML file, so the next step is to maybe figure out how to generate pdfs from Python (In the meantime, I'll just open the .html in a web browser and 'Print to PDF').

I also want to figure out how the CLI will look for this. Right now it seems like having a report subcommand like `python cli.py report --arg1 --arg2 --arg3 ...` is the way to go as I'd want to allow for configuration, and the subsequent backend code for this command is easy enough to envision in my head.

# Timezone Issues
## NOV 1, 2022
`mypy` complains about the following piece of code :

```python
# NOTE: in bp_tracker.front.utils
# error: bp_tracker\front\utils.py:26: error: Argument 1 to "to" of "Arrow" has incompatible type "Optional[tzinfo]"; expected "Union[tzinfo, str]"
SYSTZ: Optional[tzinfo] = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
# ...snip...
def __convert_timestamp(x: dict) -> dict:
    int_timestamp: int = x["timestamp"]
    arrow_timestamp: arrow.Arrow = arrow.get(int_timestamp)
    arrow_timestamp = arrow_timestamp.to(SYSTZ)
    x["timestamp"] = arrow_timestamp.format("MMM DD, YYYY @ HH:mm")
    return x
```

After some digging, I find that there's no guarantee that SYSTZ will actually have timezone data in it because not all systems use IANA timezone keys to set timezone[^1], and I get the impression that some systems don't set a timezone at all.

This program's entire datetime mechanism has, until this point, assumed that a timezone would always be available but this discovery breaks that assumption. So I now have to account for the possibility that there isn't a timezone available on a given system, and I'm not entirely sure how to go about that. I could do one of two things:

1. Try to guess at the timezone whenever it's not available.
1. Rewrite the whole program, data model and all, to only handle dates and not times.

Arguments in favor of guessing:
- It'll allow me to keep the current program and data model as-is, with very little in the way of redesign / rewrite.

Arguments against guessing:
- At this point I don't know much about handling timezones correctly, and this could be a very complex problem without an accurate solution that will take days of work without.
- Guessing incorrectly could corrupt data (i.e lead to incorrect /inaccurate reporting)

Arguments in favor of rewriting:
- It could potentially be easier to rewrite than to grapple with time-related issues 

Arguments against:
- Data wouldn't be as accurate simply because there would be no way to note what TIME a blood pressure was taken, apart from the notes.
- A rewrite is time-consuming, and would potentially introduce new problems as a side effect

Still haven't decided.

[1]: See [here](https://discuss.python.org/t/get-local-time-zone/4169/3) for discussion

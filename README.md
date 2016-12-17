# Newsreel.py

A wrapper around newspaper

Newsreel is a simple command line tool/wrapper around newspaper.  It makes it easy to periodically scrape a colleciton of news sites, adding articles to a database.  The commands:

* `--help`
* `--add <source|article> name url`: add the specified source or article to the database
* `--deactivate url`: set the specified source to inactive, meaning the system will not scrape it
* `--activate url`: set the specified source to active, meaning the system will scrape it
* without any command line flags, the script will scrape the active sources

Debugging commands: There are a handful of commands for checking the state of the database

* `--print_sources`: prints the sources, and if they are active
* `--print_stats`: print the number of sources and articles in the database
* `--print_article index`: prints the title and summary of the article at the specified index, sorted by date of writing

## Installing

The script depends on newspaper and sqlalchemy.

Git clone the repository wherever you want.

Edit line 3 in `db_utils.py `to connect to your database.  You can test the connection by running `python db_utils.py`

Run `python newsreel.py --create` to generate the table schema.  Run `python newsreel.py --add source None None` to allow manual article addition.  After, run `python newsreel.py --deactivate None`.  Next, run `python newsreel.py --add source [display name] [url]` to add a source, changing display name and url to whatever you want.  Finally, run `python newsreel.py` to scrape the source(s) you added.

import newspaper
import sqlalchemy as sqla
import datetime
import sys
import orm
import db_utils

def add_source(name, url):
    """add a source to the database, and mark as active"""
    Session = sqla.orm.sessionmaker(bind=db_utils.engine)
    session = Session()
    ret = session.query(sqla.exists().where(orm.Source.url==url)).scalar()
    if ret:
        session.close()
        return
    source = orm.Source(url=url,name=name,active=True)
    session.add(source)
    session.commit()
    session.close()
    
def deactivate_source(url):
    Session = sqla.orm.sessionmaker(bind=db_utils.engine)
    session = Session()
    s = session.query(orm.Source).filter(orm.Source.url == url)[0]
    s.active = False
    session.commit()
    session.close()

def activate_source(url):
    Session = sqla.orm.sessionmaker(bind=db_utils.engine)
    session = Session()
    s = session.query(orm.Source).filter(orm.Source.url == url)[0]
    s.active = True
    session.commit()
    session.close()
    
def print_sources():
    """Print active and inactive sources, useful in debugging"""
    sources = get_sources()
    print "Active sources:"
    for s in sources:
        if s.active:
            print "\t{}: {}".format(s.name,s.url)
    print "Inactive sources:"
    for s in sources:
        if not s.active:
            print "\t{}: {}".format(s.name,s.url)

def print_stats():
    Session = sqla.orm.sessionmaker(bind=db_utils.engine)
    session = Session()
    n_sources = session.query(orm.Source).count()
    n_articles = session.query(orm.Article).count()
    print "Database contains {} sources, {} articles".format(n_sources, n_articles)
    session.close()
    
def print_article(n):
    Session = sqla.orm.sessionmaker(bind=db_utils.engine)
    session = Session()
    articles = session.query(orm.Article).order_by(orm.Article.date_written)
    a = articles[n]
    print "{}: {}".format(a.title,a.summary)
    session.close()
    
def get_sources(active=False):
    """returns a list of source urls for the database"""
    Session = sqla.orm.sessionmaker(bind=db_utils.engine)
    session = Session()
    sources = session.query(orm.Source)
    if active == True:
        sources = [s for s in sources if s.active]
    return sources

def scrape_sources():
    """Scrape all active sources in the DB"""
    sources = get_sources(active=True)
    for s in sources:
        scrape_source(s.url)
    
def scrape_source(source_url):
    """uses newspaper to build a list of articles at the given url, then processes and populates the DB with those articles, checking for duplicates"""
    print "Scraping {}".format(source_url)
    paper = newspaper.build(source_url)
    print "Found {} articles".format(len(paper.articles))
    for article in paper.articles:
        print "\tScraping {}".format(article.url)
        add_article(source_url,article.url)
    
def add_article(source,article_url):
    #confirm the story is new to the db, by the url
    Session = sqla.orm.sessionmaker(bind=db_utils.engine)
    session = Session()
    ret = session.query(sqla.exists().where(orm.Article.url==article_url)).scalar()
    session.close()
    if ret:
        return
    n_article = newspaper.Article(article_url)
    n_article.download()
    o_article = orm.Article()
    o_article.url = article_url
    o_article.source = source
    o_article.raw = n_article.html
    n_article.parse()
    o_article.title = n_article.title
    o_article.text = n_article.text
    o_article.date_written = n_article.publish_date
    o_article.date_added = datetime.datetime.utcnow()
    n_article.nlp()
    o_article.summary = n_article.summary
    Session = sqla.orm.sessionmaker(bind=db_utils.engine)
    session = Session()
    session.add(o_article)
    session.commit()
    session.close()
    
def create():
    orm.Base.metadata.create_all(db_utils.engine) #create schemata

def process_cli(args):
    """consumes comman line args.  If they match one of the patterns, run the appropriate function"""
    if len(args)<2:
        scrape_sources()
    elif args[1] == "--add":
        if len(args) != 5:
            print "--add take 3 arguments, see --help for more"
            return
        if args[2] == "source":
            add_source(args[3],args[4])
        elif args[2] == "article":
            add_article('None',args[4])
        else:
            print "Please specify if this is a source or an article"
    elif args[1] == "--create":
        create()
    elif args[1] == "--print_stats":
        print_stats()
    elif args[1] == "--print_sources":
        print_sources()
    elif args[1] == "--print_article":
        print_article(int(args[2]))
    elif args[1] == "--deactivate":
        deactivate_source(args[2])
    elif args[1] == "--activate":
        deactivate_source(args[2])
    else:
        print "Newsreel, a newspaper wrapper for persistant storage of scraped news stories.  Available commands:\n--help: this help text\n--add <source|article> name url\n--create: will attempt to create the db tables for the system; should be idemopotent\nIf no flags are given, newsreel will scrape all active sources from the database\nDebug commands: --print_stats --print_sources --print_article [n]"
        
if __name__=='__main__':
    args = sys.argv
    process_cli(args)
from papertalk import mongo

class Article(object):
    """
    An article in papertalk.
    Title (str)
    Authors (list of str)
    Year (dt)
    Num citations (num)
    Full Citation (text)
    url (str)
    """

    def __init__(self, article_id=None):
        self.attrs = {'title':         None,
                      'authors':       [],
                      'source_urls':   [],
                      'direct_url':    None,
                      'num_citations': 0,
                      'url_citations': None,
                      'url_versions':  None,
                      'num_versions':  0,
                      'year':          None,
                      'url':           None,
                      'doi':           None}
        self.reactions = []

        if article_id:
            self.load(article_id)


    def __getitem__(self, key):
        return self.attrs[key]

    def __setitem__(self, key, item):
        self.attrs[key] = item

    def __delitem__(self, key):
        del self.attrs[key]

    def load(self, article_id):
        self.attrs = mongo.db.articles.find_one(article_id)

    def save(self):
        article = mongo.db.articles.find_one({"title" : self["title"],
                                              "year" : self["year"]})
        if article:
            print "article exists"
            article_id = article["_id"]
        else:
            print "creating new article"
            article_id = mongo.db.articles.insert(self.attrs)

        return article_id

    def as_txt(self):
        # Get items sorted in specified order:
        return '\n'.join(["%s: %s" % (item[0], item[1]) for item in self.attrs.iteritems()])

    def as_json(self):
        return self.attrs

    @classmethod
    def lookup(cls, title=None, year=None):
        """
        lookup an article in our db
        """
        return mongo.db.articles.find_one({"title": title,
                                           "year": year})

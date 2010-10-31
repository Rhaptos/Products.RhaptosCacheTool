from Globals import InitializeClass
from OFS import SimpleItem
from OFS.PropertyManager import PropertyManager
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from AccessControl import ClassSecurityInfo
from Products.CMFCore.utils import UniqueObject
from Products.CMFCore import permissions
from Products.CMFCore.ActionProviderBase import ActionProviderBase
import md5
import zLOG
def log(msg, severity=zLOG.INFO):
    zLOG.LOG("RhaptosCacheTool: ", severity, msg)

class cache(UniqueObject, PropertyManager, 
                       SimpleItem.SimpleItem, ActionProviderBase):

    "The Rhaptos Cache tool"

    meta_type = 'cache'

    id = 'cache'


    manage_options = PropertyManager.manage_options + \
                     SimpleItem.SimpleItem.manage_options + (
    	{'label': 'View', 'action': 'index_html',},
    )

    _properties = (
        {'id':'title', 'type':'string', 'mode':'w'},
    )

    # Standard security settings
    security = ClassSecurityInfo()

    security.declareProtected('Manage properties', 'index_html')
    index_html = PageTemplateFile('zpt/cache.rss', globals())


    def __init__(self,id,title=''):
        """Initialize results cache object"""
        self.searches = {}

    def _p_resolveConflict(self, oldState, savedState, newState):
        return newState


    security.declareProtected(permissions.ManagePortal, "resultsCacheInject")
    def resultsCacheInject(self, searchhash, record):
        """Insert values for a search/browse results key as a tuple 
        (result,term_results,sort_on) into the cache, using the provided 
        key 'searchhash'.
        """
        record = (self.wrapResults(record[0]),) + record[1:]
        self.searches[generateCacheKey(searchhash)] = (searchhash,record)
        self._p_changed = 1
        return None
    
    security.declarePublic("resultsCacheDump")
    def resultsCacheDump(self):
        """Dumps full cache"""
        return self.searches.items()

    security.declarePublic("resultsCacheLookup")
    def resultsCacheLookup(self, searchhash, sorton=None, recent=False):
        """Returns sorted cached values, if any, for a search/browse 
        results key as a tuple (result,term_results) or None if no cache hit.
        """
        cached_tup = self.searches.get(generateCacheKey(searchhash), None)
        if cached_tup:
            results,term_results,cached_sort,cached_recent = cached_tup[1]
            if sorton and (cached_sort != sorton or cached_recent != recent):
                results = self.sortSearchResults(results, sorton, recent)
                self.resultsCacheInject(searchhash, (results, term_results, sorton, recent))
            return results,term_results
        else:
            return None
        
    security.declarePublic("clearSearchCache")
    def clearSearchCache(self):
        """Clear out all the cached searches"""
        self.searches.clear()
        self._p_changed = 1
        return None

class nocache(UniqueObject, PropertyManager, 
                       SimpleItem.SimpleItem, ActionProviderBase):

    "The Rhaptos Cache tool"

    meta_type = 'nocache'

    id = 'cache'


    manage_options = PropertyManager.manage_options + \
                     SimpleItem.SimpleItem.manage_options + (
    	{'label': 'View', 'action': 'index_html',},
    )

    _properties = (
        {'id':'title', 'type':'string', 'mode':'w'},
    )

    # Standard security settings
    security = ClassSecurityInfo()

    security.declareProtected('Manage properties', 'index_html')
    index_html = PageTemplateFile('zpt/cache.rss', globals())


    def __init__(self,id,title=''):
        """Initialize results cache object"""
        pass

#    def _p_resolveConflict(self, oldState, savedState, newState):
#        return newState


    security.declareProtected(permissions.ManagePortal, "resultsCacheInject")
    def resultsCacheInject(self, searchhash, record):
        """Insert values for a search/browse results key as a tuple 
        (result,term_results,sort_on) into the cache, using the provided 
        key 'searchhash'.
        """
        log('inject (nocache): %s' % searchhash)
        return None
    
    security.declarePublic("resultsCacheDump")
    def resultsCacheDump(self):
        """Dumps full cache"""
        return []

    security.declarePublic("resultsCacheLookup")
    def resultsCacheLookup(self, searchhash, sorton=None, recent=False):
        """Returns sorted cached values, if any, for a search/browse 
        results key as a tuple (result,term_results) or None if no cache hit.
        """
        log('lookup (nocache): %s' % searchhash)
        return None
        
    security.declarePublic("clearSearchCache")
    def clearSearchCache(self):
        """Clear out all the cached searches"""
        return None

#####################################################
# Constructor functions, only used when adding class
# to objectManager

def manage_addCache(self, REQUEST=None):
    "Add tool instance to parent ObjectManager"
    id = cache.id
    self._setObject(id, cache(id))
    if REQUEST is not None:
        return self.manage_main(self, REQUEST)

cache_constructors = (manage_addCache,)

def manage_addNoCache(self, REQUEST=None):
    "Add tool instance to parent ObjectManager"
    id = nocache.id
    self._setObject(id, nocache(id))
    if REQUEST is not None:
        return self.manage_main(self, REQUEST)

nocache_constructors = (manage_addNoCache,)

def generateCacheKey(searchhash):
    """Returns actual key used in cache dictionary, from API 'searchhash' 
    string. Allows optimization of key for underlying storage method.
    """
    return md5.md5(searchhash).digest()

InitializeClass(cache)


import Cache

def initialize(context):

    "This makes the tool appear in the product list"

    context.registerClass(
        Cache.cache,
        constructors = Cache.cache_constructors,
        icon="zpt/icon.gif"
    )

    context.registerClass(
        Cache.nocache,
        constructors = Cache.nocache_constructors,
        icon="zpt/icon.gif"
    )

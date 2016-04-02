
# Imports config
#import config
from gcloud import datastore


dbkey = 'Book'

def get_client():
#   Need to keep config in config.py do this later
	return datastore.Client('practical-brace-126614')
def update(data, id=None):
    ds = get_client()
    if id:
        key = ds.key(dbkey, int(id))
    else:
        key = ds.key(dbkey)

    entity = datastore.Entity(
        key=key,
        exclude_from_indexes=['description'])

    entity.update(data)
    ds.put(entity)
 	#return entity
 #   return from_datastore(entity)

def delete(id):
    ds = get_client()
    key = ds.key(dbkey, int(id))
    ds.delete(key)

book = {'title': u'Tarjei', 'author': u'Utnes', 'publishedDate': u'11', 'balle': u'Heisann sveisanafdasdfasdfasdfasdfn'}

print(update(book))


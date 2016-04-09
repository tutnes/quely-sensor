#From googles example
import config
from gcloud import datastore

def get_client():
#   Need to keep config in config.py do this later
    return datastore.Client(config.PROJECT_ID)

def update(data, id=None):
    ds = get_client()
    if id:
        key = ds.key(config.KIND, int(id))
    else:
        key = ds.key(config.KIND)

    entity = datastore.Entity(
        key=key,
        exclude_from_indexes=['description'])

    entity.update(data)
    ds.put(entity)
#    return entity

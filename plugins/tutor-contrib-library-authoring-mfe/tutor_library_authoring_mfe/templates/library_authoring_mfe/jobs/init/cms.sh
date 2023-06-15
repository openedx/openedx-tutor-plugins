# Enable the waffle flag to use this MFE
(./manage.py cms waffle_flag --list | grep studio.library_authoring_mfe) || ./manage.py lms waffle_flag  studio.library_authoring_mfe --create --everyone

# Make sure a Blockstore "Collection" exists to hold the library content.
# the UUID is created in CONFIG_UNIQUE in plugin.py
echo "from blockstore.apps.bundles.models import Collection; coll, _ = Collection.objects.get_or_create(title='Libraries Content Collection', uuid='{{BLOCKSTORE_COLLECTION_UUID}}')" | ./manage.py cms shell

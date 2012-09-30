import os
from uuid import uuid4
from flask.ext.uploads import configure_uploads as flask_configure_uploads
from flask.ext.uploads import UploadSet, IMAGES, patch_request_class


class UUIDUploadSet(UploadSet):
    """
    Custom UploadSet that uses UUIDs for filenames.
    """
    def save(self, storage, folder=None):
        """
        Save the file but set the filename to a uuid value.
        """
        return super(UUIDUploadSet, self).save(storage, folder=folder, name='%s.' % str(uuid4()))

    def resolve_conflict(self, target_folder, basename):
        """
        If a file with the selected name already exists in the target folder,
        this method is called to resolve the conflict. It should return a new
        basename for the file.
        """
        name, ext = basename.rsplit('.', 1)
        while True:
            newname = '%s.%s' % (str(uuid4()), ext)
            if not os.path.exists(os.path.join(target_folder, newname)):
                return newname


# Use UUIDs for the profile picture filenames in case they are public. This
# prevents filenames from having inappropriate filenames (eg. offensive words,
# long filenames, etc). Also don't use the user.id as the filename, because
# users can guess and download the files easily.
profile_pics = UUIDUploadSet('profiles', IMAGES)


def configure_uploads(app):
    """
    Attach upload sets to the app and initialise uploads.
    """
    flask_configure_uploads(app, profile_pics)
    # Only allow uploads up to 5MiB
    patch_request_class(app, size=(5 * 1024 * 1024))

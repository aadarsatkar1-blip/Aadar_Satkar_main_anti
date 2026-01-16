from django.core.files.storage import Storage
from django.conf import settings
from supabase import create_client
import uuid
import os

class SupabaseStorage(Storage):
    def __init__(self, bucket_name='media', **kwargs):   # ✅ double underscores
        self.supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        self.bucket_name = bucket_name

    def _save(self, name, content):
        # Clean the file path
        clean_name = name.replace("\\", "/")
        base, ext = os.path.splitext(clean_name)

        # Generate unique file name using UUID
        unique_name = f"{base}_{uuid.uuid4().hex}{ext}"

        # Read content
        file_content = content.read()

        # Upload to Supabase
        self.supabase.storage.from_(self.bucket_name).upload(
            path=unique_name,
            file=file_content,
            file_options={"content-type": getattr(content, 'content_type', None)}
        )

        # Return unique file path so Django stores it in DB
        return unique_name

    def url(self, name):
        return self.supabase.storage.from_(self.bucket_name).get_public_url(name)

    def exists(self, name):
        return False

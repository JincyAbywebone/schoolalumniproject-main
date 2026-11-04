import os
import logging
from io import BytesIO
from PIL import Image, ImageOps
from django.conf import settings
from django.utils.text import slugify

logger = logging.getLogger(__name__)


def save_user_profile_pic(uploaded_file, user):
    """
    Standard profile picture processing for all user roles:
    1. Compresses & resizes image (max 1200x1200, JPEG quality=75, optimize=True).
    2. Naming convention: <slugified_first_name>_<user_id>.jpg.
    3. Saves into MEDIA_ROOT/profiles/.
    4. Automatically deletes the old profile picture if it was a different file on disk.
    5. Updates user.profile_pic to 'profiles/<filename>' with forward slashes.
    """
    if not uploaded_file or not user or not getattr(user, 'id', None):
        return None

    # Track old profile picture before updating by checking DB
    old_profile_name = None
    try:
        from .models import CustomUser
        db_user = CustomUser.objects.filter(id=user.id).values('profile_pic').first()
        if db_user and db_user['profile_pic']:
            old_profile_name = str(db_user['profile_pic'])
    except Exception:
        pass

    if not old_profile_name and getattr(user, 'profile_pic', None) and user.profile_pic.name:
        old_profile_name = str(user.profile_pic.name)

    try:
        # Open and process image
        with Image.open(uploaded_file) as img:
            img = ImageOps.exif_transpose(img)
            img.thumbnail((1200, 1200), Image.Resampling.LANCZOS)
            if img.mode != 'RGB':
                rgba_image = img.convert('RGBA')
                rgb_image = Image.new('RGB', rgba_image.size, 'white')
                rgb_image.paste(rgba_image, mask=rgba_image.getchannel('A'))
                img = rgb_image

            image_buffer = BytesIO()
            img.save(image_buffer, format='JPEG', quality=75, optimize=True)

        profiles_dir = os.path.join(settings.MEDIA_ROOT, 'profiles')
        os.makedirs(profiles_dir, exist_ok=True)

        import time
        safe_name = slugify(user.first_name) or 'user'
        timestamp = int(time.time())
        filename = f"{safe_name}_{user.id}_{timestamp}.jpg"
        new_full_path = os.path.join(profiles_dir, filename)

        # Write new image bytes
        with open(new_full_path, 'wb') as f:
            f.write(image_buffer.getvalue())

        new_relative_path = f"profiles/{filename}"
        user.profile_pic.name = new_relative_path
        user.save(update_fields=['profile_pic'])

        # Delete old profile picture if it was a genuinely different file on disk
        if old_profile_name:
            clean_old = old_profile_name.replace('\\', '/').lstrip('/')
            if clean_old.startswith('media/'):
                clean_old = clean_old[len('media/'):]
            old_full_path = os.path.join(settings.MEDIA_ROOT, os.path.normpath(clean_old))

            if (
                os.path.normpath(old_full_path) != os.path.normpath(new_full_path)
                and os.path.isfile(old_full_path)
            ):
                try:
                    os.remove(old_full_path)
                except Exception as del_err:
                    logger.warning("Could not delete old profile pic at %s: %s", old_full_path, del_err)

        return new_relative_path

    except Exception as e:
        logger.exception("Error processing profile picture for user %s: %s", user.id, e)
        return None


def delete_user_profile_pic(user):
    """
    Safely removes the profile picture from disk when a user is deleted.
    """
    if not user:
        return

    pic_name = None
    if getattr(user, 'profile_pic', None) and user.profile_pic.name:
        pic_name = str(user.profile_pic.name)
    else:
        try:
            from .models import CustomUser
            u = CustomUser.objects.filter(id=user.id).values('profile_pic').first()
            if u and u['profile_pic']:
                pic_name = str(u['profile_pic'])
        except Exception:
            pass

    if not pic_name:
        return

    clean_path = pic_name.replace('\\', '/').lstrip('/')
    if clean_path.startswith('media/'):
        clean_path = clean_path[len('media/'):]

    full_path = os.path.join(settings.MEDIA_ROOT, os.path.normpath(clean_path))
    try:
        if os.path.isfile(full_path):
            os.remove(full_path)
    except Exception as e:
        logger.warning("Could not delete profile picture for user %s: %s", getattr(user, 'id', 'unknown'), e)

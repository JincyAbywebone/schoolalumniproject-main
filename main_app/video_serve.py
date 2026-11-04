import mimetypes
import os
import re
from django.http import StreamingHttpResponse, HttpResponse, Http404
from django.conf import settings

def range_re(range_header):
    match = re.search(r'bytes=(\d+)-(\d*)', range_header)
    if match:
        start = int(match.group(1))
        end = int(match.group(2)) if match.group(2) else None
        return start, end
    return 0, None

def serve_video(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if not os.path.exists(file_path):
        raise Http404("Video not found")

    size = os.path.getsize(file_path)
    content_type, encoding = mimetypes.guess_type(file_path)
    content_type = content_type or 'application/octet-stream'

    range_header = request.META.get('HTTP_RANGE', '').strip()
    if range_header:
        start, end = range_re(range_header)
        end = size - 1 if end is None or end >= size else end

        if start >= size:
            return HttpResponse(status=416, content_type=content_type)

        length = end - start + 1
        
        def file_iterator(file_path, offset, length, chunk_size=8192):
            with open(file_path, 'rb') as f:
                f.seek(offset)
                remaining = length
                while remaining > 0:
                    chunk = f.read(min(chunk_size, remaining))
                    if not chunk:
                        break
                    yield chunk
                    remaining -= len(chunk)

        response = StreamingHttpResponse(file_iterator(file_path, start, length), status=206, content_type=content_type)
        response['Content-Length'] = str(length)
        response['Content-Range'] = f'bytes {start}-{end}/{size}'
        response['Accept-Ranges'] = 'bytes'
        return response
    else:
        def file_iterator(file_path, chunk_size=8192):
            with open(file_path, 'rb') as f:
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    yield chunk

        response = StreamingHttpResponse(file_iterator(file_path), content_type=content_type)
        response['Content-Length'] = str(size)
        response['Accept-Ranges'] = 'bytes'
        return response

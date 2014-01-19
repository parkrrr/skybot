from util import http, hook

api_root = 'https://api.imgur.com/3/image/'


@hook.api_key('imgur')
@hook.regex(r'imgur.com/([A-z0-9]+)')
def imgur(match, api_key=None):
    request_url = api_root + match.group(1)
    results = http.get_json(request_url, headers={'Authorization': 'Client-ID ' + api_key})

    if not results['success']:
        return

    image = results['data']
    title = image['title']

    if title is None:
        return

    animated = image['animated']
    attributes = [image['type']]

    size = image['size']
    if size > 1048576:
        size_mb = size / 1048576
        size_str = str(size_mb) + 'mb'
    elif size > 1024:
        size_kb = size / 1024
        size_str = str(size_kb) + 'kb'
    else:
        size_str = str(size) + 'b'

    attributes += {size_str}

    if animated:
        attributes += {"animated"}

    title = u'%s [%s]' % (title, ', '.join(attributes))

    return title

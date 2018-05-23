from collections import namedtuple
from django.shortcuts import render

def index(request):
    '''
    Show`s project sitemap.
    '''

    Link = namedtuple('Link', ['url', 'name', 'staff_only'])
    return render(request, 'index.html', {
        'links': (
            Link(reverse('admin:index'), 'Admin', True),
            Link("/docs", 'Documentation', False),
            Link(reverse('get-bill'), 'Get a Bill API', False),
            Link(reverse('add-record'), 'Post a Call Record API', False),
        )
    })

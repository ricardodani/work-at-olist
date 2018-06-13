from collections import namedtuple
from django.shortcuts import render
from django.urls import reverse


def index(request):
    '''
    Show`s project sitemap.
    '''

    Link = namedtuple('Link', ['url', 'name', 'staff_only'])
    return render(request, 'index.html', {
        'links': (
            Link(
                "/docs/",
                'Documentation', False
            ),
            Link(
                reverse('admin:index'),
                'Admin', True
            ),
            Link(
                reverse('call_records:get-bill'),
                'Bill GET Endpoint', False
            ),
            Link(
                reverse('call_records:post-record'),
                'Call POST Endpoint', False
            ),
        )
    })

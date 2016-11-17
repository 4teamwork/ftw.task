from ftw.tabbedview.browser import listing
from ftw.table import helper
from ftw.task.browser.task import getUserInfos
from ftw.task import _
from plone import api


def readable_responsible(item, persons):
    portal = api.portal.get()
    return ', '.join(
        [getUserInfos(portal, person)['name'] for person in persons])


class TaskTab(listing.CatalogListingView):
    """Lists all tasks within this context in a tabbedview listing tab.
    """

    types = ('Task',)

    sort_on = 'sortable_title'

    show_selects = False
    show_menu = False

    columns = (
        {'column': 'Title',
         'sort_index': 'sortable_title',
         'column_title': _(u'label_taskstab_title',
                           default=u'Title'),
         'transform': helper.linked},

        {'column': 'end',
         'column_title': _(u'label_taskstab_end_date',
                           default=u'End'),
         'transform': helper.readable_date_time_text,
         'width': 90},

        {'column': 'getResponsibility',
         'column_title': _(u'label_taskstab_responsibility',
                           default=u'Responsibility'),
         'transform': readable_responsible},

        {'column': 'review_state',
         'column_title': _(u'label_taskstab_review_state',
                           default=u'State'),
         'transform': helper.translated_string(),  # default is plone domain
         'width': 70},

        {'column': 'Creator',
         'column_title': _(u'label_taskstab_creator',
                           default=u'Creator'),
         'transform': helper.readable_author},
    )

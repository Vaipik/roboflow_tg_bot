from bot.utils.paginator import get_pages


def test_get_pages():
    items_per_page = 6

    total_items = 23
    assert get_pages(total_items, items_per_page) == 4

    total_items = 24
    assert get_pages(total_items, items_per_page) == 4

    total_items = 25
    assert get_pages(total_items, items_per_page) == 5

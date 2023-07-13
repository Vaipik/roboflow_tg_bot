def get_pages(total_items: int, items_per_page: int) -> int:
    """
    Implement pagioation.

    :param items_per_page: items per one page.
    :param total_items: total items amount. Required to obtain total pages.
    :return: tuple with items_per_page and total_pages
    """
    if not (total_items % items_per_page):
        return total_items // items_per_page

    return (total_items // items_per_page) + 1

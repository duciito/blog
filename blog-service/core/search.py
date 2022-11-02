from django.db.models import Q


def filter_articles(queryset, search_expression):
    """A utility that does a model-wide search for an expression in articles."""
    search_expression = search_expression.lower()
    return queryset.filter(
        Q(title__icontains=search_expression)
        # TODO: Debate if that's a good idea to look for term in text.
        | Q(text__icontains=search_expression)
        | Q(posted_at__iregex=search_expression)
    )


def filter_categories(queryset, search_expression):
    """A utility that does a model-wide search for an expression in categories."""
    search_expression = search_expression.lower()
    return queryset.filter(
        name__icontains=search_expression
    )


def filter_users(queryset, search_expression):
    """A utility that does a model-wide search for an expression in users."""
    search_expression = search_expression.lower()
    return queryset.filter(
        Q(username__icontains=search_expression)
        | Q(first_name__icontains=search_expression)
        | Q(last_name__icontains=search_expression)
        | Q(profile_description__icontains=search_expression)
    )

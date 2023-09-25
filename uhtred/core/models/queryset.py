from random import randint

from django.db.models.query import QuerySet


def get_queryset_random_entries(queryset: QuerySet, qtt: int = 1) -> list | QuerySet:
    assert qtt >= 1
    count = queryset.count()
    if count > 0 and count > qtt:
        added: list = []
        while len(added) < qtt:
            next_index = randint(0, count - 1)
            obj = queryset[next_index]
            if obj not in added:
                added.append(obj)
        return added
    return queryset

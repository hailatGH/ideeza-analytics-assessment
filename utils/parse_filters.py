import json

from django.db.models import Q


def parse_dynamic_filters(filters):
    """
    Parse a nested dict of filters into django Q objects.
    """
    if not filters:
        return Q()

    if isinstance(filters, str):
        try:
            filters = json.loads(filters)
        except json.JSONDecodeError:
            return Q()

    def build_q(data):
        if not isinstance(data, dict):
            return Q()

        for key, value in data.items():
            if key == "and":
                q = Q()
                for item in value:
                    # recursively build Q for each item and combine with AND, e.g.,
                    # ?filters={"and": [{"eq": {"author__username": "michael"}}, {"created_at__gt": "2023-01-01"}]}
                    # -> Q(author__username="michael") & Q(created_at__gt="2023-01-01")
                    q &= build_q(item)
                return q
            elif key == "or":
                q = Q()
                for item in value:
                    # recursively build Q for each item and combine with OR, e.g.,
                    # ?filters={"or": [{"eq": {"author__username": "michael"}}, {"eq": {"author__username": "eva"}}]}
                    # -> Q(author__username="michael") | Q(author__username="eva")
                    q |= build_q(item)
                return q
            elif key == "not":
                # recursively build Q for the item and negate it, e.g.,
                # ?filters={"not": {"eq": {"author__username": "michael"}}} -> ~Q(author__username="michael")
                return ~build_q(value)
            elif key == "eq":
                # e.g., ?filters={"eq": {"author__username": "michael"}}
                # -> {"author__username": "michael"}  -> Q(author__username="michael")
                return Q(**value)
            else:
                # e.g., ?filters={"created_at__gt": "2023-01-01"}
                # -> Q(created_at__gt="2023-01-01")
                return Q(**{key: value})
        return Q()

    return build_q(filters)

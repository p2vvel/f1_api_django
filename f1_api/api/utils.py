from django.core.cache import cache


from django.db.models import  Q


def q_or(q_objects: list[Q]) -> Q:
    """
    Return result of logical OR executed on Q objects from list

    Args:
        q_objects (list[Q]): list of Q objects to execute OR on

    Returns:
        Q: result of logical OR executed on Q objects from list
    """
    try:
        condition = q_objects[0]
        for q in q_objects[1:]:
            condition |= q
        return condition
    except:
        return None
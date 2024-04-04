from datetime import datetime


async def invest_after_creating_entity(target, sources):
    if not sources:
        return []

    free_sum = target.full_amount - target.invested_amount
    for source in sources:
        invest_sum = min(
            free_sum, source.full_amount - source.invested_amount
        )
        target.invested_amount += invest_sum
        target.fully_invested = target.invested_amount == target.full_amount
        if target.fully_invested:
            target.close_date = datetime.utcnow()

        source.invested_amount += invest_sum
        source.fully_invested = source.invested_amount == source.full_amount
        if source.fully_invested:
            source.close_date = datetime.utcnow()

        free_sum -= invest_sum

    if target.full_amount <= target.invested_amount:
        target.fully_invested = True
        target.close_date = datetime.utcnow()

    return [target] + sources

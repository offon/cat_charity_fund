from datetime import datetime

from app.models import CharityProject, Donation


async def invest_donation(
        charity_project: CharityProject,
        donations_for_invest: list[Donation]
):
    result = []

    if charity_project.invested_amount is None:
        charity_project.invested_amount = 0
    for donation in donations_for_invest:
        project_need_for_invested = charity_project.full_amount - charity_project.invested_amount
        donation_invested = donation.full_amount - donation.invested_amount
        if project_need_for_invested > donation_invested:
            charity_project.invested_amount += donation_invested
            donation.fully_invested = True
            donation.close_date = datetime.now()
            donation.invested_amount = donation.full_amount
            result.append(donation)
        if project_need_for_invested == donation_invested:
            charity_project.invested_amount = charity_project.full_amount
            charity_project.fully_invested = True
            charity_project.close_date = datetime.now()
            donation.close_date = datetime.now()
            donation.fully_invested = True
            donation.invested_amount = donation.full_amount
            result.append(donation)
            break
        if project_need_for_invested < donation_invested:
            charity_project.invested_amount = charity_project.full_amount
            charity_project.fully_invested = True
            donation.invested_amount += project_need_for_invested
            charity_project.close_date = datetime.now()
            result.append(donation)
            break
    return result, charity_project
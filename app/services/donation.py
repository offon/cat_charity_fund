from datetime import datetime

from app.models import CharityProject, Donation


def invest_donation(
        donation: Donation,
        charity_projects: list[CharityProject]):
    result = []
    donation.invested_amount = 0
    for project in charity_projects:
        project_need_for_invested = project.full_amount - project.invested_amount
        donation_invested = donation.full_amount - donation.invested_amount
        if project_need_for_invested > donation_invested:
            project.invested_amount += donation_invested
            donation.fully_invested = True
            donation.close_date = datetime.now()
            donation.invested_amount = donation.full_amount
            result.append(project)
            break
        if project_need_for_invested == donation_invested:
            project.invested_amount = project.full_amount
            project.fully_invested = True
            project.close_date = datetime.now()
            donation.close_date = datetime.now()
            donation.fully_invested = True
            donation.invested_amount = donation.full_amount
            result.append(project)
            break
        if project_need_for_invested < donation_invested:
            project.invested_amount = project.full_amount
            project.fully_invested = True
            donation.invested_amount += project_need_for_invested
            project.close_date = datetime.now()
            result.append(project)
    return result, donation
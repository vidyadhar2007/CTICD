from report_generator import ReportGenerator


def generate_report_data():
    """
    Returns high-level structured threat intelligence report data
    for rendering in reports.html and printable executive views.
    """
    report = ReportGenerator.generate_executive_report()
    return report

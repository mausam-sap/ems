import calendar
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer

def generate_payslip_pdf(buffer, pr):
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("EMPLOYEE MANAGEMENT SYSTEM", styles['Title']))
    elements.append(Paragraph("Pay Slip", styles['Heading2']))
    elements.append(Spacer(1, 12))

    month_name = calendar.month_name[pr.month]
    emp = pr.employee

    info_data = [
        ["Employee ID", emp.employee_id, "Name", emp.full_name],
        ["Department", str(emp.department or '-'), "Designation", emp.designation],
        ["Pay Period", f"{month_name} {pr.year}", "Generated On", pr.generated_on.strftime('%d-%m-%Y')],
    ]
    info_table = Table(info_data, colWidths=[100, 150, 100, 150])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 20))

    salary_data = [
        ["Earnings", "Amount (₹)", "Deductions", "Amount (₹)"],
        ["Basic Salary", f"{pr.basic_salary:,.2f}", "Attendance Deduction", f"{pr.deductions:,.2f}"],
        ["Bonus", f"{pr.bonus:,.2f}", "", ""],
        ["", "", "", ""],
        ["Gross Pay", f"{pr.basic_salary + pr.bonus:,.2f}", "Total Deductions", f"{pr.deductions:,.2f}"],
    ]
    sal_table = Table(salary_data, colWidths=[150, 100, 150, 100])
    sal_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#343a40')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BACKGROUND', (0, 4), (-1, 4), colors.lightgrey),
        ('FONTNAME', (0, 4), (-1, 4), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(sal_table)
    elements.append(Spacer(1, 16))

    net_data = [["NET SALARY", f"₹ {pr.net_salary:,.2f}"]]
    net_table = Table(net_data, colWidths=[350, 150])
    net_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#198754')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 14),
        ('PADDING', (0, 0), (-1, -1), 10),
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
    ]))
    elements.append(net_table)
    elements.append(Spacer(1, 20))
    elements.append(Paragraph("Attendance Summary", styles['Heading3']))
    att_data = [
        ["Working Days", "Present Days", "Absent Days"],
        [str(pr.working_days), str(pr.present_days), str(pr.working_days - pr.present_days)],
    ]
    att_table = Table(att_data, colWidths=[166, 166, 166])
    att_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0d6efd')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(att_table)
    elements.append(Spacer(1, 30))
    elements.append(Paragraph("This is a computer-generated payslip and does not require a signature.", styles['Italic']))

    doc.build(elements)

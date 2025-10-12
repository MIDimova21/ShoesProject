from flask import Blueprint, render_template, redirect, url_for, request, flash, session, make_response
from flask_login import current_user, login_required
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from io import BytesIO
import datetime

from FlaskProject.services.catalog_service import Products
from FlaskProject.services import cart_service, order_service

cart_bp = Blueprint("cart", __name__)


@cart_bp.route("/cart")
@login_required
def show_cart():
    cart_items = cart_service.get_cart()

    products_in_cart = []
    for item in cart_items:
        product = Products.query.get(item["product_id"])
        if product:
            products_in_cart.append({
                "product": product,
                "size": item["size"],
                "quantity": item.get("quantity", 1)
            })

    return render_template("cart.html", cart_items=products_in_cart)


@cart_bp.route("/cart/add/<int:product_id>", methods=["POST"])
@login_required
def add_to_cart(product_id):
    size = request.form.get("size")
    if not size:
        flash("Моля, изберете размер!")
        return redirect(url_for("catalog.show_catalog"))

    product = Products.query.get(product_id)
    if not product:
        flash("Продуктът не съществува.")
        return redirect(url_for("catalog.show_catalog"))

    cart_service.add_to_cart(product.product_id, size)

    return redirect(url_for("catalog.show_catalog"))


@cart_bp.route("/cart/export-pdf")
@login_required
def export_cart_pdf():
    cart_items = cart_service.get_cart()

    if not cart_items:
        flash("Количката ви е празна.")
        return redirect(url_for("cart.show_cart"))

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)

    elements = []

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#9742b8'),
        spaceAfter=30,
        alignment=TA_CENTER
    )

    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#1f2937'),
        spaceAfter=12
    )

    normal_style = styles['Normal']

    elements.append(Paragraph("ShoeBox - Order", title_style))
    elements.append(Spacer(1, 12))

    order_number = f"ORD-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    order_date = datetime.datetime.now().strftime('%d.%m.%Y %H:%M')

    elements.append(Paragraph(f"<b>Order number:</b> {order_number}", normal_style))
    elements.append(Paragraph(f"<b>Date:</b> {order_date}", normal_style))
    elements.append(Paragraph(f"<b>Client info:</b> {current_user.first_name} {current_user.last_name}", normal_style))
    elements.append(Paragraph(f"<b>Email:</b> {current_user.email}", normal_style))
    elements.append(Spacer(1, 20))

    elements.append(Paragraph("Order details", heading_style))

    table_data = [['Nº', 'Product', 'Size', 'Quantity', 'Price', 'Total amount']]

    total_items = 0
    total_price = 0.0

    for idx, item in enumerate(cart_items, 1):
        product = Products.query.get(item["product_id"])
        if product:
            quantity = item.get("quantity", 1)
            item_total = product.price * quantity
            total_items += quantity
            total_price += item_total

            table_data.append([
                str(idx),
                product.name,
                item["size"],
                str(quantity),
                f"{product.price} lv",
                f"{item_total} lv"
            ])

    table = Table(table_data, colWidths=[0.5 * inch, 2 * inch, 1 * inch, 0.8 * inch, 1 * inch, 1 * inch, 1.2 * inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#9742b8')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')])
    ]))

    elements.append(table)
    elements.append(Spacer(1, 20))

    summary_style = ParagraphStyle(
        'Summary',
        parent=styles['Normal'],
        fontSize=12,
        alignment=TA_RIGHT,
        spaceAfter=6
    )

    elements.append(Paragraph(f"<b>Total number of items:</b> {total_items} ", summary_style))
    elements.append(Paragraph(f"<b>Total amount:</b> {total_price:.2f} lv", summary_style))
    elements.append(Spacer(1, 30))

    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.grey,
        alignment=TA_CENTER
    )
    elements.append(Paragraph("Thank you for the order!", footer_style))
    elements.append(Paragraph("ShoeBox © 2025", footer_style))

    doc.build(elements)

    pdf = buffer.getvalue()
    buffer.close()

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=porachka_{order_number}.pdf'

    return response


@cart_bp.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    if request.method == "POST":
        address = request.form.get("address")
        payment = request.form.get("payment")

        order = order_service.create_order(current_user.user_id, address, payment)
        if order:
            flash("Успешна поръчка!")
            return redirect(url_for("catalog.show_catalog"))
        else:
            flash("Количката ви е празна или продуктите нямат наличност.")

    return render_template("checkout.html")
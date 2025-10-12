from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required

from FlaskProject import db
from FlaskProject.services.review_service import Review
from FlaskProject.services.catalog_service import Products

review_bp = Blueprint('review', __name__)

@review_bp.route("/product/<int:product_id>")
def product_detail(product_id):
    product = Products.query.get_or_404(product_id)
    reviews = Review.query.filter_by(product_id=product_id).order_by(Review.created_at.desc()).all()

    avg_rating = 0
    if reviews:
        avg_rating = sum([r.rating for r in reviews]) / len(reviews)

    return render_template(
        "product_detail.html",
        product=product,
        reviews=reviews,
        avg_rating=avg_rating,
        reviews_count=len(reviews),
        current_user=current_user
    )


@review_bp.route("/product/<int:product_id>/review", methods=['POST'])
@login_required
def add_review(product_id):
    product = Products.query.get_or_404(product_id)

    rating = request.form.get("rating", type=int)
    comment = request.form.get("comment", "").strip()

    if not rating or rating < 1 or rating > 5:
        flash("Моля, изберете рейтинг от 1 до 5 звезди.")
        return redirect(url_for("review.product_detail", product_id=product_id))

    existing_review = Review.query.filter_by(
        user_id=current_user.user_id,
        product_id=product_id
    ).first()

    if existing_review:
        flash("Вече сте оставили ревю за този продукт.")
        return redirect(url_for("review.product_detail", product_id=product_id))

    review = Review(
        user_id=current_user.user_id,
        product_id=product_id,
        rating=rating,
        comment=comment
    )

    db.session.add(review)
    db.session.commit()

    flash("Вашето ревю беше добавено успешно!")
    return redirect(url_for("review.product_detail", product_id=product_id))


from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models import db
from app.models.distributor import Distributor

distributor_bp = Blueprint("distributor", __name__)

@distributor_bp.route("/")
@login_required
def list_distributors():
    try:
        distributors = Distributor.query.all()
        return render_template("distributors/list.html", distributors=distributors)
    except Exception as e:
        # Handle the error (e.g., log it, flash a message, etc.)
        flash("Error retrieving distributors.", "error")
        # Consider logging the error: logger.error(f"Error retrieving distributors: {e}")
        return render_template("distributors/list.html", distributors=[])

@distributor_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_distributor():
    if request.method == "POST":
        try:
            name = request.form["name"]
            contact = request.form["contact"]
            type_ = request.form["type"]

            distributor = Distributor(name=name, contact=contact, type=type_)
            db.session.add(distributor)
            db.session.commit()
            flash("Distributor added successfully!", "success")
            return redirect(url_for("distributor.list_distributors"))
        except Exception as e:
            db.session.rollback()
            flash("Error adding distributor.", "error")
            # Consider logging the error: logger.error(f"Error adding distributor: {e}")

    return render_template("distributors/add.html")

@distributor_bp.route("/edit/<int:distributor_id>", methods=["GET", "POST"])
@login_required
def edit_distributor(distributor_id):
    distributor = Distributor.query.get_or_404(distributor_id)

    if request.method == "POST":
        try :
            distributor.name = request.form["name"]
            distributor.contact = request.form["contact"]
            distributor.type = request.form["type"]

            db.session.commit()
            flash("Distributor updated successfully!", "success")
            return redirect(url_for("distributor.list_distributors"))
        except Exception as e:
            db.session.rollback()
            flash("Error updating distributor.", "error")
            # Consider logging the error: logger.error(f"Error updating distributor: {e}")

    return render_template("distributors/edit.html", distributor=distributor)

@distributor_bp.route("/delete/<int:distributor_id>", methods=["DELETE"])
@login_required
def delete_distributor(distributor_id):
    try:
        distributor = Distributor.query.get_or_404(distributor_id)
        db.session.delete(distributor)
        db.session.commit()
        flash("Distributor deleted successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash("Error deleting distributor.", "error")
        # Consider logging the error: logger.error(f"Error deleting distributor: {e}")
    return redirect(url_for("distributor.list_distributors"))
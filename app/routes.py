from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from urllib.parse import urlsplit
from datetime import datetime, timedelta
from app import db
from app.models import User, Client, Case
from app.forms import LoginForm, ClientForm, CaseForm
from sqlalchemy import or_

bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    # Dashboard
    today = datetime.now().date()
    next_week = today + timedelta(days=7)

    upcoming_hearings = Case.query.filter(
        Case.next_hearing_date >= today,
        Case.next_hearing_date <= next_week
    ).order_by(Case.next_hearing_date).all()

    # Grouping by date is requested, but list is fine for now.
    # We can group in template or python.

    active_count = Case.query.filter_by(status='Active').count()
    closed_count = Case.query.filter_by(status='Closed').count()

    return render_template('dashboard.html', title='Dashboard',
                           upcoming_hearings=upcoming_hearings,
                           active_count=active_count,
                           closed_count=closed_count,
                           today=today,
                           tomorrow=today + timedelta(days=1))

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('main.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/clients')
@login_required
def clients():
    search = request.args.get('search', '')
    if search:
        clients = Client.query.filter(
            or_(
                Client.name.contains(search),
                Client.contact_details.contains(search)
            )
        ).all()
    else:
        clients = Client.query.all()
    return render_template('clients/list.html', title='Clients', clients=clients)

@bp.route('/client/new', methods=['GET', 'POST'])
@login_required
def new_client():
    form = ClientForm()
    if form.validate_on_submit():
        client = Client(name=form.name.data,
                        contact_details=form.contact_details.data,
                        notes=form.notes.data)
        db.session.add(client)
        db.session.commit()
        flash('Client added!')
        return redirect(url_for('main.clients'))
    return render_template('clients/form.html', title='New Client', form=form)

@bp.route('/client/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_client(id):
    client = db.session.get(Client, id)
    if not client:
        flash('Client not found')
        return redirect(url_for('main.clients'))
    form = ClientForm(obj=client)
    if form.validate_on_submit():
        client.name = form.name.data
        client.contact_details = form.contact_details.data
        client.notes = form.notes.data
        db.session.commit()
        flash('Client updated!')
        return redirect(url_for('main.clients'))
    return render_template('clients/form.html', title='Edit Client', form=form)

@bp.route('/cases')
@login_required
def cases():
    # Filter logic
    search = request.args.get('search', '')
    query = Case.query
    if search:
        query = query.join(Client).filter(
            or_(
                Case.case_number.contains(search),
                Case.court_name.contains(search),
                Client.name.contains(search),
                Case.status.contains(search)
            )
        )
    cases = query.all()
    return render_template('cases/list.html', title='Cases', cases=cases)

@bp.route('/case/new', methods=['GET', 'POST'])
@login_required
def new_case():
    form = CaseForm()
    # Populate client choices
    form.client_id.choices = [(c.id, c.name) for c in Client.query.all()]

    if form.validate_on_submit():
        case = Case(
            case_number=form.case_number.data,
            court_name=form.court_name.data,
            case_title=form.case_title.data,
            case_type=form.case_type.data,
            client_id=form.client_id.data,
            opponent_name=form.opponent_name.data,
            opponent_advocate=form.opponent_advocate.data,
            filing_date=form.filing_date.data,
            current_stage=form.current_stage.data,
            next_hearing_date=form.next_hearing_date.data,
            status=form.status.data,
            notes=form.notes.data
        )
        db.session.add(case)
        db.session.commit()
        flash('Case added!')
        return redirect(url_for('main.cases'))
    return render_template('cases/form.html', title='New Case', form=form)

@bp.route('/case/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_case(id):
    case = db.session.get(Case, id)
    if not case:
        flash('Case not found')
        return redirect(url_for('main.cases'))
    form = CaseForm(obj=case)
    form.client_id.choices = [(c.id, c.name) for c in Client.query.all()]

    if form.validate_on_submit():
        form.populate_obj(case)
        db.session.commit()
        flash('Case updated!')
        return redirect(url_for('main.cases'))
    return render_template('cases/form.html', title='Edit Case', form=form)

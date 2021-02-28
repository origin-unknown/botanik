from .. import db
from .models import Bot

from flask import (
    Blueprint,
    current_app,
    redirect,
    render_template,
    request,
    url_for
)

blueprint = Blueprint(
    'bots',
    __name__,
    template_folder='../templates/bots',
    url_prefix='/bots'
)

@blueprint.route('/')
def index():
    bots = Bot.query.all()
    return render_template('bots/index.html', **locals())

@blueprint.route('/new', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        bot = Bot(
            name=request.form['name'],
            command=request.form['command']
        )
        db.session.add(bot)
        db.session.commit()
        return redirect(url_for('.index'))
    return render_template('bots/create.html', **locals())

@blueprint.route('/<int:id>')
def show(id):
    bot = Bot.query.get_or_404(id)
    return render_template('bots/show.html', **locals())

@blueprint.route('/<int:id>/edit', methods=['GET', 'POST'])
def update(id):
    bot = Bot.query.get_or_404(id)
    if request.method == 'POST':
        bot.name=request.form['name']
        bot.command=request.form['command']
        db.session.commit()
        return redirect(url_for('.index'))
    return render_template('bots/edit.html', **locals())

@blueprint.route('/<int:id>/delete', methods=['POST', 'DELETE'])
def delete(id):
    bot = Bot.query.get_or_404(id)
    if bot.is_running: bot.kill()
    db.session.delete(bot)
    db.session.commit()
    return redirect(url_for('.index'))

@blueprint.route('/<int:id>/launch', methods=['POST'])
def launch(id):
    bot = Bot.query.get_or_404(id)
    bot.launch()
    return redirect(request.referrer)

@blueprint.route('/<int:id>/kill', methods=['POST'])
def kill(id):
    bot = Bot.query.get_or_404(id)
    bot.kill()
    return redirect(request.referrer)

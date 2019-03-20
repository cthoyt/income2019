# -*- coding: utf-8 -*-

"""Web interface for ``table_validator``."""

import logging
import os

from flask import Flask, current_app, flash, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms.fields import SubmitField
from wtforms.validators import DataRequired

from table_validator.api import parse_tsv, validate

logger = logging.getLogger(__name__)


class MyForm(FlaskForm):
    """A form for uploading a file."""

    candidate = FileField('Candidate File', validators=[DataRequired()])
    submit = SubmitField('Upload')

    def validate_table_template(self) -> bool:
        """Validate the file against the table template in the current app."""
        candidate = parse_tsv(self.candidate.data.stream.read().decode("utf-8").splitlines())
        return current_app.config['table_validator'].validate(candidate)


app = Flask(__name__)
app.secret_key = os.urandom(8)

# Add the Flask-Bootstrap extension
Bootstrap(app)


@app.route('/', methods=['GET', 'POST'])
def home():
    """Serve the upload page."""
    if 'table_template' not in app.config:
        raise ValueError('``table_template`` is not configured')

    form = MyForm()

    if not form.validate_on_submit():
        return render_template('index.html', form=form)

    valid = form.validate_table_template()
    flash(f'Form is valid: {valid}')
    return render_template('index.html', form=form)

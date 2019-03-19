# -*- coding: utf-8 -*-

import logging
import os

from flask import Flask, flash, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms.fields import SubmitField
from wtforms.validators import DataRequired

from table_validator.api import parse_tsv, validate

logger = logging.getLogger(__name__)

with open('/Users/cthoyt/dev/income2019/tests/simple_template.tsv') as file:
    template = parse_tsv(file)


class MyForm(FlaskForm):
    """A form for uploading a file."""

    candidate = FileField('Candidate File', validators=[DataRequired()])
    submit = SubmitField('Upload')

    def validate_table_template(self) -> bool:
        candidate = parse_tsv(self.candidate.data.stream.read().decode("utf-8").splitlines())
        return validate(template, candidate)


app = Flask(__name__)
app.secret_key = os.urandom(8)

# Add the Flask-Bootstrap extension
Bootstrap(app)


@app.route('/', methods=['GET', 'POST'])
def home():
    """Serve the home page."""
    form = MyForm()

    if not form.validate_on_submit():
        return render_template('index.html', form=form)

    valid = form.validate_table_template()
    flash(f'Form is valid: {valid}')
    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email


# Reset password form
class CompetitionInsertForm(FlaskForm):
    comp_title = StringField('Competition Title', validators=[DataRequired()])
    comp_subtitle = StringField('Subtitle')
    comp_range = StringField('Duration', validators=[DataRequired()])
    comp_url = StringField('Competition Url', validators=[DataRequired()])
    comp_description = StringField('Competition Description')
    comp_host_name = StringField('Competition Hostname', validators=[DataRequired()])
    comp_host_url = StringField('Competition Host Url', validators=[DataRequired()])
    prize_currency = StringField('Currency Type')
    prize_amount = StringField('Prize')
    deadline = StringField('Competition Deadline', validators=[DataRequired()])
    timezone = StringField('Timezone', validators=[DataRequired()])
    comp_scenario = StringField('Competition Scenario')
    data_feature = StringField('Data Feature')
    submit = SubmitField('Submit')

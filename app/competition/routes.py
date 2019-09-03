from app import app
from flask import render_template, url_for, redirect
from app.competition.forms import CompetitionInsertForm
from func_pack import get_api_info
from config import Config
from app.competition import bp
import requests


# ------------ Competition Routing -------------- #
# competition inserting
@bp.route('/competition-inserting', methods=['GET'])
def competition_inserting_view():
    form = CompetitionInsertForm()
    return render_template('competition/compInsert.html', form=form)


# my competition list
@bp.route('/competition-list/<string:uid>', methods=['GET'])
def competition_list_view(uid):
    own_competition_url = 'http://' + Config.COMPETITION_SERVICE_URL + \
                          '/api/competition/contributor-id/' + str(uid)
    result = requests.get(own_competition_url)
    if result.status_code == 200:
        owner_comps_list = get_api_info(result)
        return render_template('competition/compOpers.html', comp_list=owner_comps_list)



# # competition updating
# @bp.route('/competition-updating', methods=['GET'])
# def competition_updating_view():




from app import app
from flask import render_template, url_for, redirect, jsonify
from app.competition.forms import CompetitionInsertForm, CompetitionUpdateForm, CompetitionDeleteForm
from werkzeug.http import HTTP_STATUS_CODES
from func_pack import get_api_info, get_current_datetime
from config import Config
from app.competition import bp
import requests


# ------------ Competition Routing -------------- #
# competition inserting
@bp.route('/competition-inserting', methods=['GET'])
def competition_inserting_view():
    form = CompetitionInsertForm()
    return render_template('competition/compInsert.html', form=form)


# competition inserting function
@bp.route('/competition-inserting', methods=['POST'])
def competition_inserting_function():
    form = CompetitionInsertForm()
    if form.validate_on_submit():
        insert_url = 'http://' + Config.COMPETITION_SERVICE_URL + \
            '/api/competition'
        new_competition = dict()

        new_competition['comp_title'] = form.comp_title.data
        new_competition['comp_subtitle'] = form.comp_subtitle.data
        new_competition['comp_range'] = form.comp_range.data
        new_competition['comp_url'] = form.comp_url.data
        new_competition['prize_currency'] = form.prize_currency.data
        new_competition['prize_amount'] = form.prize_amount.data
        new_competition['deadline'] = form.deadline.data
        new_competition['timezone'] = form.timezone.data
        new_competition['update_time'] = get_current_datetime()
        new_competition['publish_time'] = get_current_datetime()
        new_competition['contributor_id'] = '233'

        new_competition['comp_description'] = form.comp_description.data
        host_list = [{'comp_host_name': form.comp_host_name.data, 'comp_host_url': form.comp_host_url.data}]
        new_competition['comp_host'] = str(host_list)

        comp_scenario_list = [str(form.comp_scenario.data)]
        new_competition['comp_scenario'] = str(comp_scenario_list)
        data_feature = [str(form.data_feature.data)]
        new_competition['data_feature'] = str(data_feature)

        result = requests.post(insert_url, data=new_competition)
        if result.status_code == 200:
            competition = get_api_info(result)[0]
            comp_record_hash = competition['comp_record_hash']
            return redirect(url_for('competition-operator.competition_detail_view', comp_record_hash=comp_record_hash))


# my competition list
@bp.route('/competition-list/<string:user_id>', methods=['GET'])
def competition_list_view(user_id):
    # ToDo: Auth recognization
    own_competition_url = 'http://' + Config.COMPETITION_SERVICE_URL + \
                          '/api/competition/contributor-id/' + str(user_id)
    result = requests.get(own_competition_url)
    if result.status_code == 200:
        owner_comps_list = get_api_info(result)
        return render_template('competition/compMenu.html', comp_list=owner_comps_list)


# competition detail view
@bp.route('/competition-detail/<string:comp_record_hash>', methods=['GET'])
def competition_detail_view(comp_record_hash):
    comp_url = 'http://' + Config.COMPETITION_SERVICE_URL + \
               '/api/competition/competition-record-hash/' + str(comp_record_hash)
    result = requests.get(comp_url)
    if result.status_code == 200:
        competition = get_api_info(result)[0]
        return render_template('competition/compView.html', competition=competition)


# competition update page
@bp.route('/competition-updating/<string:comp_record_hash>', methods=['GET'])
def competition_updating_view(comp_record_hash):
    # ToDo: Auth recognization
    comp_url = 'http://' + Config.COMPETITION_SERVICE_URL + \
               '/api/competition/competition-record-hash/' + str(comp_record_hash)
    result = requests.get(comp_url)
    if result.status_code == 200:
        competition = get_api_info(result)[0]
        form = CompetitionUpdateForm()
        form.comp_title.data = competition['comp_title']
        form.comp_subtitle.data = competition['comp_subtitle']
        form.comp_range.data = competition['comp_range']
        form.comp_url.data = competition['comp_url']
        form.comp_description.data = competition['comp_description']
        form.comp_host_name.data = competition['comp_host'][0]['comp_host_name']
        form.comp_host_url.data = competition['comp_host'][0]['comp_host_url']
        form.prize_currency.data = competition['prize_currency']
        form.prize_amount.data = competition['prize_amount']
        form.deadline.data = competition['deadline']
        form.timezone.data = competition['timezone']
        form.comp_scenario.data = competition['comp_scenario'][0]
        form.data_feature.data = competition['data_feature'][0]
        return render_template('competition/compUpdate.html', form=form)


# competition update post
@bp.route('/competition-updating/<string:comp_record_hash>', methods=['POST'])
def competition_updating_function(comp_record_hash):
    form = CompetitionUpdateForm()
    # ToDo: Auth recognization
    if form.validate_on_submit():
        # Get competition info
        comp_url = 'http://' + Config.COMPETITION_SERVICE_URL + \
                   '/api/competition/competition-record-hash/' + str(comp_record_hash)
        result = requests.get(comp_url)
        if result.status_code == 200:
            mod_competition = get_api_info(result)[0]

            # Update Info
            update_url = 'http://' + Config.COMPETITION_SERVICE_URL + \
                '/api/competition/competition-record-hash/' + comp_record_hash

            mod_competition['comp_title'] = form.comp_title.data
            mod_competition['comp_subtitle'] = form.comp_subtitle.data
            mod_competition['comp_range'] = form.comp_range.data
            mod_competition['comp_url'] = form.comp_url.data
            mod_competition['prize_currency'] = form.prize_currency.data
            mod_competition['prize_amount'] = form.prize_amount.data
            mod_competition['deadline'] = form.deadline.data
            mod_competition['timezone'] = form.timezone.data
            mod_competition['update_time'] = get_current_datetime()

            mod_competition['comp_description'] = form.comp_description.data
            host_list = [{'comp_host_name': form.comp_host_name.data, 'comp_host_url': form.comp_host_url.data}]
            mod_competition['comp_host'] = str(host_list)

            comp_scenario_list = [str(form.comp_scenario.data)]
            mod_competition['comp_scenario'] = str(comp_scenario_list)
            data_feature = [str(form.data_feature.data)]
            mod_competition['data_feature'] = str(data_feature)

            result = requests.put(update_url, data=mod_competition)
            if result.status_code == 200:
                user_id = get_api_info(result)[0]['contributor_id']
                return redirect(url_for('competition-operator.competition_detail_view',
                                        comp_record_hash=mod_competition['comp_record_hash']))


# competition delete view
@bp.route('/competition-deleting/<string:comp_record_hash>', methods=['GET', 'POST'])
def competition_delete_confirm(comp_record_hash):
    form = CompetitionDeleteForm()
    # Get competition info
    comp_url = 'http://' + Config.COMPETITION_SERVICE_URL + \
               '/api/competition/competition-record-hash/' + str(comp_record_hash)
    result = requests.get(comp_url)
    # Functional Part
    if form.validate_on_submit():
        if result.status_code == 200:
            # ToDo: Auth recognization
            user_id = get_api_info(result)[0]['contributor_id']
            delete_url = 'http://' + Config.COMPETITION_SERVICE_URL + \
                         '/api/competition/competition-record-hash/' + str(comp_record_hash)
            requests.delete(delete_url)
            return redirect(url_for('competition-operator.competition_list_view', user_id=user_id))
    # View Part
    else:
        if result.status_code == 200:
            # ToDo: Auth recognization
            competition = get_api_info(result)[0]
            return render_template('competition/compDelete.html', form=form, competition=competition)


# # competition delete function
# @bp.route('/competition-deleting/<string:comp_record_hash>', methods=['DELETE'])
# def competition_deleting_function(comp_record_hash):
#     comp_url = 'http://' + Config.COMPETITION_SERVICE_URL + \
#                '/api/competition/competition-record-hash/' + str(comp_record_hash)
#     result = requests.get(comp_url)
#     if result.status_code == 200:
#         user_id = get_api_info(result)[0]
#         delete_url = 'http://' + Config.COMPETITION_SERVICE_URL + \
#             '/api/competition/competition-record-hash/' + str(comp_record_hash)
#         result = requests.delete(delete_url)
#         if result == 200:
#             return redirect(url_for('competition-operator.competition_list_view', user_id=user_id))


# bad requests holder
def bad_request(message):
    return error_response(400, message)


# error response
def error_response(status_code, message=None):
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response

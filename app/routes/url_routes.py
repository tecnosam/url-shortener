from flask import Blueprint, redirect, request, abort, Response

from app.models.urls import URL, URLShema

blueprint = Blueprint('url_blueprint', __name__, url_prefix='/url')

url_schema = URLShema()

@blueprint.route("/add", methods=['POST'])
def add_url():
    url = request.form['url']

    _url: URL = URL.add(url)

    response = url_schema.dump(_url)

    return response

@blueprint.route("/<url_endpoint>", methods=['GET'])
def work_endpoint(url_endpoint):
    
    _url: URL = URL.query.filter_by(endpoint=url_endpoint)

    if _url is None:
        abort(Response("URL not found", 404))

    return redirect(_url.real_link)

@blueprint.route("/<url_id>/edit", methods=['PUT', 'DELETE'])
def edit_url(url_id):
    _url: URL = URL.query.get(url_id)

    if _url is None:
        abort(Response("URL not found", 404))

    if request.method == 'PUT':
        new_url = request.form['url']

        _url = _url.change_url(new_url)

    else:
        _url = _url.pop()

    return url_schema.dump(_url)

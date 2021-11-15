import os
from random import randint
import redis
from shortener import app
from flasgger import swag_from

from flask import send_file
from flask import request, jsonify
from flask import render_template, redirect

print(os.environ.get("REDIS_HOST"))
r = redis.Redis(host=os.environ.get("REDIS_HOST", "123:45"),
                port=int(os.environ.get("REDIS_PORT", "6379")))
r = redis.StrictRedis(decode_responses=True)
print('Redis connected', r.ping())

long_url_field = 'long_url'
visits_field = 'visits'


@ app.route('/', methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST' and request.form['url']:
        url_to_redirect = request.host_url + \
            'shorten?url=' + request.form['url']
        return redirect(url_to_redirect)
    return render_template('homepage.html'), 200


@ app.route("/shorten", methods=['GET'])
@ swag_from('docs/shorten.yml')
def shorten_url():
    long_url = request.args.get('url', None)

    if not long_url:
        return send_file('templates/index.html')

    # TODO
    if long_url.startswith(request.host_url):
        return jsonify({
            'success': False,
            'error': app.config['MSG_ALREADY_SHORT_URL']
        }), 400

    if r.exists(long_url):
        short_id = r.get(long_url)
        visits = r.hget(short_id, visits_field)
        return jsonify({
            'success': True,
            'long_url': long_url,
            'id': short_id,
            'short_url': request.host_url + short_id,
            'visits': visits
        }), 200

    short_id = shorten(long_url)

    # make sure this is a unique short url
    while r.hexists(short_id, long_url_field):
        short_id = shorten(long_url)

    r.hset(short_id, long_url_field, long_url)
    r.hset(short_id, visits_field, 0)
    r.set(long_url, short_id)

    return jsonify({
        'success': True,
        'long_url': long_url,
        'id': short_id,
        'short_url': request.host_url + short_id,
        'visits': 0
    }), 200


@ app.route("/<short_id>", methods=['GET'])
@ swag_from('docs/redirect.yml')
def redirect_to_long_url(short_id):

    if not r.hexists(short_id, long_url_field):
        return send_file('templates/unknown.html'), 404

    long_url = r.hget(short_id, long_url_field)

    # increment the number of visits to this url
    r.hincrby(short_id, visits_field, 1)
    return redirect(long_url), 302


@ app.route("/<short_id>/detail", methods=['GET'])
@ swag_from('docs/url_detail.yml')
def get_detail_from_short_url(short_id):

    if not r.hexists(short_id, long_url_field):
        return jsonify({
            'success': False,
            'error': app.config['MSG_UNKNOWN_SHORT_URL']
        }), 400

    long_url = r.hget(short_id, long_url_field)

    # increment the number of visits to this url
    r.hincrby(short_id, visits_field, 1)
    visits = r.hget(short_id, visits_field)

    return jsonify({
        'success': True,
        'long_url': long_url,
        'id': short_id,
        'short_url': request.host_url + short_id,
        'visits': visits
    }), 200


@ app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


##

valid_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
# Algorithm to generate alias based on 62 characters [a-Z, 0-9] using pseudorandom numbers.


def shorten(long_url, n=8):
    short_id = ""
    for i in range(n):
        index = randint(0, len(valid_chars)-1)
        short_id += valid_chars[index]
    return short_id

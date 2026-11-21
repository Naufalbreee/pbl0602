import json
import urllib.request
import urllib.parse

SERVER_URL = "http://127.0.0.1:8000/pbl0602_server/default/cars.json"

def index():
    keyword = request.vars.keyword or ''
    url = SERVER_URL
    if keyword:
        url += "?keyword=" + urllib.parse.quote(keyword)
    req = urllib.request.urlopen(url)
    data = json.loads(req.read().decode('utf-8'))
    return dict(cars=data.get('cars', []), keyword=keyword)

def create():
    if request.env.request_method == 'POST':
        payload = json.dumps({
            'carname': request.vars.carname,
            'carbrand': request.vars.carbrand,
            'carmodel': request.vars.carmodel,
            'carprice': request.vars.carprice
        }).encode('utf-8')
        req = urllib.request.Request(SERVER_URL, data=payload, method='POST')
        req.add_header('Content-Type', 'application/json')
        urllib.request.urlopen(req)
        redirect(URL('index'))
    return dict()

def update():
    car_id = request.args(0)
    if request.env.request_method == 'POST':
        payload = json.dumps({
            'id': car_id,
            'carname': request.vars.carname,
            'carbrand': request.vars.carbrand,
            'carmodel': request.vars.carmodel,
            'carprice': request.vars.carprice
        }).encode('utf-8')
        req = urllib.request.Request(SERVER_URL, data=payload, method='PUT')
        req.add_header('Content-Type', 'application/json')
        urllib.request.urlopen(req)
        redirect(URL('index'))

    # Ambil data lama untuk ditampilkan di form edit
    req = urllib.request.urlopen(SERVER_URL)
    cars = json.loads(req.read().decode('utf-8')).get('cars', [])
    car = next((c for c in cars if str(c['id']) == str(car_id)), {})
    return dict(car=car)

def delete():
    car_id = request.args(0)
    req = urllib.request.Request(f"{SERVER_URL}/{car_id}", method='DELETE')
    urllib.request.urlopen(req)
    redirect(URL('index'))
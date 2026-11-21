import json

def index():
    return "Web2py Web Service Server Ready"

@request.restful()
def cars():
    response.view = 'generic.json'

    def GET(*args, **vars):
        keyword = vars.get('keyword', '')
        if keyword:
            query = (db.tbcarsweb.carname.contains(keyword)) | \
                    (db.tbcarsweb.carbrand.contains(keyword)) | \
                    (db.tbcarsweb.carmodel.contains(keyword)) | \
                    (db.tbcarsweb.carprice.contains(keyword))
            rows = db(query).select()
        else:
            rows = db(db.tbcarsweb).select()
        return dict(cars=rows.as_list())

    def POST(*args, **vars):
        data = json.loads(request.body.read().decode('utf-8'))
        new_id = db.tbcarsweb.insert(
            carname=data.get('carname'),
            carbrand=data.get('carbrand'),
            carmodel=data.get('carmodel'),
            carprice=data.get('carprice')
        )
        db.commit()
        return dict(status='created', id=new_id)

    def PUT(*args, **vars):
        data = json.loads(request.body.read().decode('utf-8'))
        car_id = data.get('id')
        db(db.tbcarsweb.id == car_id).update(
            carname=data.get('carname'),
            carbrand=data.get('carbrand'),
            carmodel=data.get('carmodel'),
            carprice=data.get('carprice')
        )
        db.commit()
        return dict(status='updated', id=car_id)

    def DELETE(*args, **vars):
        car_id = args[0] if args else vars.get('id')
        db(db.tbcarsweb.id == car_id).delete()
        db.commit()
        return dict(status='deleted', id=car_id)

    return dict(GET=GET, POST=POST, PUT=PUT, DELETE=DELETE)
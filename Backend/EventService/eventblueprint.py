from flask import Blueprint, request, jsonify
from database import mongo
from bson.objectid import ObjectId

eventblueprint = Blueprint('eventblueprint', __name__)

@eventblueprint.route('/', methods=['GET'])
def get_events():
    search_param = request.args.get('search')
    start = int(request.args.get('start', 0))
    limit = 20
    if search_param:
        events = mongo.db.events.find({
            '$or': [
                {'name': {'$regex': search_param, '$options': 'i'}},
                {'description': {'$regex': search_param, '$options': 'i'}}
            ]
        }).skip(start).limit(limit)
    else:
        events = mongo.db.events.find().skip(start).limit(limit)

    event_list = []
    for event in events:
        if 'image' not in event:
            event['image'] = 'default'
        event_data = {
            'id': str(event['_id']),
            'name': event['name'],
            'date': event['date'],
            'image': event['image'],
            'location': event['location'],
            'entry_fee': event['entry_fee'],
            'description': event['description'],
            'organizer': event['organizer'],
            'capacity': event['capacity']
        }
        event_list.append(event_data)
    return jsonify({'events': event_list})
    

@eventblueprint.route('/find/<id>', methods=['GET'])
def find_event(id):
    event = mongo.db.events.find_one({'_id': ObjectId(id)})
    if event:
        if 'image' not in event:
            event['image'] = 'default'
        response = {
            'name': event['name'],
            'date': event['date'],
            'image': event['image'],
            'location': event['location'],
            'entry_fee': event['entry_fee'],
            'description': event['description'],
            'organizer': event['organizer'],
            'capacity': event['capacity']
        }
        return jsonify(response)
    else:
        return jsonify({'message': 'Event not found'})
    

@eventblueprint.route('/addEvent', methods=['POST'])
def add_event():
    name = request.json['name']
    date = request.json['date']
    image= request.json['image']
    location = request.json['location']
    entry_fee = request.json['entry_fee']
    description = request.json['description']
    organizer = request.json['organizer']
    capacity = request.json['capacity']
    mongo.db.events.insert_one({
        'name': name,
        'date': date,
        'image': image,
        'location': location,
        'entry_fee': entry_fee,
        'description': description,
        'organizer': organizer,
        'capacity': capacity
    })
    return jsonify({'message': 'Event added successfully'})


@eventblueprint.route('/updateEvent/<id>', methods=['PUT'])
def update_event(id):
    event = mongo.db.events.find_one({'_id': id})
    if event:
        mongo.db.events.update_one({'_id': id}, {'$set': request.json})
        return jsonify({'message': 'Event updated successfully'})
    else:
        return jsonify({'message': 'Event not found'})
    
    
@eventblueprint.route('/deleteEvent/<id>', methods=['DELETE'])
def delete_event(id):
    event = mongo.db.events.find_one({'_id': id})
    if event:
        mongo.db.events.delete_one({'_id': id})
        return jsonify({'message': 'Event deleted successfully'})
    else:
        return jsonify({'message': 'Event not found'})

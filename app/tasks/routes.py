from flask import request, jsonify, Blueprint
from . import tasks_bp
from app.models import Task, ActivityLog
from app.extensions import db, limiter
from app.middleware.decorators import token_required
from datetime import datetime

# Validation Helper (can be a decorator)
def validate_task_data(data):
    if not data:
        return False, "No data provided"
    if 'title' not in data or not data['title'].strip():
        return False, "Title is required"
    if 'status' in data and data['status'] not in ['Pending', 'In-Progress', 'Completed']:
        return False, "Invalid status. Must be Pending, In-Progress, or Completed"
    return True, None

@tasks_bp.route('/', methods=['POST'])
@token_required
@limiter.limit("100 per minute")
def create_task(current_user):
    """
    Create a new task
    ---
    tags:
      - Tasks
    security:
      - Bearer: []
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
        description: Bearer <access_token>
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
            description:
              type: string
            status:
              type: string
              enum: [Pending, In-Progress, Completed]
    responses:
      201:
        description: Task created
    """
    data = request.get_json()
    is_valid, error = validate_task_data(data)
    if not is_valid:
        return jsonify({'message': error}), 400

    task = Task(
        title=data['title'],
        description=data.get('description', ''),
        status=data.get('status', 'Pending'),
        author=current_user
    )
    
    db.session.add(task)
    
    # Audit Log
    log = ActivityLog(user_id=current_user.id, action="Task Created", details=f"Task {task.title} created")
    db.session.add(log)
    
    db.session.commit()
    
    return jsonify({
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'status': task.status,
        'timestamp': task.timestamp.isoformat()
    }), 201

@tasks_bp.route('/', methods=['GET'])
@token_required
@limiter.limit("100 per minute")
def get_tasks(current_user):
    """
    Get all tasks for current user
    ---
    tags:
      - Tasks
    security:
      - Bearer: []
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
    responses:
      200:
        description: List of tasks
    """
    # Pagination could be added but assignment didn't explicitly ask.
    # We filter by author=current_user implicitly by querying current_user.tasks
    tasks = current_user.tasks.all() # tasks is a dynamic relationship
    
    output = []
    for task in tasks:
        output.append({
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'status': task.status,
            'timestamp': task.timestamp.isoformat()
        })
    
    return jsonify({'tasks': output}), 200

@tasks_bp.route('/<int:id>', methods=['GET'])
@token_required
@limiter.limit("100 per minute")
def get_task(current_user, id):
    """
    Get a single task by ID
    ---
    tags:
      - Tasks
    security:
      - Bearer: []
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Task details
      404:
        description: Task not found or unauthorized
    """
    # Enforce at DB query level
    task = current_user.tasks.filter_by(id=id).first_or_404(description='Task not found or unauthorized')
    
    return jsonify({
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'status': task.status,
        'timestamp': task.timestamp.isoformat()
    }), 200

@tasks_bp.route('/<int:id>', methods=['PUT'])
@token_required
@limiter.limit("100 per minute")
def update_task(current_user, id):
    """
    Update an existing task
    ---
    tags:
      - Tasks
    security:
      - Bearer: []
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
      - name: id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
            description:
              type: string
            status:
              type: string
    responses:
      200:
        description: Task updated
      404:
        description: Task not found
    """
    # Enforce at DB query level
    task = current_user.tasks.filter_by(id=id).first_or_404(description='Task not found or unauthorized')
    
    data = request.get_json()
    
    # Simple validation for update
    if 'title' in data:
        task.title = data['title']
    if 'description' in data:
        task.description = data['description']
    if 'status' in data:
        if data['status'] not in ['Pending', 'In-Progress', 'Completed']:
             return jsonify({'message': "Invalid status"}), 400
        task.status = data['status']
        
    # Audit Log
    log = ActivityLog(user_id=current_user.id, action="Task Updated", details=f"Task {task.id} updated")
    db.session.add(log)
    
    db.session.commit()
    
    return jsonify({
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'status': task.status,
        'timestamp': task.timestamp.isoformat()
    }), 200

@tasks_bp.route('/<int:id>', methods=['DELETE'])
@token_required
@limiter.limit("100 per minute")
def delete_task(current_user, id):
    """
    Delete a task
    ---
    tags:
      - Tasks
    security:
      - Bearer: []
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Task deleted
      404:
        description: Task not found
    """
    # Enforce at DB query level
    task = current_user.tasks.filter_by(id=id).first_or_404(description='Task not found or unauthorized')
        
    db.session.delete(task)
    
    # Audit Log
    log = ActivityLog(user_id=current_user.id, action="Task Deleted", details=f"Task {id} deleted")
    db.session.add(log)
    
    db.session.commit()
    
    return jsonify({'message': 'Task deleted'}), 200

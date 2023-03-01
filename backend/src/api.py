import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink, db
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

"""
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
"""
app.app_context().push()
db_drop_and_create_all()

# ROUTES
"""
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
"""


@app.get("/drinks")
def get_drinks():
    drinks = db.session.query(Drink).all()
    if drinks is None:
        abort(404)
    all_drinks = [drink.short() for drink in drinks]
    return {"success": True, "drinks": all_drinks}


"""
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
"""


@app.get("/drinks-detail")
@requires_auth("get:drinks-detail")
def get_drinks_details(jwt):
    drinks = db.session.query(Drink).all()
    if drinks is None:
        abort(404)
    all_drinks = [drink.long() for drink in drinks]
    return {"success": True, "drinks": all_drinks}


"""
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
"""


@app.post("/drinks")
@requires_auth("post:drinks")
def add_new_drink(jwt):
    data = request.get_json()

    title = data.get("title", None)
    recipe = data.get("recipe", None)
    recipe_to_josn = json.dumps(recipe)

    # if ther is no data passed donw to the api
    if len(title) == 0:
        abort(422)

    try:
        new_drink = Drink(title=title, recipe=recipe_to_josn)
        new_drink.insert()

        # read all the drinks and send back to the front end
        drinks = db.session.query(Drink).all()
        all_drinks = [drink.long() for drink in drinks]
        return {"success": True, "drinks": all_drinks}
    except:
        abort(422)


"""
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
"""


@app.patch("/drinks/<id>")
@requires_auth("patch:drinks")
def update_drink(jwt, id):
    # find the drink to update
    drink_to_update = db.session.query(Drink).filter(Drink.id == id).one_or_none()
    if drink_to_update is None:
        abort(404)

    try:
        data = request.get_json()
        title = data.get("title")
        recipe = data.get("recipe")
        recipe_to_json = json.dumps(recipe)

        drink_to_update.title = title
        drink_to_update.recipe = recipe_to_json
        drink_to_update.update()

        # get all drinks and send back to the front end
        drinks = db.session.query(Drink).all()
        all_drinks = [drink.long() for drink in drinks]

        return {"success": True, "drinks": all_drinks}
    except:
        abort(404)


"""
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
"""


@app.delete("/drinks/<id>")
@requires_auth("delete:drinks")
def delete_drink(jwt, id):
    drink_to_delete = db.session.query(Drink).filter(Drink.id == id).one_or_none()

    try:
        if drink_to_delete is None:
            abort(404)

        deleted_record_id = drink_to_delete.id
        drink_to_delete.delete()

        return {"success": True, "delete": deleted_record_id}
    except:
        abort(404)


# Error Handling
"""
Example error handling for unprocessable entity
"""


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({"success": False, "error": 422, "message": "unprocessable"}), 422


"""
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

"""

"""
@TODO implement error handler for 404
    error handler should conform to general task above
"""


@app.errorhandler(404)
def not_found(error):
    return (
        jsonify({"success": False, "error": 404, "message": "resource not found"}),
        404,
    )


"""
@TODO implement error handler for AuthError
    error handler should conform to general task above
"""


@app.errorhandler(AuthError)
def autherror(error):
    return jsonify({"success": False, "error": 401, "message": "An Authorized"})

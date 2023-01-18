from flask import Flask, jsonify, make_response, render_template, request
from database import session, Contact
import logging, json

app = Flask(__name__, template_folder="../templates", static_folder="../styles")

def register_new_contact(fname: str, lname: str, category: str, phone: str):
    contact = Contact(firstName=fname, lastName=lname, phone=phone, category=category)
    try:
        session.add(contact)
        session.commit()
    except Exception as error:
        logging.warning("While adding new Contact occured error")


def get_contacts_all():
    return session.query(Contact).all()

def get_contact_by_phone(phone: str):
    return session.query(Contact).filter_by(phone=phone)

def get_contacts_by_name(name: str, specification = "firstname"):
    if specification == "firstname":
        return session.query(Contact).filter_by(firstName=name)
    elif specification == "lastname":
        return session.query(Contact).filter_by(lastName=name)
    else:
        logging.warning("Selecting Contact by searching unspecified field name: {}".format(specification))

def get_contacts_by_fullname(fname: str, lname: str):
    return session.query(Contact).filter(
        Contact.firstName == fname,
        Contact.lastName == lname
    )

def get_contacts_by_category(category: str):
    if category in ["family", "friends", "work"]:
        return session.query(Contact).filter_by(category=category).all()
    else:
        logging.warning("Selecting Contact by searching unspecified field category: {}".format(category))


def update_fname(phone: str, new_fnmae: str):
    result = session.query(Contact).filter_by(phone=phone).update({
        Contact.firstName: new_fnmae
    })
    session.commit()
    return result

def update_lname(phone: str, new_lnmae: str):
    result = session.query(Contact).filter_by(phone=phone).update({
        Contact.lastName: new_lnmae
    })
    session.commit()
    return result

def update_category(phone: str, new_category: str):
    result = session.query(Contact).filter_by(phone=phone).update({
        Contact.category: new_category
    })
    session.commit()
    return result

def update_phone(phone: str, new_phone: str):
    result = session.query(Contact).filter_by(phone=phone).update({
        Contact.phone: new_phone
    })
    session.commit()
    return result

def delete_contact(phone: str):
    result = session.query(Contact).filter_by(phone=phone).delete()
    session.commit()
    return result

def contact_to_dict(contacts: list[Contact]):
    json_contacts = list()
    for contact in contacts:
        json_contact = {
            "firstName": contact.firstName,
            "lastName": contact.lastName,
            "phone": contact.phone,
            "category": contact.category
        }
        json_contacts.append(json_contact)
    return json_contacts


@app.route("/api/contacts/all")
def api_contacts_all():
    contacts = get_contacts_all()
    return jsonify(contact_to_dict(contacts))

@app.route("/api/contact/<phone>")
def api_contact_search(phone: str):
    contacts = get_contact_by_phone(phone).all()
    if len(contacts) == 0:
        return jsonify({"result": "not-found"})
    return jsonify(contact_to_dict(contacts))

@app.route("/api/contacts/by-name/<name>")
def api_contact_search_by_name(name: str):
    contacts = get_contacts_by_name(name).all()
    if len(contacts) == 0:
        return jsonify({"result": "not-found"})
    return jsonify(contact_to_dict(contacts))

@app.route("/api/contacts/by-fullname/<fname>/<lname>")
def api_contact_seatch_by_fullname(fname: str, lname: str):
    contacts = get_contacts_by_fullname(fname, lname).all()
    if len(contacts) == 0:
        return jsonify({"result": "not-found"})
    return jsonify(contact_to_dict(contacts))

@app.route("/api/contact/delete/<phone>")
def api_contact_delete(phone: str):
    delete_contact(phone)
    return jsonify({"result": "contact deleted"})

@app.route("/api/contact/update-fname/<phone>/<new_name>")
def api_contact_fname_update(phone: str, new_name: str):
    update_fname(phone, new_name)
    return jsonify({"result": "contact updated"})

@app.route("/api/contact/update-lname/<phone>/<new_name>")
def api_contact_lname_update(phone: str, new_name: str):
    update_lname(phone, new_name)
    return jsonify({"result": "contact updated"})

@app.route("/api/contact/update-phone/<phone>/<new_phone>")
def api_contact_phone_update(phone: str, new_phone: str):
    update_phone(phone, new_phone)
    return jsonify({"result": "contact updated"})

@app.route("/api/contact/update-category/<phone>/<category>")
def api_contact_category_update(phone: str, category: str):
    update_category(phone, category)
    return jsonify({"result": "contact updated"})

@app.route("/api/contact/create", methods=('POST',))
def api_contact_create():
    if request.method == 'POST':
        register_new_contact(fname=request.form["firstname"], lname=request.form["lastname"], category=request.form["category"], phone=request.form["phone"])
    return jsonify({"result": "contact created"})



@app.route('/')
def renderApplication():
    return render_template("index.html")

app.run(debug=True)
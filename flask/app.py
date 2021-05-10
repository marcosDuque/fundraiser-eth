import json

from web3 import Web3

from flask import Flask
from flask_wtf import FlaskForm
import wtforms


BLOCKCHAIN_URL = 'http://127.0.0.1:7545'
CONTRACT_PATH = "contracts/FundraiserFactory.json"

w3 = Web3(Web3.HTTPProvider(BLOCKCHAIN_URL))
contract = None
app = Flask(__name__)



@app.route("/")
def hello_world():
  return "Hello World!"


@app.route("/new", methods=["GET"])
def new_fundraiser_form():
    return render_template('new-fundraiser.html', form=NewFundraiserForm())


class NewFundraiserForm(FlaskForm):
    name = wtforms.StringField('Name')
    url = wtforms.StringField('URL')
    imageURL = wtforms.StringField('Image URL')
    description = wtforms.StringField('description')
    beneficiary = wtforms.StringField('Beneficiary')
    new_fundraiser = wtforms.SubmitField('NEW')


@app.route("/new", methods=["POST"])
def create_fundraiser():
    form = NewFundraiserForm()
    if form.validate_on_submit():
        f = contract.functions.createFundraiser(
            name = form.name.data,
            url =  form.url.data,
            imageURL = form.imageURL.data,
            description = form.description.data,
            beneficiary = form.beneficiary.data
        )
        f.call()

    return render_template('new-fundraiser.html', form=NewFundraiserForm())




if __name__ == '__main__':
    with open(CONTRACT_PATH) as file:
        contract_interface = json.load(file)
    network_id = w3.eth.chain_id

    abi = contract_interface['abi']
    deployed_network = contract_interface["networks"][str(network_id)]
    address = deployed_network["address"]
    contract = w3.eth.contract(address=address, abi=abi)


    app.run()

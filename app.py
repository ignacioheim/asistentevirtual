from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField

from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

app = Flask(__name__)
app.config['SECRET_KEY'] = 'random-key-for-csrf'

class ContactForm(FlaskForm):
    field = StringField('Field')
    send = SubmitField('Enviar')


@app.route('/', methods=['GET', 'POST'])
def index():
	form = ContactForm()
	# Situación inicual del sitio
	if request.method == 'GET':
		return render_template(
			"index.html",
			form=form)

	# POST: Form completado
	elif request.method == 'POST':
		form_field = form.field.data
		resultado = bot(form_field)
		titulo = bot2(form_field)
		return render_template(
			"index.html", 
			resultado=resultado,
			titulo=titulo,
			form=form)


def bot(param):
	authenticator = IAMAuthenticator('BBnXfj5oqTtAuivYUUN8LR4NCgdKRjem135JxOsxmxCY')
	assistant = AssistantV2(
		version='2019-02-28',
		authenticator=authenticator
	)

	assistant.set_service_url('https://api.us-south.assistant.watson.cloud.ibm.com/instances/817432bb-ecb3-4337-b0eb-0933f2b6ca87')

	assistant_id = '4dea62ea-8f08-4704-8fea-53009bcfa649'

	session_id = assistant.create_session(
		assistant_id = assistant_id
	).get_result()['session_id']

	response = assistant.message(
		assistant_id=assistant_id,
		session_id=session_id,
		input={
			'message_type': 'text',
			'text': param
		}
	).get_result()

	resultado = response['output']['generic'][0]['options']

	return resultado

def bot2(param):
	authenticator = IAMAuthenticator('BBnXfj5oqTtAuivYUUN8LR4NCgdKRjem135JxOsxmxCY')
	assistant = AssistantV2(
		version='2019-02-28',
		authenticator=authenticator
	)

	assistant.set_service_url('https://api.us-south.assistant.watson.cloud.ibm.com/instances/817432bb-ecb3-4337-b0eb-0933f2b6ca87')

	assistant_id = '4dea62ea-8f08-4704-8fea-53009bcfa649'

	session_id = assistant.create_session(
		assistant_id = assistant_id
	).get_result()['session_id']

	response = assistant.message(
		assistant_id=assistant_id,
		session_id=session_id,
		input={
			'message_type': 'text',
			'text': param
		}
	).get_result()

	titulo = response['output']['generic'][0]['title']

	return titulo

if __name__ == "__main__":
	app.run(debug=True)
const nodemailer = require('nodemailer');
const fs = require('fs');

const config = require('../config');

class Mail {

	constructor(from, to, subject, bodyTemplate) {

		try {

			this.transporter = nodemailer.createTransport({
				host: config.mailServer,
				port: 25,
				tls: {
					rejectUnauthorized: false
				}
			});

			this.sender = from;
			this.receiver = to;
			this.subject = subject;
			this.text = fs.readFileSync(bodyTemplate, 'utf8');
	
		} catch (e) {
	
			throw Error("Error");
			return {"status" : "Error","msg" : "El correu no s'ha pogut enviar","codi" : 1, "error":e};
	
		}

	}

	swapTemplateVariable(key, value) {

		this.text = this.text.replace(
			new RegExp(key,'g'),
			value);

	}

	send() {

		var mailOptions = {
			from: this.sender,
			to: this.receiver,
			subject: this.subject,
			html: this.text
		};

		return new Promise((resolve, reject) => {

			this.transporter.sendMail(mailOptions, (error, info) => {

				if (error) {
	
					reject(error);
	
				}
	
				resolve();
	
			});

		});

	}

}

module.exports = Mail;

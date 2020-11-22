import smtplib

def send(subject, body, to):
	try:
		print("Email started!")
		server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
		server.ehlo()
		server.login('noreply.donationnation@gmail.com', 'DonationNationPass2020')
		msg = "\r\n".join([
			f"From: noreply.donationnation@gmail.com",
			f"To: {', '.join(to)}",
			f"Subject: {subject}",
			"",
			body
		])
		server.sendmail('noreply.donationnation@gmail.com', to, msg)
		server.close()
		print("Email sent!")
	except Exception as e:
		print(e)
		raise e

from flask import Flask, jsonify, render_template, url_for, redirect
import imaplib
import email
import json
import random
import urllib
from email.header import decode_header


app = Flask(__name__)

main_domain = "YOUR_DOMAIN"
imap_username = "YOUR_CATCH-ALL_INBOX@YOUR_DOMAIN"
imap_password = "INBOX_PASSWORD"
allowed_domains = [main_domain]
restricted_inbox = ["all", "admin", "administrator"] # inboxes that are not processed by this website
restricted_inbox_lenght = 10 # means anything less than 10 characters will not be allowed
words_file = "./static/words.txt"

# cache words in memory
with open(words_file) as file:
    words = file.readlines()


def get_random_words():
    upper_words = [word.strip() for word in words if word[0].isupper()]
    name_words  = [word.strip() for word in upper_words if not word.isupper()]
    rand_name   = ''.join([name_words[random.randint(0, len(name_words))] for i in range(2)])


    if len(rand_name) < restricted_inbox_lenght:
        return get_random_words()

    return rand_name


def parse_email(email):
    if "@" in email:
        parsed_email = email.split("@")
        return parsed_email
    else:
        #fallback to main domain
        return [email, main_domain] #@todo: stick to current url


@app.route("/")
def home():
    random_inbox = urllib.parse.quote_plus(get_random_words())
    #return "This is the homepage!"
    print("Will redirect to " + random_inbox)
    return redirect(f"https://{main_domain}/{random_inbox}@emailtemporal.es")


@app.route("/<inbox>")
def read_email(inbox):
    parsed_inbox = parse_email(inbox)
    parsed_email = parsed_inbox[0]
    parsed_domain = parsed_inbox[1]

    if parsed_domain not in allowed_domains:
        return f"This page should show emails for {parsed_email}@{parsed_domain}"
    elif parsed_email in restricted_inbox:
        return f"The address {parsed_email}@{parsed_domain} is prohibited"
    elif len(parsed_email) < 10:
        return f"The address lenght is not enough. Use address with lenght {restricted_inbox_lenght}"
    else:
        emails = return_emails_for_selected_inbox(parsed_email, parsed_domain)
        return render_template("email.html", email="@".join((parsed_email, parsed_domain)), emails=emails)


def return_emails_for_selected_inbox(parsed_email, parsed_domain):
    mail = imaplib.IMAP4_SSL(parsed_domain, 993)
    mail.login(imap_username, imap_password)
    mail.select("Inbox")
    typ, data = mail.search(None, 'TO', parsed_email + "@" + parsed_domain)
    mail_ids = data[0]
    id_list = mail_ids.split()

    emails = []
    for num in data[0].split():
        typ, data = mail.fetch(num, '(RFC822)')
        raw_email = data[0][1]
        #raw_email_string = raw_email.decode('ISO-8859-1')
        raw_email_string = raw_email.decode('utf-8')
        email_message = email.message_from_string(raw_email_string)
        #print(email_message)
        email_subject = decode_header(email_message.get("SUBJECT"))[0][0].decode("utf-8")
        email_parts = email_message.get_payload(decode=True)

        if email_message.is_multipart():
            for part in email_parts:
                if part.get_content_type() == "text/plain": # by now only working with text
                    email_content = part.get_payload()
        else:
            email_content = email_parts

        #print(email_content)
        if hasattr(email_content, "decode"):
            try:
                emails.append([email_subject,email_content.decode("utf-8")])
            except UnicodeDecodeError:
                emails.append([email_subject,email_content.decode("ISO-8859-1")])
        else:
            emails.append([email_subject, email_content])

    if emails:
        print("asunto: ", emails[0][0])
        return emails
    else:
        return [] # return empty array so we don't have to tweak templates



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8447, debug=False)
    # manual check
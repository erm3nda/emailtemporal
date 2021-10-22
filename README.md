# Emailtemporal.Es

Dead-simple Flask website to render emails at emailtemporal.es.

This code can work with any remote email accounts, because the use of imaplib.
The only key behind such temp email websites is that the email server is setup with a catch-all email, so, any message sent to non active inbox will be redirected to that one.

So, when you send a email to asdfasfasdf@emailtemporal.es wich doesn't exist at all, it is being saved at catch-all@emailtemporal.es inbox.
Lately, the flask app connects via imaplib to such inbox, and allows you to read those whose were sent to asdfasfasdf@emailtemporal.es.
Very usefull, very simple.

I know there are lot of sites doing this, I was just curious and wanted to create my own "send me your shit spam" system.

I let this code as a POC for anyone interested into it.

If you want to make the same, follow this ninja path:
- Install vestacp
- Configure your domain and create a catch-all email for that domain.
- Install supervisor or any "process manager" you know, monit, pm2, or other.
- Configure nginx to proxy_pass to this flask app (tweak /static folder calls).
- Configure the script details to access imap data.
- Enjoy.

VestaCP adds many goodies, letsencrypt, fail2ban, etc. Not only to manage mail server, but for general purpose even if you don't host more websites.
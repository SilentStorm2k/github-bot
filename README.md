# GitHub Bot Setup

Link to Smee: [Smee.io - Webhook Redirect Service](https://smee.io/AYpFuB1lI7uH9msO)

## Steps to Run Locally:

1. Utilize Smee as the webhook redirecting service. Use the provided link above.
2. Modify the bot settings within GitHub user settings:
   - Go to Settings -> Applications -> roody_ruler -> App Settings
3. Update the webhook URL to the Smee link provided above. For deployment, use https://silentstorm-bot.onrender.com.
4. Install the Smee client globally if not already installed:
```bash
npm install --global smee-client
```
5. In the `app.py` file, adjust the private key's path (used for GitHub verification) to the corresponding local location. At deployment use path 
```bash 
'/etc/secrets/your_private_key.pem'
```
6. Execute the following command to redirect payloads received by Smee to the local environment:
```bash
smee -u https://smee.io/AYpFuB1lI7uH9msO --port 5000
```
7. Run `app.py` on port 5000 (or the designated port Smee directs payloads to).
8. Test by typing in "/meme" in any issue/pr/discussion 

## Deploying on render:

1. Change webhook url in github app settings to https://silentstorm-bot.onrender.com 
2. Remove local testing instances in app.py and other files (such as if name == __main__)
3. Change cert_file file location to the correct format (by uncommenting correct value)
4. Push code to main and wait for deployment.

## Future additions and helpful links:

https://coverage.readthedocs.io/en/7.3.2/ 
https://pygithub.readthedocs.io/en/stable/
https://medium.com/@gilharomri/github-app-bot-with-python-ea38811d7b14 (inspired from)
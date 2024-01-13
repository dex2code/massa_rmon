# MASSA remote monitoring service

A simple monitoring agent for your MASSA node.

With this service you can check the availability of one or several nodes remotely via the Internet or locally on the server.

All notifications come to your telegram messenger. The service notices you only if status of your node changed (alive -> dead or dead -> alive).



# Installation:

1. Install Python3 and modules:
   
   `sudo apt-get update`
   
   `sudo apt-get dist-upgrade`

   `sudo apt-get install python3-full python3-venv python3-pip`

   `sudo reboot` (optionally in case dist-upgrade installed new kernel)


2. Prepare service:

   `cd ~`

   `git clone https://github.com/dex2code/massa_rmon.git`

   `cd massa_rmon`

   `python3 -m venv .`

   `source ./bin/activate` -- now you should see `(massa_rmon)` at the beginning of shell prompt

   `./bin/pip3 install pip --upgrade`

   `./bin/pip3 install -r ./requirements.txt` -- this installs all neccessary libs

   `chmod +x ./install-service.sh`

   `./install-service.sh` -- this may ask your password (if you're not root) and you should see "Success!" at the end of the script output.
   

3. Configure service:

   `nano ./settings.json`

   Edit "nodes" section and put correct URL(s) into the config. Check the URL twice before save the file.

   If you plan is to watch local node only, just remove first line (`massa_remote`) to get the following:
   
   `"massa_local": "http://127.0.0.1:33035/api/v2"`

   Fill in `telegram_key` and `telegram_chat` values!

   - `telegram_key` is the secret API key of your bot.
  
     How to create new bot: https://www.youtube.com/watch?v=UQrcOj63S2o

     Don't forget to add your new bot to your contacts to receive messages!

   - `telegram_chat` is the chat_id where bot will send the notifications to. You can use your telegram ID: https://www.youtube.com/watch?v=e_d3KqI6zkI
  

4. Configure Firewall

   Normally MASSA uses 33035/tcp port to receive public API requests.

   This public API is safe and nobody can know your secret keys or even your wallet address. More about public API here: https://docs.massa.net/docs/build/api/jsonrpc

   If you watch localhost (`127.0.0.1`) no actions needed with your firewall. Otherwise you should open TCP port on your node to receive monitoring requests outside:

   `sudo ufw allow 33035/tcp`


# Running service

After all actions described above you can try to run the service: `sudo systemctl start massa_rmon.service`.

In normal way no errors or any other messages should be displayed on this command.

You can additionally check the service with command `sudo systemctl status massa_rmon.service`

You can also read the logfile: `tail -f main.log` or with `sudo journalctl -fu massa_rmon.service`

After succesfull start you should immidiatelly receive two (or more, depends on number of your nodes) messages in your Telegram messenger:

`🤖 MASSA remote monitoring: 💡 Service successfully started to watch the following nodes:`

` - massa_local: http://127.0.0.1:33035/api/v2`

`Main loop delay: 600 seconds`

This message means that your service is started successfully!

Next message(s) is about your node availability:

`🤖 MASSA remote monitoring: ✅ Node 'massa_local' (http://127.0.0.1:33035/api/v2) became alive with chain_id=xxx!` - Everything is fine and your node alive and available.

`🤖 MASSA remote monitoring: ⚠ Node 'massa_local' (http://127.0.0.1:33035/api/v2) seems dead or unavailable! Check node status or firewall settings (sudo ufw allow 33035/tcp)` - Node is unavailable. You should check all your settings and restart service: `sudo systemctl restart massa_rmon.service`.

When everything is fine and working correct you should enable systemd service to restore it after server reboot.

You can easily do it with `sudo systemctl enable massa_rmon.service`.


# Good Luck!

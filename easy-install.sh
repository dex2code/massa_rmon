#!/usr/bin/env bash

DESTDIR="massa_rmon"

# Check OS distro
hostnamectl | grep -i "ubuntu" > /dev/null
if [[ $? -ne 0 ]]
then
    echo "Error: this installation uses Ubuntu-compatible commands and cannot be used in other OS distros."
    echo "You can try to install service manually using this scenario: https://github.com/dex2code/massa_rmon/blob/main/README.md"
    exit 1
else
    cd ~
fi

echo
echo "::::::::::::::::::::::::::::::::::::::::::::::::::::::::"
echo "::'##::::'##::::'###:::::'######:::'######:::::'###:::::"
echo ":::###::'###:::'## ##:::'##... ##:'##... ##:::'## ##::::"
echo ":::####'####::'##:. ##:: ##:::..:: ##:::..:::'##:. ##:::"
echo ":::## ### ##:'##:::. ##:. ######::. ######::'##:::. ##::"
echo ":::##. #: ##: #########::..... ##::..... ##: #########::"
echo ":::##:.:: ##: ##.... ##:'##::: ##:'##::: ##: ##.... ##::"
echo ":::##:::: ##: ##:::: ##:. ######::. ######:: ##:::: ##::"
echo "::..:::::..::..:::::..:::......::::......:::..:::::..:::"
echo "::::::::::::::::::::::::::::::::::::::::::::::::::::::::"
echo
echo "[ MASSA remote monitoring service ] -- https://github.com/dex2code/massa_rmon.git"
echo
echo "This script will configure your system and install all neccessary software:"
echo "  - python3-full"
echo "  - python3-venv"
echo "  - python3-pip"
echo "  - git"
echo
echo "New Python virtual environment will be created in $HOME/$DESTDIR and new systemd unit will be created."
echo -n "If you are ok with this please hit Enter, otherwise Ctrl+C to quit the installation... "
read _
echo
echo -n "First we update your repository and install all packages. Press Enter to continue... "
read _
echo

sudo apt-get update
if [[ $? -eq 0 ]]
then
    echo "*** Updating finished!"
    echo
else
    echo
    echo "Some error occured during updating. Please check your settings."
    exit 1
fi

sudo apt-get -y install git python3-full python3-venv python3-pip
if [[ $? -eq 0 ]]
then
    echo "*** All dependecies installed!"
    echo
else
    echo
    echo "Some error occured during installation. Please check your settings."
    exit 1
fi

echo -n "Now we clone repo to download service software. Press Enter to continue... "
read _
echo

git clone https://github.com/dex2code/massa_rmon.git
if [[ $? -eq 0 ]]
then
    echo "*** Repo cloned successfully!"
    echo
else
    echo
    echo "Some error occured during repo cloning. Please check your settings."
    exit 1
fi

echo -n "Now we are ready to create and configure Python virtual environment. Press Enter to continue... "
read _
echo

cd $DESTDIR && python3 -m venv .
if [[ $? -eq 0 ]]
then
    echo "*** Virtual environment created successfully! Configureng venv..."
    echo
else
    echo
    echo "Some error occured during venv creating. Please check your settings."
    exit 1
fi

source ./bin/activate && ./bin/pip3 install pip --upgrade && ./bin/pip3 install -r ./requirements.txt
if [[ $? -eq 0 ]]
then
    echo "*** Virtual environment configured successfully!"
    echo
else
    echo
    echo "Some error occured during venv configuring. Please check your settings."
    exit 1
fi

echo -n "It's time to create systemd unit. Press Enter to continue... "
read _
echo

echo -n "*** Generating service file... "
echo "
[Unit]
Description=MASSA Remote Monitoring service
Wants=network.target
After=network.target

[Service]
Type=idle
User=$USER
WorkingDirectory=$HOME/$DESTDIR
ExecStart=$HOME/$DESTDIR/bin/python3 main.py
Restart=always
RestartSec=60

[Install]
WantedBy=multi-user.target
" > ./massa_rmon.service && sudo cp ./massa_rmon.service /etc/systemd/system/massa_rmon.service && sudo systemctl daemon-reload

if [[ $? -eq 0 ]]
then
    echo "Done!"
    echo
else
    echo
    echo "Some error occured during systemd configuring. Please check your settings."
    exit 1
fi

echo "*** Installation done! Press Enter to continue... "
read _
echo
echo "Now you need to configure the service and start it."
echo
echo "Service settings are located in '~/$DESTDIR/settings.json' file and you can edit it with 'nano ~/$DESTDIR/settings.json' command."
echo "After it you can start service with command 'sudo systemctl start massa_rmon.service'."
echo
echo "If something goes wrong please see logfile: 'tail ~/$DESTDIR/main.log'."
echo
echo "If everything is fine please enable service with command 'sudo systemctl enable massa_rmon.service' to restore it after server reboot."
echo
echo "More information here: https://github.com/dex2code/massa_rmon.git"
echo


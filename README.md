## In short:


- This integration allows you to read runtime-related data from a UGOS-based NAS directly into Home Assistant.
- The main idea: keep UGOS completely untouched (no additional tools installed on the NAS, so updates remain hassle-free).
- The process involves two steps:<br/>1) Obtain an individual token to authenticate your NAS queries (this is the tricky part).<br/>2) Configure Home Assistant for frequent data polling using the built-in RESTful integration (super simple).
- For step 1, a shell script will guide you through a few straightforward questions and generate the token.

**Important**: This is in a pre-alpha phase and still under development, currently optimized for the DXP-4800Plus.<br/>Larger models will require adjustments for additional volumes/disks, unit conversions/ roundings are not done properly yet, etc. Bottom line: This is a proof-of-concept for enthusiasts. Follow the steps at your own risk.

## Introduction

When I switched from my trusty old 10-year old 2-Bay QNAP to the shiny new UGreen DXP-4800Plus, I ran into a couple of challenges.

The first issue was migrating my QNAP VMs to the UGreen NAS. After nearly 10 years of using that QNAP, I had built up quite a collection of virtual machines—including my entire Home Automation System with databases spanning the past decade. Initially, I couldn’t get these VMs to a functional state on the new system. After some trial-and-error (and a deeper dive into what was going wrong), I found a relatively simple solution. You can check out the details in [this](https://discord.com/channels/1208438687168335913/1270855790147797104/1318333164455723070) short post on UGreen’s Discord.

The next hurdle was UGOS itself—it’s not exactly chatty when it comes to providing operational data about the NAS. As QNAP has it's own HA integration, I was used to views like this one:

![image](https://github.com/user-attachments/assets/a7d0b14b-f056-4609-acbc-414baf8e3dd2)

I soon found out that a similar card on the dashboard was rather impossible to do, and searching the Web for a ready-made HA solution or integration didn't get me any positives (but a lot of useful background information). So I had to start digging myself.

The result can be found below. It is not what I would expect from a 'professional' end-user solution; it isn't even nice code. But it's working, and from my point of view a valid proof-of-concept.

> If you come across any problems when following this guide, you are welcome to open a thread in the discussions section.
> If you did the steps successfully, please also report back - people are interested to know that this doesn't work only once here on my desk.
> If you like it - please leave a star. Thanks, good luck and enjoy. :)

## Preparations

Before you get started, make sure to gather some important information that you’ll need later. Write it down somewhere safe—you’ll need it in the upcoming steps:

- The IP address of your NAS (four numbers, e.g., 192.168.178.9).
- The port number your NAS uses for communication (usually 9999).
- The username of an account with administrative privileges.
- The password for that user account.
- A specific number that we’ll extract together in step 2 of this guide.

Since you already use this information when accessing your NAS through its Web Interface in a browser, it should be easy to find.
Tip: The IP address and port number are displayed in your browser’s address bar (URL).

![image](https://github.com/user-attachments/assets/43a8ca7e-cc14-4aff-8b0b-9379804f5b28)

_Side note: While I initially explored this using a different approach, I will use the Visual Studio Code Server for this guide to make the steps easier to follow. If you haven’t installed it yet as an add-on, now is a good time to do so. Alternatively, you’ll need to manually execute the steps using an SSH shell and transfer files via an SMB connection to Home Assistant, or similar methods._

_Side note 2: All shell commands below can be copied and pasted directly from this guide. After pasting a command, press <Enter> to execute it._

## Step 1: Getting the Token Script Ready
> **Purpose:** Set up the shell script for token generation.

- Open the Visual Studio Code Server, navigate to your file structure on the left, and create a directory named `scripts` (if it doesn’t already exist).
- Inside the `scripts` directory, create a new file called `get_ugreen_token.sh`.
- Copy the content of the `scripts/get_ugreen_token.sh` file from this repository into your newly created file.
- Right-click the file name and select “Open in Integrated Terminal”.
- In the terminal, run the following command to make the script executable: `chmod +x get_ugreen_token.sh`.<br/><br/> ![image](https://github.com/user-attachments/assets/160ee7f7-5eab-45a6-8db8-99e6a2fc9b5b)

The script is now ready to use.

## Step 2: Retrieving the Last Piece of Information for the Token
> **Purpose:** Locate the certificate number required for token generation.

- Stay in the terminal window and type: `clear` - this gets us an empty, clean workbench.
- Connect to your NAS via SSH by running: `ssh your_username@your_nas_ip` (example: `ssh tom@192.168.178.9`).
- Enter your password when prompted. You will now see the NAS command prompt (you’re working directly on the NAS).
- Run the following command to list the certificate files: `sudo ls /var/cache/ugreen-rsa` (Note: For security reasons, you will be asked to re-enter your password).
- The output will list two files, e.g., 1000.key and 1000.pub. The number in the file name (e.g., 1000) is the certificate number you need. Write this number down.
- Log off from the NAS SSH session by typing: `exit`.<br/><br/>![image](https://github.com/user-attachments/assets/01d9a86c-76bf-4fc0-a554-9c015dc6dd4e)

You now have the final piece of information required for token generation.

## Step 3: Getting Your Token
> **Purpose:** Generate your authentication token for Home Assistant REST requests.

- Stay in the terminal window, run `clear` again for a clean workbench.
- Run the shell script to generate the token: `./get_ugreen_token.sh` (the `./` at the beginning is important).
- Follow the prompts displayed by the script. You’ll need to provide: The IP address of your NAS, the port number, the username and password, the certificate number retrieved in Step 2.<br/>Note: Password will be asked for again; ignore any _'Could not chdir'_ messages.
- You will be presented with 3 results: (1) an encrypted password, (2) a static token, (3) a session token.
- Select the static token (only this one we need) and copy it to you clipboard. Make sure it is staying there until the end of the next step (safe way is to temporarily paste it somewhere).<br/><br/>![image](https://github.com/user-attachments/assets/64ee57b2-8720-43af-a453-22def10e91d7)

You now have a valid token that can be used to authenticate REST requests from Home Assistant.

## Step 4: Creating Boot-Safe HA Config Entities for Your NAS

> **Purpose:** Ensure your token is easily accessible and quickly adjustable at any time without restarting HA.

The most flexible way to store your token is by using a `text_input` entity. This approach allows you to update the token directly in the Home Assistant developer tools without requiring a restart. Currently, I have no practical experience regarding how frequently a token might be revoked or changed by the NAS, but this method seems like the most logical solution.

Additionally, I prefer to keep configurations organized in separate files. Below, I’ll describe the steps following that principle. However, feel free to adjust the instructions to match your setup or preferences. For example, you could also store the token in `secrets.yaml` if that suits your needs.

Open `configuration.yaml` and add a new package under the `homeassistant` key. Leave the `rest` section commented out for now; we’ll handle that in the next step. As always, pay attention to proper indentation:
```yaml
homeassistant:
  packages:
    ugreen_nas:
      # rest:            !include conf/ugreen_nas_rest.yaml
      text_input:        !include conf/ugreen_nas_text_input.yaml
```


- Create a `conf` directory for your configuration and add a file named `ugreen_nas_text_input.yaml` inside it:![image](https://github.com/user-attachments/assets/559ac374-7b92-487a-8e0a-6acd7fa4aa0e)
- Copy the content of the file `conf/ugreen_nas_text_input.yaml` from this repository into the newly created file.
- Restart Home Assistant to apply the changes and create the entities.
- Open **Developer Tools** → **States** in Home Assistant and filter for `ugreen`. For each filtered entity, set your local values, confirm each with 'Set state'.![image](https://github.com/user-attachments/assets/e04e4abe-c5a3-49c0-acba-9f2d375cdd7a)

You have now completed the basic configuration and initial setup.

## Step 5: Create Your Entities / Sensors
> **Purpose:** Finalize the setup procedure by defining the sensors to read data from the NAS.


>to be completed by me tomorrow - see conf/ugreen_nas_rest.yaml.
>
>it used to work fine for 3 days until I switched today the REST URL from fixed IP/Port in YAML definition to templated input_text's ...
>
>since then, some sensors are not reporting anymore. manual call in browser with the current token in the same URL gives positive JSON results / dict. (HUH? - to be evaluated - still a proof-of-concept)

![image](https://github.com/user-attachments/assets/086f2108-7872-42f1-90ff-faec348ada39)

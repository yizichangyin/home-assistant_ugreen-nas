## Preparations
<details>
  <summary>click to show/hide</summary>
  <br/>Before you get started, make sure to gather some important information that you’ll need later. Write it down somewhere, you’ll need it in the upcoming steps:<br/><br/>
  
  - The IP address of your NAS (four numbers, e.g., 192.168.178.9).
  - The port number your NAS uses for communication (usually 9999).
  - The username of a NAS account with administrative privileges.
  - The password for that user account.
  - A specific number that we’ll extract in step 2 of this guide.
  
  Since you already use most of this information when accessing your NAS through its Web Interface in a browser, it should be easy to find (e.g. the IP address and port number are displayed in your browser’s address bar):
  
  ![image](https://github.com/user-attachments/assets/01f2415a-c07f-4730-8150-6131435e11f3)
  
  _Side note: While I initially explored this using a different approach, I will use the Visual Studio Code Server for this guide to make the steps easier to follow. If you haven’t installed it yet as an add-on, now is a good time to do so. Alternatively, you’ll need to manually execute the steps using an SSH shell and transfer files via an SMB connection to Home Assistant, or similar methods._
  
  _Side note 2: All shell commands below can be copied and pasted directly from this guide. After pasting a command, press <Enter> to execute it._
</details>

## Step 1: Creating the token gathering script
<details>
  <summary>click to show/hide</summary>
  <br/>This will create a shell script for token generation:<br/><br/>
  
  - Open the Visual Studio Code and create a directory named `scripts` in your file structure on the left.
  - Inside `scripts`, create a new file called `get_ugreen_token.sh`.
  - Copy the content of `scripts/get_ugreen_token.sh` from this Github repository into your newly created file.
  - Right-click the file name and select “Open in Integrated Terminal”.
  - In the terminal window, run the following command: `chmod +x get_ugreen_token.sh`
  
  ![image](https://github.com/user-attachments/assets/3c4808fb-0aa5-4188-bc4d-96c56c79f3a5)

  The script is now ready to use.<br/><br/>
</details>

## Step 2: Retrieving the certificate number
<details>
  <summary>click to show/hide</summary>
  <br/>This will provide you the certificate number, which is the final piece of information we need for token generation:<br/><br/>

  - Stay in the terminal window and type: `clear` - it will get us an empty, clean workbench.
  - Connect to your NAS via SSH by running: `ssh your_username@your_nas_ip` (example: `ssh tom@192.168.178.9`).
  - Enter your password when prompted. You will now see the NAS command prompt (you’re working directly on the NAS).
  - Run the following command to list the certificate files: `sudo ls /var/cache/ugreen-rsa`<br/>(For security reasons, you will be asked to re-enter your password).
  - The output will list two files, e.g., `1000.key` and `1000.pub`.<br/>The file names give you a certificate number (here: 1000) - please write it down.
  - Log off from the NAS SSH session by typing: `exit`.
  
  ![image](https://github.com/user-attachments/assets/194275a3-57d7-4f7e-9bee-f43b96ee219c)
  
  We now have the final piece of information on hand that we need for token generation.
</details>

## Step 3: Getting the REST token
<details>
  <summary>click to show/hide</summary>
  <br/>Let's generate our token:<br/><br/>
  
  - Stay in the terminal window, run `clear` again for a clean workbench.
  - Run the shell script to generate the token: `./get_ugreen_token.sh` (the `./` at the beginning is important!).
  - Follow the prompts - you’ll need to provide:<br/>IP address the NAS, port number, username and password, certificate number retrieved in Step 2.<br/>Note: For security reasons, it will ask for the password again after entering the data.
  - You will be presented with 3 results:<br/>(1) an encrypted password, (2) a static token, (3) a session token.
  - Select the static token (we need only this one) and copy it to your clipboard.<br/>Make sure it is staying there until the end of the next step (safe way is to temporarily paste it somewhere).
  
  ![image](https://github.com/user-attachments/assets/e985f25f-0f16-4cfd-a552-08b50d444ef4)
  
  We now have a valid token that can be used to authenticate REST requests from Home Assistant towards the NAS.
</details>

## Step 4: Creating restart-safe HA config entities
<details>
  <summary>click to show/hide</summary>
  <br/>This will ensure that your token is easily accessible and quickly adjustable at any time - no need to restart HA after changes:<br/><br/>
  
  - Open `configuration.yaml` and add a new package under the `homeassistant` key. Leave the `rest` section commented out for now; we’ll handle that in the next step. As always, pay attention to proper indentation:<br/><br/>
    ```yaml
    homeassistant:
      packages:
        ugreen_nas:
          # rest:            !include conf/ugreen_nas_rest.yaml
          text_input:        !include conf/ugreen_nas_text_input.yaml
    ```
  - Create a `conf` directory for your configuration and add a file named `ugreen_nas_text_input.yaml` inside it:<br/><br/>![image](https://github.com/user-attachments/assets/c133a6a0-a45f-4b7a-91d2-a81057ecff93)
  - Copy the content of the file `conf/ugreen_nas_text_input.yaml` from this repository into the newly created file.
  - Restart Home Assistant to apply the changes and create the entities.
  - Open **Developer Tools** → **States** in Home Assistant and filter for `ugreen`.<br/>For each filtered entity, set your local values, confirm each with 'Set state'.<br/><br/>![image](https://github.com/user-attachments/assets/c324dfaa-f522-4017-87f2-e5520817c890)
  
  We have now completed the basic configuration and initial setup.
</details>

## Step 5: Creating the NAS entities in HA
<details>
  <summary>click to show/hide</summary>
  <br/>Finally, we are ready to create our REST sensors in HA.<br/><br/>

_to be completed - if you want to work ahead now, see conf/ugreen_nas_rest.yaml_
</details>

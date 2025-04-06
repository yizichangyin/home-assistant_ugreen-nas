Revised version: Steps 1 - 3 can be skipped.

## Preparations
<details>
  <summary>click to show/hide</summary>
  <br/>Before you get started, make sure to gather some important information that you’ll need later. Write it down somewhere, you’ll need it in the upcoming steps:<br/><br/>
  
  - The IP address of your NAS (four numbers, e.g., 192.168.178.9).
  - The port number your NAS uses for communication (usually 9999).
  - ~~The username of a NAS account with administrative privileges.~~ (not needed any longer)
  - ~~The password for that user account.~~ (not needed any longer)
  - ~~A specific number that we’ll extract in step 2 of this guide.~~ (not needed any longer)
  
  Since you already use most of this information when accessing your NAS through its Web Interface in a browser, it should be easy to find (e.g. the IP address and port number are displayed in your browser’s address bar):
  
  ![image](https://github.com/user-attachments/assets/01f2415a-c07f-4730-8150-6131435e11f3)
  
 ~~_Side note: While I initially explored this using a different approach, I will use the Visual Studio Code Server for this guide to make the steps easier to follow. If you haven’t installed it yet as an add-on, now is a good time to do so. Alternatively, you’ll need to manually execute the steps using an SSH shell and transfer files via an SMB connection to Home Assistant, or similar methods._~~
  
  ~~_Side note 2: All shell commands below can be copied and pasted directly from this guide. After pasting a command, press <Enter> to execute it._~~
</details>

## ~~Step 1: Creating the token gathering script~~ (obsolete, use browser)
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

## ~~Step 2: Retrieving the certificate number~~ (obsolete, use browser)
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

## ~~Step 3: Getting the REST token~~ (obsolete, use browser)
<details>
  <summary>click to show/hide</summary>
  <br/>Let's generate our token:<br/><br/>
  
  - Stay in the terminal window, run `clear` again for a clean workbench.
  - Run the shell script to generate the token: `./get_ugreen_token.sh` (the `./` at the beginning is important!).
  - Follow the prompts - you’ll need to provide:<br/>IP address the NAS, port number, username and password, certificate number retrieved in Step 2.<br/>Note: For security reasons, it will ask for the password again after entering the data.
  - You will be presented with 3 results:<br/>(1) an encrypted password, (2) a static token, (3) a session token.
  - Select the static token (we need only this one) and copy it to your clipboard. Make sure it is staying there until the end of the next step (safe way is to temporarily paste it somewhere).<br/>**Update 04/2025: After firmware 1.3, the `static token` is not working any longer. As a workaround, please use the `api_token` instead.**
  
  ![image](https://github.com/user-attachments/assets/e985f25f-0f16-4cfd-a552-08b50d444ef4)
  
    We now have a valid token that can be used to authenticate REST requests from Home Assistant towards the NAS.
</details>

## Steps 1-3 combined (the easier way to do it, no shell script needed)
<details>
  <summary>click to show/hide</summary>
  <br/>Let's gain our token:<br/><br/>
  
  - Open your web browser, log on to the Web GUI of the NAS with an administrative user.
  - Display the developer tools (most browsers: press F12).
  - The following picture (screenshot of Google Chrome developer tools) shows where to find the `static_token`key that we need. There might be different menu titles if you are using another browser; in most of them you can use Ctrl-F to locate the key![image](https://github.com/user-attachments/assets/19582953-1790-4a2e-9242-34fc56d32d43)
  - Select and right-click the `static_token` key and choose 'copy' (or 'copy value', again depending on your browser) to copy the token to your clipboard.<br/>Make sure it is staying there until the end of the next step (safe way is to temporarily paste it somewhere).
  
  We now have a valid token that can be used to authenticate REST requests from Home Assistant towards the NAS.
</details>

## Step 4: Creating restart-safe HA config entities
<details>
  <summary>click to show/hide</summary>
  <br/>This will ensure that your token is easily accessible and quickly adjustable at any time - no need to restart HA after changes:<br/><br/>
  
  - Open `configuration.yaml` and add a new package under the `homeassistant` key. Leave the `rest` section commented out for now; we’ll handle that in the next step. As always, pay attention to proper indentation:<br/><br/>
    ```yaml
    logger:
      default: warning
      logs:
        homeassistant.components.rest: critical
        homeassistant.components.sensor: error
    
    homeassistant:
      packages:
        ugreen_nas:
          # rest:            !include conf/ugreen_nas_rest.yaml
          # template:        !include conf/ugreen_nas_template_sensors.yaml
          input_text:        !include conf/ugreen_nas_input_text.yaml
    ```
  - Create a `conf` directory for your configuration and add a file named `ugreen_nas_input_text.yaml` inside it:<br/><br/>![image](https://github.com/user-attachments/assets/c133a6a0-a45f-4b7a-91d2-a81057ecff93)
  - Copy the content of the file `conf/ugreen_nas_input_text.yaml` from this repository into the newly created file.
  - Restart Home Assistant to apply the changes and create the entities.
  - Open **Developer Tools** → **States** in Home Assistant and filter for `ugreen`.<br/>For each filtered entity, set your local values, confirm each with 'Set state'.<br/><br/>![image](https://github.com/user-attachments/assets/c324dfaa-f522-4017-87f2-e5520817c890)
  
  We have now completed the basic configuration and initial setup.
</details>

## Step 5: Creating the NAS entities in HA
<details>
  <summary>click to show/hide</summary>
  <br/>Finally, we are ready to create our REST sensors in HA.<br/><br/>

  - Go back to VS Code and create a file `conf/ugreen_nas_rest.yaml` (next to the `ugreen_nas_rest.yaml` we have created before).
  - Copy/paste the code of this repository's `conf/ugreen_nas_rest.yaml` into it.
  - Create another file `conf/ugreen_nas_template_sensors.yaml` and copy it's contents from this repo, too.
  - Go back to your `configuration.yaml`and uncomment `rest:` and `template`![image](https://github.com/user-attachments/assets/8714d257-00af-41c5-b28a-98b726e2028e)
  - Restart Home Assistant.
  - Wait for a minute or two to let everything start properly, then choose **Developer Tools** --> **Actions** --> **Action:'RESTful: Reload'** and confirm.
  - After another 5...10 seconds you should be set.
  - Click **Developer Tools** --> **States** and filter for _ugreen_. All your NAS sensor names and data should appear.
  - Make sure you are aware of the latest comments in the '[known problems and limitations](https://github.com/Tom-Bom-badil/ugreen_nas/discussions/2) discussion here.
  - You may need to adjust your sensors to your model / discs / pools, see discussion [here](https://github.com/Tom-Bom-badil/ugreen_nas/discussions/6).

  _(... and let me know if you came across any difficulties, so I can improve this documentation ...)_
</details>

## Step 6: Making adjustments to your specific model or number of disks / volumes / fans etc
<details>
  <summary>click to show/hide</summary>
  <br/>Please make sure to check `homeassistant.log` for any errors. To adjust the default entities and sensors, you can comment / uncomment / add / remove entities in the following files:<br/><br/>

  - `conf/ugreen_nas_rest.yaml` for your REST requests ('raw data')
  - `conf/ugreen_nas_template_sensors.yaml` for your calculations and unit conversions.

  In both cases, no full restart is required. You can use the `Reload YAML` quickstart method to reload both REST and Template Sensors.

  Congratulations, enjoy your selfmade UGreen HA Integration! :)<br/>
  _(... and let me know if you came across any difficulties, so I can improve this documentation ...)_
</details>

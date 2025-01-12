## In short

The setup procedure shown in this repository enables Home Assistant to read data from a UGOS-based UGreen NAS. It keeps UGOS completely untouched - no additional tools will be installed on the NAS; we will just use what is already there.

The process involves two steps:<br/>1) Obtain an individual token for authentication (the rather complicated part).<br/>2) Configure Home Assistant for frequent data polling by utilizing the standard HA REST integration (simple).

For step 1, a dedicated shell script will take care of the complicated token generation process. You only need to input some general parameters like NAS IP or user name.

## The story behind

<details>
  <summary>click to show/hide</summary>
  <br/>When I switched from my old QNAP to the new UGreen DXP, I ran into a couple of challenges.<br/><br/>
  The first issue was migrating my VMs. After nearly 10 years of using that QNAP, I had built up a collection of virtual machines, including my entire Home Automation System with databases spanning the past decade. Initially, I couldn’t get these VMs to a functional state on the new system. After some trial-and-error (and a deeper dive into what was going wrong), I found a relatively simple solution. You can check out the details in <a href="https://discord.com/channels/1208438687168335913/1270855790147797104/1318333164455723070">this</a> pinned post on the UGreen Discord.<br/><br/>
  
  The next hurdle was UGOS itself — it’s not exactly chatty when it comes to providing operational data like CPU utilization, memory usage etc. As QNAP has its own HA integration, I was used to views like this one:
  
  ![image](https://github.com/user-attachments/assets/37f5f5d5-9998-4879-bdfa-8fa4d5590ef0)
  
  Searching the Web for a ready-made HA solution or integration didn't get me any positives (but a lot of useful background information). So, I had to start digging myself. The outcome can be found in this GitHub Repository. It is not what I would expect of a 'professional' one-click end user solution; it isn't even nice code. But it's working, and a valid proof-of-concept.
</details>

## The setup procedure

Click [here](https://github.com/Tom-Bom-badil/ugreen_nas/blob/main/docs/how_to_setup.md) to open the detailed step-by-step instructions. Make sure to check on [Known problems and limitations](https://github.com/Tom-Bom-badil/ugreen_nas/discussions/2) in the discussions section before proceeding with installation.

## Final notes

Everything on this Repository is still under development. My current focus is the DXP 4800 Plus. Different models will require adjustments to volumes/disk readings. Also, unit conversions + rounding are not done properly yet, some data are displayed in weird formats. I will solve all this step-by-step, e.g. by adjusting the current templates, or by adding new template sensors (your pull requests are appreciated!).<br/><br/>
If you come across any problems, you are welcome to open a thread in the [discussions](https://github.com/Tom-Bom-badil/ugreen_nas/discussions) section.<br/>
If you succeed, please also report back. It's always good to know if things are working as intended.
<br/><br/>
![image](https://github.com/user-attachments/assets/2f3053ac-35a0-42af-af59-087d0ec2134a)


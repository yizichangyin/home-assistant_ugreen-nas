[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-%2341BDF5.svg)](https://www.home-assistant.io)
[![Custom integration](https://img.shields.io/badge/custom%20integration-%2341BDF5.svg)](https://www.home-assistant.io/getting-started/concepts-terminology)
[![HACS](https://img.shields.io/badge/HACS%20listing-not%20needed-red.svg)](https://github.com/hacs)
[![HACS](https://img.shields.io/badge/HACS%20install-not%20needed-red.svg)](https://github.com/hacs)
[![Version](https://img.shields.io/badge/Version-v2025.05.1-green.svg)](https://github.com/Tom-Bom-badil/home-assistant_helios-vallox/releases)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Tom-Bom-badil/home-assistant_helios-vallox/graphs/commit-activity)

## In short

The setup procedure shown in this repository enables Home Assistant to read data from a UGOS-based UGreen NAS. It keeps UGOS completely untouched - no additional tools will be installed on the NAS; we will just use what is already there.

![image](https://github.com/user-attachments/assets/2f3053ac-35a0-42af-af59-087d0ec2134a)

The process involves two steps:<br/>1) Obtain an individual token for authentication (the rather complicated part; reworked to make it more easy).<br/>2) Configure Home Assistant for frequent data polling by utilizing the standard HA REST integration (simple).

The entire setup procedure shouldn't take you more than 10 minutes if you are familiar with Home Assistant's basic concepts.

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

When tinkering out these instructions, my focus was on my DXP 4800+. Different models might require adjustments to volumes / disks / readings / sensors / templates; I tried to include as many optional and additional components as I could foresee (particularly in the sensor templates) - but for sure there are some I have overlooked.
<br/><br/>
If you come across any problems, you are welcome to open a new thread in the [discussions](https://github.com/Tom-Bom-badil/ugreen_nas/discussions) section.<br/>
If you succeed, please also report back. It's always good to know if things are working out as intended.
If you find any options that can be included in addition to what is already there - your pull requests / reports are always welcome. Thanks. :)

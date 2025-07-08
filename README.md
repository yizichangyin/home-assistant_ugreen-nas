# UGreen NAS Monitoring

[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-%2341BDF5.svg)](https://www.home-assistant.io)
[![Custom integration](https://img.shields.io/badge/Custom%20Integration-%2341BDF5.svg)](https://www.home-assistant.io/getting-started/concepts-terminology)
[![HACS Listing](https://img.shields.io/badge/HACS%20Listing-default-green.svg)](https://github.com/hacs)
[![Version](https://img.shields.io/badge/Version-v2025.07.2-green.svg)](https://github.com/Tom-Bom-badil/home-assistant_helios-vallox/releases)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/Tom-Bom-badil/home-assistant_helios-vallox/graphs/commit-activity)

---

## 🚀 Quick Overview

This project enables **Home Assistant** to monitor system data from a **UGOS-based UGreen NAS** – *without modifying the NAS in any way*. No extra tools or scripts are installed on the standard UGOS operating system of the NAS; we simply use what it already provides.

<p align="center">
  <img src="https://github.com/user-attachments/assets/2f3053ac-35a0-42af-af59-087d0ec2134a" alt="System View" width="600"/>
</p>

The setup process involves two steps:

1. **Token retrieval** - done by setting up a Docker Container.  
2. **Home Assistant configuration** - done by installing the integration from HACS and adding your NAS device.

> ⏱️ Total setup time: *~10 minutes* (if you’re familiar with HA basics)

---

## 📖 Background

<details>
  <summary>Click to expand</summary>

When migrating from my old QNAP to a UGreen DXP, I encountered a few issues.

First, my virtual machines wouldn’t boot properly. After some digging, I solved the problem — [full details here](https://discord.com/channels/1208438687168335913/1270855790147797104/1318333164455723070) on Discord.

Then came the real issue: UGOS doesn’t expose system data like CPU or RAM usage through standard interfaces. Unlike QNAP (which has a built-in Home Assistant integration), I couldn’t find any plug-and-play option.

So I started building something myself — not beautiful, not plug-and-play - but it worked. And it’s been a solid proof of concept for anyone wanting Home Assistant insights from a UGreen NAS.

Then @dobby5 jumped in and came up with a “real” integration - and that’s where we are today.

<p align="center">
  <img src="https://github.com/user-attachments/assets/37f5f5d5-9998-4879-bdfa-8fa4d5590ef0" alt="HA Dashboard Example" width="600"/>
</p>

</details>

---

## ⚙️ Setup Instructions

👉 [**Click here** for the step-by-step guide (Plugin) »](https://github.com/Tom-Bom-badil/ugreen_nas/blob/main/docs/how_to_setup_custom_components.md)

👉 [**Click here** for the step-by-step guide (Config) »](https://github.com/Tom-Bom-badil/ugreen_nas/blob/main/docs/how_to_setup.md) (deprecated, to be removed 2025-08.1)

---

## 📝 Notes & Feedback

- This setup was developed using a **UGreen DXP 4800+** and a **DXP480T**. Other models might require adjustments (we are working on it).

**Contributions welcome!**  
💬 [Start a discussion](https://github.com/Tom-Bom-badil/ugreen_nas/discussions) if you run into issues.  
✅ If it works for you, please let us know - it's great to hear success stories.  
📬 Pull requests and improvements are always appreciated!

---

*Thanks for using this integration, enjoy it! 😊*

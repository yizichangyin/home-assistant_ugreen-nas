# UGreen NAS Monitoring for Home Assistant

[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-%2341BDF5.svg)](https://www.home-assistant.io)
[![Custom integration](https://img.shields.io/badge/Custom%20Integration-%2341BDF5.svg)](https://www.home-assistant.io/getting-started/concepts-terminology)
[![HACS Listing](https://img.shields.io/badge/HACS%20Listing-not%20needed-red.svg)](https://github.com/hacs)
[![HACS Install](https://img.shields.io/badge/HACS%20Install-not%20needed-red.svg)](https://github.com/hacs)
[![Version](https://img.shields.io/badge/Version-v2025.05.1-green.svg)](https://github.com/Tom-Bom-badil/home-assistant_helios-vallox/releases)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/Tom-Bom-badil/home-assistant_helios-vallox/graphs/commit-activity)

---

## 🚀 Quick Overview

This project enables **Home Assistant** to monitor system data from a **UGOS-based UGreen NAS** – *without modifying the NAS in any way*. No extra tools or scripts are installed; we simply use what UGOS already provides.

<p align="center">
  <img src="https://github.com/user-attachments/assets/2f3053ac-35a0-42af-af59-087d0ec2134a" alt="System View" width="600"/>
</p>

The setup process involves two steps:

1. **Token retrieval** – once tricky, now simplified.  
2. **Home Assistant configuration** – done via the standard REST integration.

> ⏱️ Total setup time: *~10 minutes* (if you’re familiar with HA basics)

---

## 📖 Background

<details>
  <summary>Click to expand</summary>

When migrating from my old QNAP to a UGreen DXP, I encountered a few issues.

First, my virtual machines wouldn’t boot properly. After some digging, I solved the problem — [full details here](https://discord.com/channels/1208438687168335913/1270855790147797104/1318333164455723070) on Discord.

Then came the real issue: UGOS doesn’t expose system data like CPU or RAM usage through standard interfaces. Unlike QNAP (which has a built-in Home Assistant integration), I couldn’t find any plug-and-play option.

So I started building something myself — not beautiful, not plug-and-play — but it works. And it’s a solid proof-of-concept for anyone wanting Home Assistant insights from a UGreen NAS.

<p align="center">
  <img src="https://github.com/user-attachments/assets/37f5f5d5-9998-4879-bdfa-8fa4d5590ef0" alt="HA Dashboard Example" width="600"/>
</p>

</details>

---

## ⚙️ Setup Instructions

👉 [**Click here** for the step-by-step guide (Config) »](https://github.com/Tom-Bom-badil/ugreen_nas/blob/main/docs/how_to_setup.md)

👉 [**Click here** for the step-by-step guide (Plugin) »](https://github.com/Tom-Bom-badil/ugreen_nas/blob/main/docs/how_to_setup_custom_components.md)

Before proceeding, check out the [**Known Problems & Limitations**](https://github.com/Tom-Bom-badil/ugreen_nas/discussions/2) to avoid pitfalls.

---

## 📝 Notes & Feedback

- This setup was developed using a **UGreen DXP 4800+**. Other models might require adapting disk references or sensor templates.
- Sensor templates were written with flexibility in mind, but some adjustments may be necessary for your specific configuration.

**Contributions welcome!**  
💬 [Start a discussion](https://github.com/Tom-Bom-badil/ugreen_nas/discussions) if you run into issues.  
✅ If it works for you, please let me know — it's great to hear success stories.  
📬 Pull requests and improvements are always appreciated!

---

*Thanks for using this integration! 😊*
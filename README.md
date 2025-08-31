# UGreenPro NAS Monitoring 国内自用

[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-%2341BDF5.svg)](https://www.home-assistant.io)
[![Custom integration](https://img.shields.io/badge/Custom%20Integration-%2341BDF5.svg)](https://www.home-assistant.io/getting-started/concepts-terminology)
[![HACS Listing](https://img.shields.io/badge/HACS%20Listing-default-green.svg)](https://github.com/hacs)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/yizichangyin/home-assistant_ugreen_pro-nas/graphs/commit-activity)
[![Version](https://img.shields.io/github/v/release/yizichangyin/home-assistant_ugreen_pro-nas?include_prereleases&sort=semver&color=green)](https://github.com/Tom-Bom-badil/yizichangyin/home-assistant_ugreen_pro-nas/releases)
[![Stars](https://img.shields.io/github/stars/yizichangyin/home-assistant_ugreen_pro-nas?style=flat&color=yellow)](https://github.com/yizichangyin/home-assistant_ugreen_pro-nas/stargazers)

---

## 🚀 Quick Overview

👉 This project enables **Home Assistant** to monitor data of a **UGOS based UGreen NAS** - *without modifying its operating system in any way*. No extra tools/scripts are installed in UGOS, no ssh access with cryptic shell commands is needed; we simply use what UGOS already provides.

<p align="center">
  <img src="https://github.com/user-attachments/assets/2f3053ac-35a0-42af-af59-087d0ec2134a" alt="System View" width="600"/>
</p>

The integration has two parts: A Token Server running as a Docker container. It retrieves and renews access authorization tokens. And a Home-Assistant custom integration. It uses the tokens to read data from the NAS by utilizing an UGOS-builtin API, and updates your HA sensors.


---

## 📝 Notes & Feedback

👉 This integration was developed using a **UGreen DXP 4800+** and a **UGreen DXP 480T**. Other models and special setups (like GPU usage in the larger models) might not fully be covered. If you want to help us further developing the integration towards your specific setup, please contribute to the project by posting the API response of your NAS in the [Model Collection](https://github.com/Tom-Bom-badil/home-assistant_ugreen-nas/discussions/43).

使用原仓库(https://github.com/Tom-Bom-badil/home-assistant_ugreen-nas)
修改取消Docker容器获取NAS Token

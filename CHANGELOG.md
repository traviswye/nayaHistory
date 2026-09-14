# NayaFlow release changelog (archived from NayaTech/NayaFlow-releases)

_Captured 2026-09-14. 14 of 25 releases carry release notes._

## v1.25.1  (2026-07-21)

# Release Notes - Hotfix

## 💻 NayaFlow (v1.25.0 -> v1.25.1)

- **Fixed:** **Automatic Update** - Fixed an issue where NayaFlow could fail to update after confirming the software update prompt.

# 1️⃣ First Time Download
⚠️ Note that NayaFlow and NayaFlow-Beta CANNOT run simultaneously. Make sure no Naya processes are open before starting up either one. ⚠️

Release Link: https://github.com/NayaTech/NayaFlow-releases/releases/latest
MacOS ARM Download: https://github.com/NayaTech/NayaFlow-releases/releases/latest/download/NayaFlow-arm64.dmg
MacOS x64 Download: https://github.com/NayaTech/NayaFlow-releases/releases/latest/download/NayaFlow-x64.dmg
Windows Download: https://github.com/NayaTech/NayaFlow-releases/releases/latest/download/NayaFlow-x64-setup.exe

Cheers,
— The Naya Team

## v1.25.0  (2026-07-17)

## 💻 NayaFlow (v1.21.0 -> v1.25.0)
- **Added:** **Windows Code Sign** - Windows builds are now digitally code signed, helping Windows recognize NayaFlow as a trusted application and reduce security prompts. SmartScreen warnings will also decrease over time as the application builds its reputation through more downloads.
- **Added:** **LED Remapping**
  - **Led Mapping Tools** - "Brush" lets you apply a color to individual keys by clicking and holding the left mouse button while moving the cursor over them. "Fill" applies a color to all keys at once by clicking a single key. Each layer can have its own LED mapping data.
  - **LED Color Palette** - The LED color palette allows you to choose the color to apply, as well as create, edit, and delete colors using the color picker. 
 	- **LED View Toggle** - Visualize the LED color on the keymappig board so you can configure your keymap while you see the mapped LED color on each key.
  - **LED Animations** - Predfined LED animations for each specific layer
 
  
<img width="2806" height="1640" alt="led-mapping" src="https://github.com/user-attachments/assets/d284e01c-6527-407c-a13e-4e4ebb31afae" />

<img width="2806" height="1638" alt="color-palette" src="https://github.com/user-attachments/assets/96fe8fe0-29f5-4419-abb4-4236301f1976" />

<img width="2806" height="1638" alt="led-view-toggle" src="https://github.com/user-attachments/assets/5ec3d596-569c-4e24-b80c-20abe6fdfcae" />

<img width="2806" height="1638" alt="animation" src="https://github.com/user-attachments/assets/215402d8-1c11-4c76-a311-680b313ff9b5" />

- **Added:** **Tray Icon Battery Status** - Add toggle in UI settings to hide/show battery status of connected modules in the system tray icon on macOS and Windows and as part of the menubar icon on macOS.

<img width="2004" height="1212" alt="tray-module-battery" src="https://github.com/user-attachments/assets/40636390-833e-4703-9655-7bec60bf582f" />

<img width="1200" height="679" alt="image" src="https://github.com/user-attachments/assets/37974259-a15c-4827-84f6-067c7544e67a" />

<img width="1181" height="704" alt="image (1)" src="https://github.com/user-attachments/assets/7c295912-93ec-4110-849a-7ab9ee019df3" />

- **Added:** **LED Remapping Off** - Add LED Off Option in LED Color Palette with which you can apply LED Off state on each key with the palette tool.

<img width="2698" height="1530" alt="turn-off-leds" src="https://github.com/user-attachments/assets/0eefaae2-bac1-4b5b-910d-2616ebe66931" />


- **Added:** **Activity Timeout Configuration** - Add ability to change the sleep and idle timeouts on NayaCreate through NayaFlow settings. This feature was included in v1.22.0 but omitted from the release note.

<img width="2992" height="1796" alt="image (2)" src="https://github.com/user-attachments/assets/fd4e3cc1-58e7-4d51-b93e-01cea44930e7" />

- **Added:** **Hardware Manager Shortcut Start** - Add ability to start Hardware Manager workflows using keyboard shortcuts. This feature was included in v1.22.0 but omitted from the release note.

<img width="1707" height="530" alt="image (3)" src="https://github.com/user-attachments/assets/502fc069-0777-4b90-a0cf-985bca0eca48" />

- **Added:** **LED Pipet Tool** - activate or create a new colour swatch from the selected colourmap LED.

<img width="2988" height="1802" alt="pipet-highlight" src="https://github.com/user-attachments/assets/e63ba4be-4e50-45f6-837e-5eacc983af2e" />


- **Added:** **Window Scaling** - allow NayaFlow UI to be scaled up or down to fit different screen sizes better. 
- **Added:** **Window Out of Bounds** - add notification informing parts of the UI may be hidden due to a scaling discrepancy.
- **Added:** **Scaling Slider** - add scaling slider to UI settings allowing for manual scaling adjustment.
- **Added:** **Scaling Shortcuts** - CMD/Ctrl+plus and CMD/Ctrl+plus allow the software to be scaled.

<img width="704" height="424" alt="scaling" src="https://github.com/user-attachments/assets/21f4d754-2b1a-4df9-96a6-ab992c4f815b" />


- **Added:** **Double Tap & Tap and Hold** - add **Double Tap** and **Tap and Hold** as new keybinding behaviors, allowing keys to perform more different actions based on how they are pressed.

<img width="1580" height="780" alt="doubletaptapandhold" src="https://github.com/user-attachments/assets/8c158ff4-5234-41c3-9118-da55f70788f7" />

- **Added:** **Manual Backup** - add a manual user data backup option alongside automatic backups. Manual and automatic backups are now stored in separate folders.

<img width="2704" height="1530" alt="image (4)" src="https://github.com/user-attachments/assets/e72f92e4-8bb0-4cc5-a96b-738b23f1df93" />


- **Added:** **LED Action Override Behavior Setting** - add a setting to choose how long LED actions on the keyboard should override the LED colormap.
- **Added:** **LED Maximum Brightness Setting** - add a setting to configure the maximum LED brightness.
- **Added:** **LED Scan Mode Setting** - add a setting to enable LED scanning, reducing power consumption and helping extend LED lifespan.


<img width="2710" height="1548" alt="image (5)" src="https://github.com/user-attachments/assets/9cc61e2d-9433-4a5f-8015-20ce5a0abe3e" />

- **Added:** **Global Shortcut for Saving Changes** - add a global shortcut (**Cmd/Ctrl + S**) to save changes from anywhere in the application.
- **Added:** **Global Shortcut for Flashing Create** - add a global shortcut (**Cmd/Ctrl + D**) to trigger the **FLASH CREATE** action.
- **Added:** **New Default Profile Template** - update the default profile templates to include the latest LED mapping data.

<img width="2714" height="946" alt="image (6)" src="https://github.com/user-attachments/assets/5df054eb-222e-4b44-91da-93c6d69ccd74" />

<img width="2620" height="762" alt="image (7)" src="https://github.com/user-attachments/assets/4d66ea76-abaf-48c5-b9dc-f463fa5e5ca9" />

- **Fixed:** **Diagnostic Report Generation Issue** - The system failed to include an OS version in the generated report.
- **Fixed:** **Saving Color Swatch Fail** - Newly crated color swatches in the LED color palette failed to be saved after clicking the save button.
- **Fixed:** **Communication issue between Flow and Core on Windows** - NayaFlow lost connection to NayaCore (its background worker) after the app window was hidden via the close button and the app shortcut was clicked.
- **Fixed:** **LED Colourmapping UI** - improve LED colourmapping UI by including better tooltips, saturation for new colourswatches defaults of 100, and highlighting colour swatch on LED hover with any tool.
- **Fixed:** **Diagnostics Report** - Due to a silent rename of a MacOS variable on MacOS 26, the diagnostics report failed to complete with all information.
- **Fixed:** **Layer Duplicate** - fix an issue where duplicating a layer did not copy module configuration bindings.

## 💓 NayaCore (v6.6.1 -> v6.11.0)
- **Added:** **Device Detection** - Improved the stability of the device detection by redesigning the system information collection system from the groud up.
- **Added:** **Double Tap & Tap and Hold Support** - add keybinding slot handling and layer serialization for Double Tap and Tap and Hold behaviors when flashing profiles to Create devices.
- **Added:** **LED Profile Settings Commands** - add protocol support for LED scan mode, maximum brightness, and LED action override duration settings from profile data.
- **Added:** **LED Settings SQL Retrieval** - read new LED behavior settings from the user profile database when building the flash payload.
- **Added:** **64-bit Create Firmware Updates** - add support for updating 64-bit Create left and right firmware images.
- **Added:** **Consolidated Firmware Version Checking** - centralize Create, module, and dongle version requirements and command minimum-version lookups.
- **Added:** **Colour Mapping LED OFF State** - Allow for individual LEDs to be configured to be OFF in colour mapping.
- **Fixed:** **Create Pairing Edge Case** - Create Pairing Workflow Stability Issue - The Create Pairing workflow could silently fail. 
- **Fixed:** **Edge Case Handling** - Improve handling of edge cases.
- **Fixed:** **Write Keymap Fail** - Gracefully handle edge case where writing fails due to hold-tap action and hold-tap flavour mismatch. Thanks to user @pictureofitself for flagging the edge case.
- **Fixed:** **Modules Disrespecting Colourmap** - fix modules not following NayaFlow colourmap.
- **Fixed:** **Communication Edge Case** - fix a communication breakdown edge case with NayaCreate caused by a bitflip or corrupted data.
- **Fixed:** **Pairing Initialization** - improve pairing operation handling and add a dedicated error code for pairing init failures.
- **Fixed:** **Pairing Targeting** - fix incorrect pairing target selection in edge-case device states.
- **Fixed:** **Firmware Update BLE Check** - fix BLE version check logic run after keyboard firmware updates.
- **Fixed:** **Command Timeouts** - improve command timeout handling in the ProtocolCDC worker to reduce hung operations.
- **Fixed:** **Profile SQL Error Handling** - improve error handling when reading profile settings from the database.
- **Fixed:** **Dongle Crash** - fixed crash caused by dongle connection.
- **Fixed:** **Profile Debug Logging** - profile print/log output now includes settings data for easier debugging.

## ⌨️ NayaCreate (v3.35.4 -> v3.41.0)
- **Added:** **LED-based Notifications** - Added LED notifications to communicate device statuses, connectivity, battery health, and system events.
- **Added:** **LED Remapping** - Enabled LED remapping on FW side, allowing NayaFlow to configure the LEDs of NayaCreate.
- **Added:** **Colour Mapping LED OFF State** - Allow for individual LEDs to be configured to be OFF in colour mapping.
- **Added:** **LED Action Override Configuration** - add a setting to control whether LED actions can override colors defined by the active LED map. This allows you to prioritize either dynamic LED actions or your custom LED map colors.
- **Fixed:** **Power Cycling** - Power cycling caused due to low internal battery and depleted module battery.
- **Fixed:** **BLE Traffic** - Reduce BLE traffic between keyboard halves to improve battery life and latency.
- **Fixed:** **Handle Edge Cases** - Improve handling of specific edge cases which could cause unpredictable behaviour.
- **Fixed:** **Activity Timeout Bugs** - fix right keyboard waking left on entering idle, Track module not keeping create awake, LEDs getting stuck in a half ON/half OFF position.
- **Fixed:** **Low Battery Notification** - lower treshold for low battery LED notification.
- **Fixed:** **Misaligned LED Colors** - fix an issue where LED colors could become offset or appear on the wrong keys during rapid LED updates.
- **Fixed:** **Tune Phantom Ticks** - fix an issue where the Tune module could occasionally register unintended tick events when switching between layers.

## 🎮 NayaModules (v2.3.2 -> v2.3.3)
- **Fixed:** **Tune Phantom Ticks** - Prevent phantom ticks by improving the algorithm for tracking crown location near ticks.
- **Fixed:** **Disable Battery Blink** - Disable battery blinking of modules as battery can now be fully read out by NayaFlow.


# 1️⃣ First Time Download
⚠️ Note that NayaFlow and NayaFlow-Beta CANNOT run simultaneously. Make sure no Naya processes are open before starting up either one. ⚠️

Layers from NayaFlow v1.19.x are compatible with NayaFlow-Beta v1.21.x.

Release Link: https://github.com/NayaTech/NayaFlow-releases/releases/latest
MacOS ARM Download: https://github.com/NayaTech/NayaFlow-releases/releases/latest/download/NayaFlow-arm64.dmg
MacOS x64 Download: https://github.com/NayaTech/NayaFlow-releases/releases/latest/download/NayaFlow-x64.dmg
Windows Download: https://github.com/NayaTech/NayaFlow-releases/releases/latest/download/NayaFlow-x64-setup.exe

Cheers,
— The Naya Team

## v1.21.0  (2026-04-21)

# Release Notes - Customer Support Report Generation

## 💻 NayaFlow (v1.20.0 → v1.21.0)
- **Added:** **CS Report Generation** - Add one click system diagnostics report generation to enable our Customer Support team to diagnose issues and assist more effectively. <img width="854" height="686" alt="generating a report" src="https://github.com/user-attachments/assets/6d17a6f5-cf5e-4da7-a8c7-f7359587c50c" />

# 1️⃣ First Time Download
⚠️ Note that NayaFlow and NayaFlow-Beta CANNOT run simultaneously. Make sure no Naya processes are open before starting up either one. ⚠️

Layers from NayaFlow v1.19.x are compatible with NayaFlow-Beta v1.21.x.

Release Link: https://github.com/NayaTech/NayaFlow-releases/releases/latest
MacOS ARM Download: https://github.com/NayaTech/NayaFlow-releases/releases/latest/download/NayaFlow-arm64.dmg
MacOS x64 Download: https://github.com/NayaTech/NayaFlow-releases/releases/latest/download/NayaFlow-x64.dmg
Windows Download: https://github.com/NayaTech/NayaFlow-releases/releases/latest/download/NayaFlow-x64-setup.exe

Cheers,
— The Naya Team

## v1.20.0  (2026-04-15)

# Release Notes - Minor Quality of Life

## 💻 NayaFlow (v1.19.0 → v1.20.0)
- **Added:** **MacOS Intel Release** - With this release we are promoting the MacOS Intel build of NayaFlow from BETA to STABLE. This build has been available through BETA for the last several releases and is now deemed stable enough to release.
- **Added:** **Module battery percentage** — You can now see the battery charge state of each connected module when hovering over the device connection info. We are aware of fluctuations between 5 and 10 percent depending on exact connection situation. This is currently being mapped to improve the reported percentage in the future. <img width="1497" height="893" alt="beta release 1" src="https://github.com/user-attachments/assets/4b85c73c-922e-4f88-bb1a-a83158d92140" />
- **Added:** **Add Help Buttons** - Add several help center link buttons throughout NayaFlow software. 
<img width="1495" height="896" alt="beta release 2" src="https://github.com/user-attachments/assets/4877f666-6c85-4bca-b43d-c08c6af411df" /><img width="1407" height="818" alt="beta release 3" src="https://github.com/user-attachments/assets/d235b3d5-da03-4a7a-8357-9c4716df5813" />


## 💓 NayaCore (v6.4.1 → v6.6.1)
- **Added:** **Module battery** — Re-enable module battery reading and validation.

# 1️⃣ First Time Download
⚠️ Note that NayaFlow and NayaFlow-Beta CANNOT run simultaneously. Make sure no Naya processes are open before starting up either one. ⚠️

Layers from NayaFlow v1.19.x are compatible with NayaFlow-Beta v1.20.x.

Release Link: https://github.com/NayaTech/NayaFlow-releases/releases/latest
MacOS ARM Download: https://github.com/NayaTech/NayaFlow-releases/releases/latest/download/NayaFlow-arm64.dmg
MacOS x64 Download: https://github.com/NayaTech/NayaFlow-releases/releases/latest/download/NayaFlow-x64.dmg
Windows Download: https://github.com/NayaTech/NayaFlow-releases/releases/latest/download/NayaFlow-x64-setup.exe

Cheers,
— The Naya Team

## v1.19.1  (2026-04-03)

# Release Notes - BLE v2 & Quality of Life Update
Hiya everyone!

This STABLE release brings together two major BETA updates into one: the complete BLE v2 overhaul and a set of quality of life improvements across NayaFlow and NayaCore.

If you've been with us for a while, you probably know that Bluetooth stability and reliability have been one of the weaker spots in NayaCreate. We realized pretty early on that properly fixing it would take more than small patches here and there — it needed a full rebuild. Until now, we've been fixing issues as they popped up, but that approach could only take us so far.

With this update, we're finally rolling out a completely rewritten Bluetooth layer for NayaCreate — one that we fully control from end to end.

That's opened the door to some big improvements: much better reliability across Debian Linux, Windows, macOS, iPadOS, iOS, and Android, higher bandwidth between keyboard halves and between NayaCreate and the host, lower BLE latency down to 7.5ms on most platforms, stronger host connection security at Level 4 (*yes, the "military grade" kind* 😄), and much deeper insight into connected BLE host devices.

One small note for Apple users: Apple platforms enforce a 15ms minimum on non-Apple devices, so while things are still much improved there too, they won't go below that limit.

When you update your NayaCreate from BLE v1 to BLE v2 all of the known hosts on NayaCreate will be removed so that when you connect to them again, they will be using the new Bluetooth library configuration. Going forward, each slot has a different name. If you are connecting to slot 1 on NayaCreate, you should connect to the Bluetooth device named NayaCreate BLE 1, if you are connecting to slot 2 the device name will be NayaCreate BLE 2, et cetera. Note that on some hosts you have to restart the Bluetooth to see the correct slot name.

On top of BLE v2, we've also packed in a bunch of quality of life improvements on the NayaFlow side — including GIFs and photos in the notes below so you can see the changes more clearly!

## 💻 NayaFlow (v1.17.1 → v1.19.0)
### BLE v2 & Connection Features
- **Added:** **Connection Settings** — A new settings tab now shows the connection status of all connected Naya devices, including Bluetooth device information.
- **Added:** **Naya Device Status** — Connected devices are now shown in the top bar of NayaFlow. Hovering over the icon reveals more device details.
- **Added:** **Create Split Connection Warning** — When NayaCreate Left and NayaCreate Right fail to establish a connection, Flow displays a warning icon in the topbar and a pop-up.
![1-warning popups](https://github.com/user-attachments/assets/e605c527-3d8e-4d62-b2ce-72903e0f0d5c)

### Profile & UI Improvements
- **Added:** **Minor UI/UX improvement for profiles** — Renamed "onboard profile" and "stored profile" to "Active profile (flashes to Naya device)" and "Inactive profile (saves to NayaFlow only)" respectively to improve clarity.
<img width="1854" height="762" alt="image" src="https://github.com/user-attachments/assets/6e994723-f25d-40ed-82dc-0294262ead76" />

- **Added:** **Active/Inactive Profile Indicator** — Added currently active indicator to keymapping profiles. A Naya logo indicates that the currently viewed profile will be flashed to NayaCreate. If a number is shown, the currently viewed profile will only be saved to NayaFlow.
![3-profile-indicator-naya-flow](https://github.com/user-attachments/assets/638a8a10-787f-4725-bf27-8119c15a518c)

- **Added:** **Minor UI/UX improvement in Hardware Manager** — Disabled workflow start button and added a tooltip on hover with instruction to disconnect devices in red to proceed.
![4-disabled-workflow-on-red-devices-naya-flow](https://github.com/user-attachments/assets/6f64111b-9a27-4423-8f37-cc5db05810f7)

- **Added:** **Minor UI/UX improvement in FLASH CREATE button** — Disabled FLASH CREATE button on unsaved changes or the currently edited profile is not the active profile. When button is enabled and hovered over, displays the name of the profile to be flashed to NayaCreate. 
![5-disabled-flash-create-button](https://github.com/user-attachments/assets/b573b8f8-06dc-4614-aa86-187a062140cf)

### Utility & Troubleshooting
- **Added:** **Manual Software Update Check** — A new "Check for Updates" button in Settings lets you manually check for NayaFlow updates.
![6-manual-update-check](https://github.com/user-attachments/assets/a645ebdd-1d3a-46b0-8b65-43f513da94e7)

- **Added:** **SPI Flash Test and Format** — Added a "Test and Format SPI Flash" button to the Troubleshooting section in Settings.
- **Added:** **Clear BLE Devices** — Added a "Clear BLE Devices" button to the Troubleshooting section in Settings.
- **Added:** **App Focus on Quit** — When quitting NayaFlow from the tray icon (Windows) or menu bar icon (macOS), the app now opens/focuses itself to provide visual confirmation that it is closing.
- **Added:** **Resizable Window** — The NayaFlow window can now be resized, with minimum height and width limits in place.

### Bug Fixes
- **Fixed:** **Windows Auto-Updater Retry Issue** — The auto-updater could fail on Windows because the updater process was being interrupted when NayaFlow quit.
- **Fixed:** **macOS Intel / Windows Auto-Updater Mix-Up** — Due to the macOS Intel release of NayaFlow, the Windows auto-updater ended up tracking the wrong OS. We do not expect issues for Windows users, but macOS Intel users should install the latest NayaFlow manually.
- **Fixed:** **Key Combo Recording** — When one single action, which is not a modifier key, is recorded, the recorded action icon was mistakenly displayed as a question symbol.
- **Fixed:** **Removed No Updates Available Popup** — When NayaFlow starts, a pop-up was previously shown to indicate that there are no new updates. The pop-up has been removed as it provides no new useful information.

## 💓 NayaCore (v6.1.5 → v6.4.1)
- **Added:** **BLE v2 Support** — Added support for BLE v2, along with improvements to device information gathering and pairing workflows.
- **Added:** **SPI Flash Test and Format** — Added the ability to test and format corrupted SPI flash sectors on NayaCreate.
- **Added:** **Clear All BLE Devices** — Added the ability to clear all BLE devices stored on NayaCreate, which can help when Bluetooth data becomes corrupted.
- **Added:** **Device Human Names** — Each keyboard half now gets a human-readable name generated from its hardware ID.
- **Fixed:** Resolved **19 issues**, improving overall performance and stability.

## ⌨️ NayaCreate (v3.31.1 → v3.35.4)
- **Added:** **BLE v2** — BLE on NayaCreate has been completely rebuilt to address most of the issues seen with the previous implementation and to significantly improve latency across all platforms. Please note that macOS will not go below 15ms, as this is enforced by the OS.
- **Added:** **Module Battery Management** — Introduced a new module battery management system, improving battery performance by **10%**.
- **Fixed:** Resolved **10 issues**, improving connection performance and overall stability.

Cheers,
— The Naya Team

## v1.17.3  (2026-02-18)

## 💻 NayaFlow (v1.17.2 → v1.17.3)
- **Fix issue:** NayaCore log files were incorrectly written to the `NayaFlow-Beta` directory instead of the `NayaFlow` directory.

## v1.17.2  (2026-02-18)

## 💻 NayaFlow (v1.15.1 → v1.17.2)
- **Add feature:** Periodic Backup of User Data — every 30 min a backup will be taken of all user data, provided any changes are found.
- **Add feature:** Logging system file rotation — streamline log handling for NayaFlow and reduce file size growth.
- **Add feature:** Software Info — add a section in NayaFlow settings showing all software versions in one place. *(Note: keyboard and module firmware versions currently on device can only be seen in Device Manager.)*
- **Updated feature:** Hardware Manager — rename DeviceManager to Hardware Manager to avoid confusion with the Windows OS Device Manager.
- **Updated feature:** Hardware Manager — improve UIUX and functionality to match new NayaCore redesign.
- **Update feature:** NayaFlow←→NayaCore Communication — update communication to and from NayaCore to follow improved conventions and new message types.
- **Fix issue:** **Cmd + Return** creates an empty window on macOS Tahoe 26.2 — shortcut has been disabled inside NayaFlow.
- **Fix issue:** Multiple issues preventing child processes from exiting correctly.
- **Fix issue:** Log files could exceed 100MB.
- **Fix issue:**  Global Shortcuts - Refresh and force refresh global shortcuts were not disabled.
- **Fix issue:**  Default Profile Templates (On Windows) - Default profile templates were not loaded on Windows.
- **Add feature(BETA ONLY):**  MacOS Intel - rebuild and configure NayaFlow for operation on Intel based Macs. This build will currently only be available on BETA as we verify the stability.

## 💓 NayaCore (v5.8.1 → v6.1.5)
- **Breaking change:** NayaFlow<>NayaCore Communication — streamline, improve, and expand communication conventions to provide a better user experience.
- **Add feature:** Comprehensive Logging — added detailed logging to NayaCore to enable faster and more effective Customer Support troubleshooting.
- **Add feature:** Manufacturing Build — merged our manufacturing tool with NayaCore. Starting with the last batch of hardware, a custom build of NayaCore has been used for all testing and validation. In a near-future update, this merge will allow remote diagnostics of NayaCreate for all users, similar to our manufacturing workflows.
- **Add feature:** NayaCore<>NayaCreate Communication — drastically improve performance and reliability by retiring the engineering communication channel (SystemCDC).
- **Update feature:** Hardware Manager — streamline Hardware Manager to improve user experience and minimize development overhead.
- **Fix issue:** Critical bugs causing unexpected quitting — we identified and fixed 6 critical edge-case issues that could cause NayaCore to prematurely exit, as well as 30+ bugs in the system.
- **Fix issue:** Corrupted FW File - Handle corrupted module FW file on NayaCreate correctly.
- **Fix issue:** Module Batt - correct module battery reporting to NayaFlow.
- **Fix issue:** Memory Violation - Race condition causing access of corrupted memory.
- **Fix issue:** Behavior Settings  - Interrupt Flavor  and Tapping Term  settings were not applied to NayaCreate in some cases.
- **Add feature(BETA ONLY):** MacOS Intel - rebuild and configure NayaCore for operation on Intel based Macs. This build will currently only be available on BETA as we verify the stability.

## ⌨️ NayaCreate (v0.3.29.1 → v0.3.31.1)
- **Add feature:** LED PWM Power Control — lower power consumption of NayaCreate by **~50%** with LED brightness set to max.
- **Fix issue:** Under the Hood Improvement — a number of under-the-hood improvements to speed up performance and communication with NayaModule.
- **Fix issue:** LED Desync — fix an issue where LED colours between left and right half desync on boot and after sleep.
- **Perf:** SystemCDC Retirement — improve performance by **~5%** by fully retiring SystemCDC.

## 🎮 NayaModules (v2.1.1 → v2.3.2)
- **Add feature:** LED PWM Power Control — lower power consumption of NayaTune by **~20%** with LED brightness set to max.
- **Fix issue:** NayaTune Ticks — improve tick accuracy on NayaTune to be exact instead of estimated.
- **Fix issue:** Under the Hood Improvement — a number of under-the-hood improvements to speed up performance and communication with NayaCreate.

## v1.15.1  (2026-01-06)

## What’s fixed
NayaFlow **1.15.1** (updating from **1.15.0 → 1.15.1**) updates device readiness detection so newly delivered Naya Create units are recognized correctly for **keymap flashing**. Please refer to the previous message for additional context.

## v1.15.0  (2025-11-07)

## 💻 NayaFlow (v1.14.5 → v1.15.0)
- Added Input Source selection (JIS | QWERTY) — [learn more here](https://help.naya.tech/Input-Source-Selection-JIS-2a4e8a2f50ec8008a7fbdcfa977df36c).
- Added Default Template System with JP/US Intl layout templates.
- Added Force Module Update feature — [learn more here](https://help.naya.tech/Force-Flashing-Naya-Modules-2a4e8a2f50ec806cab5efabf92726f37).
- Updated Naya Default Templates — [learn more here](https://help.naya.tech/Default-Templates-v2-Update-2a4e8a2f50ec808d8d58f767cfe08754).
- Fixed: Delete key not being recorded on Windows.
- Fixed: “Num Lock” missing from the action palette.

## ❤️ NayaCore (v5.5.2 → v5.8.1)
- Added Force Module Update feature — [learn more here](https://help.naya.tech/Force-Flashing-Naya-Modules-2a4e8a2f50ec806cab5efabf92726f37).
- Improved USB driver handling to prevent crashes on certain machines.
- Improved communication between Core and Create.
- Greatly improved keyboard flashing speed (up to 2.5× faster).
- Fixed: Keymap flashing failure on some keyboards.
- Fixed: Updating not possible on some older firmware versions.
- Fixed: Dongle could cause Core to get stuck on some machines.

## ⌨️ NayaCreate (v3.28.7 → v3.29.1)
- Added Module Force Update feature — [learn more here](https://help.naya.tech/Force-Flashing-Naya-Modules-2a4e8a2f50ec806cab5efabf92726f37).
- Improved communication performance between left and right halves.
Fixed: Module update method to prevent wrong firmware from being installed.

## 🎮 NayaModules (v2.1.2 → v2.2.0)
- Added Module Force Update feature — [learn more here](https://help.naya.tech/Force-Flashing-Naya-Modules-2a4e8a2f50ec806cab5efabf92726f37).
- Fixed: Brightness sync for animations.

## v1.14.5  (2025-10-03)

# 🚑 HotFix Release

## 💻 NayaFlow (v1.14.3 → v1.14.5)
- Fixed: Tooltip texts for layer actions were shown in Japanese even when the UI language setting is set to English.
- Fixed: Some texts on the firmware update screen were incorrectly translated in Japanese.

## 💓 NayaCore (v5.5.1 → v5.5.2)
- Bump version to include new Create & Module Firmware

## ⌨️ NayaCreate (v0.3.28.6 → v0.3.28.7)
- Fixed: Fix for Hold-tap keys getting stuck when two are activated at the same time. Due to a human mistake this was not included in the last release. Soon everything will be automated to avoid issues like this ❤️

## 🎮 NayaModules (v2.1.1 → v2.1.2)
- Fixed: Track module scrolling (rotate around Z-axis) activated too easily.

— The Naya Team

## v1.14.3  (2025-10-02)

_No release notes provided._

## v1.11.11  (2025-09-19)

_No release notes provided._

## v1.11.10  (2025-09-15)

_No release notes provided._

## v1.11.9  (2025-09-12)

_No release notes provided._

## v1.11.8  (2025-09-12)

_No release notes provided._

## v1.11.0  (2025-09-07)

_No release notes provided._

## v1.6.10  (2025-07-24)

_No release notes provided._

## v1.6.5  (2025-07-14)

_No release notes provided._

## v1.6.4  (2025-07-13)

_No release notes provided._

## v1.3.11  (2025-06-15)

1. Fix "Duplicate" button on the profile list staying disabled.
2. Fix Onboard profile not being able to be changed, interfering with flashing of Create.
3. Fix Flow freeze after computer wake from sleep.

## v1.3.8  (2025-06-13)

1. Custom key remapping now available, with some limitations as we gradually roll out more features:
   1. Only the ‘Press’ behaviour is available.
   2. Limited action selection
   3. Disabled Action combinations executed with single keypress
2. Module recovery support for battery Zero included, step-by-step instructions to follow next week
3. A completely redeveloped Naya Core
   1. Updating still executed through a prior variant of Core
4. Naya Create BLE stability improvements
   1. Fixed a device pairing bug
   2. Fixed a device not showing up on windows bug
   3. Improved a random Windows device connection drop

## v0.1.1  (2025-05-02)

1. Patch – Remove Unnecessary File
    a. Removed an unnecessary unnecessary file decreasing the final application size by 40MB.

## v0.1.0  (2025-05-01)

1. Critical Fix – Module Charging on Batch 1 / DVT#2
    a. Resolved a firmware bug where Batch 1 / DVT#2 units could not charge modules when plugged in via USB.
2. Naya Flow Auto Updater Bug Fix
    a. Resolved a bug in Naya Flow which prevented the software from automatically updating to a new version.
3. Track Module Support
    a. Track module is now enabled.
    b. Refer to the Track user manual for current functionality.
4. Scroll Direction Toggle
    a. You can now independently toggle scroll direction for compatible modules, regardless of OS mode.
    b. Your preference is saved and persists between restarts.
5. Tune Module: Separate Configs for Left and Right Halves
    a. Left and Right Create halves can now have independent Tune configurations.
    b. Cycle between them using the “Cycle Tune Mode” shortcut. Refer to the Create user manual page 18. We will update the Tune user manual to include explanations of the default modes, watch out for version 1.0.3.
    c. Note: Only preloaded configurations are currently supported.
6. Bluetooth Stability Improvements
    a. Improved pairing reliability for macOS 14+ and Windows 10/11.
    b. Better keyboard-to-keyboard communication.
7. Dongle Support Preparation
    a. Slot 5 is now reserved for future BLE dongle support.
    b. Slots 1–4 remain user-assignable.

## v0.0.2  (2025-03-19)

_No release notes provided._

## v0.0.1  (2025-03-19)

_No release notes provided._

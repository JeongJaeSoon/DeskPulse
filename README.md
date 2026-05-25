# DeskPulse

ESP32 desk-side usage monitor for Claude Code and Codex.

DeskPulse is maintained as a separate multi-provider fork of
[HermannBjorgvin/Clawdmeter](https://github.com/HermannBjorgvin/Clawdmeter).
The GitHub fork relationship is intentionally retained. See
[UPSTREAM.md](UPSTREAM.md) for origin, attribution, and license notes.

Some runtime names still use the original `Claude Controller` and
`claude-usage-daemon` identifiers for compatibility with existing BLE pairing
and service setup.

## Supported Hardware

- [Waveshare ESP32-S3-Touch-AMOLED-2.16](https://www.waveshare.com/esp32-s3-touch-amoled-2.16.htm?&aff_id=149786)
- [Waveshare ESP32-C6-Touch-AMOLED-2.16](https://www.waveshare.com/esp32-c6-touch-amoled-2.16.htm?&aff_id=149786)
- [Waveshare ESP32-S3-Touch-AMOLED-1.8](https://www.waveshare.com/esp32-s3-touch-amoled-1.8.htm?&aff_id=149786)

Board env names:

- `waveshare_amoled_216`
- `waveshare_amoled_18`

## Requirements

- PlatformIO CLI
- macOS: `python3`
- Linux: `curl`, `bluetoothctl`, `busctl`
- Claude Code login for Claude usage
- Codex / ChatGPT login for Codex usage

If `pio` is not on your PATH, try `~/.platformio/penv/bin/pio`.

## macOS Setup

### 1. Flash firmware

```bash
./flash-mac.sh waveshare_amoled_216
./flash-mac.sh waveshare_amoled_18 /dev/cu.usbmodem1101
```

The first command auto-detects `/dev/cu.usbmodem*`. Pass the serial port
explicitly if more than one device is connected.

### 2. Pair Bluetooth

After flashing, open **System Settings -> Bluetooth** and connect to
`Claude Controller`.

The daemon discovers the device by that BLE name.

### 3. Install daemon

```bash
./install-mac.sh
```

The installer:

- creates `daemon/.venv/`
- installs `bleak` and `httpx`
- creates `daemon/config.toml` if missing
- installs `~/Library/LaunchAgents/com.user.claude-usage-daemon.plist`
- starts the LaunchAgent

On first run, allow the macOS Bluetooth permission prompt.

### 4. Choose provider

```bash
./switch-provider.sh both
./switch-provider.sh claude
./switch-provider.sh codex
```

The provider setting is stored in `daemon/config.toml`.

Provider priority:

1. CLI flag: `daemon/.venv/bin/python daemon/claude_usage_daemon.py --provider both`
2. Environment variable: `CLAWDMETER_PROVIDER=both`
3. Config file: `daemon/config.toml`
4. Built-in fallback: `claude`

### 5. Check logs

```bash
tail -F ~/Library/Logs/claude-usage-daemon.out.log
```

In `both` mode, a healthy payload includes:

```text
"p":"both"
"c":{...,"ok":true}
"x":{...,"ok":true}
```

Useful service commands:

```bash
launchctl list | grep claude-usage
launchctl unload ~/Library/LaunchAgents/com.user.claude-usage-daemon.plist
launchctl load -w ~/Library/LaunchAgents/com.user.claude-usage-daemon.plist
```

## Linux Setup

The Linux installer currently uses the legacy Claude-only shell daemon.

### 1. Flash firmware

```bash
./flash.sh waveshare_amoled_216
./flash.sh waveshare_amoled_18 /dev/ttyACM1
```

### 2. Pair Bluetooth

```bash
bluetoothctl scan le
bluetoothctl pair <MAC>
bluetoothctl trust <MAC>
```

Pair the device named `Claude Controller`. The MAC address is also shown on the
Bluetooth screen.

### 3. Install daemon

```bash
./install.sh
systemctl --user start claude-usage-daemon
```

Useful service commands:

```bash
systemctl --user status claude-usage-daemon
journalctl --user -u claude-usage-daemon -f
systemctl --user restart claude-usage-daemon
systemctl --user stop claude-usage-daemon
```

## Screen Controls

Main screen cycle:

```text
Usage -> Claude -> Codex -> Bluetooth -> Usage
```

Buttons:

| Button | Function |
| ------ | -------- |
| Left | Hold to send Space |
| Middle / PWR | Cycle screens; on splash, cycle animations |
| Right | Press to send Shift+Tab |

Tap the screen to toggle between splash and the last non-splash screen.

## Development References

- Board porting: [docs/porting/adding-a-board.md](docs/porting/adding-a-board.md)
- HAL contract: [docs/porting/hal-contract.md](docs/porting/hal-contract.md)
- Upstream origin and attribution: [UPSTREAM.md](UPSTREAM.md)

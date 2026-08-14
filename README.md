<div align="center">

# 🎀 Aigis Music Bot

<!-- Language Switcher Bar -->
<p align="center">
  <a href="#-tiếng-việt"><b>🇻🇳 Tiếng Việt</b></a> •
  <a href="#-english"><b>🇬🇧 English</b></a>
</p>

<!-- Professional Flat Badges Row 1: Core Tech & Status -->
<p align="center">
  <a href="https://github.com/2amkeyl/aigis-bot/releases/latest"><img src="https://img.shields.io/badge/Release-v1.0.0-blue.svg?style=flat-square" alt="Latest Release" /></a>
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/Python-3.12+-3776AB.svg?style=flat-square&logo=python&logoColor=white" alt="Python Version" /></a>
  <a href="https://discordpy.readthedocs.io/"><img src="https://img.shields.io/badge/discord.py-v2.x-5865F2.svg?style=flat-square&logo=discord&logoColor=white" alt="discord.py" /></a>
  <a href="https://www.docker.com/"><img src="https://img.shields.io/badge/Docker-Ready-2496ED.svg?style=flat-square&logo=docker&logoColor=white" alt="Docker Ready" /></a>
  <a href="https://github.com/yt-dlp/yt-dlp"><img src="https://img.shields.io/badge/yt--dlp-Active-FF0000.svg?style=flat-square&logo=youtube&logoColor=white" alt="yt-dlp" /></a>
</p>

<!-- Professional Flat Badges Row 2: Stats & Community -->
<p align="center">
  <a href="https://github.com/2amkeyl/aigis-bot/stargazers"><img src="https://img.shields.io/github/stars/2amkeyl/aigis-bot?style=flat-square&color=ffd700&logo=github" alt="GitHub Stars" /></a>
  <a href="https://github.com/2amkeyl/aigis-bot/network/members"><img src="https://img.shields.io/github/forks/2amkeyl/aigis-bot?style=flat-square&color=blueviolet&logo=github" alt="GitHub Forks" /></a>
  <a href="https://discord.gg/5XbvxEkCbG"><img src="https://img.shields.io/badge/Support_Server-Join_Discord-5865F2.svg?style=flat-square&logo=discord&logoColor=white" alt="Discord Support Server" /></a>
  <a href="https://discord.com/users/1147592525696204822"><img src="https://img.shields.io/badge/Developer-Keyl-10B981.svg?style=flat-square&logo=discord&logoColor=white" alt="Developer Contact" /></a>
  <a href="https://github.com/2amkeyl/aigis-bot/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-green.svg?style=flat-square" alt="License" /></a>
  <img src="https://img.shields.io/badge/Uptime-24%2F7_Ready-brightgreen.svg?style=flat-square" alt="Uptime 24/7" />
</p>

---

<p align="center">
  <b>Một Discord Music Bot hiệu năng cao, tối ưu tài nguyên viết bằng Python & Docker.</b><br>
  Phát nhạc trực tiếp từ YouTube, SoundCloud & Spotify với luồng âm thanh Opus chất lượng cao và cơ chế bypass chặn IP.
</p>

</div>

---

<a name="-tiếng-việt"></a>
## 🇻🇳 Tiếng Việt

### 📑 Mục Lục
1. [Tổng quan](#-tổng-quan)
2. [Tính năng nổi bật](#-tính-năng-nổi-bật)
3. [Kiến trúc hệ thống](#-kiến-trúc-hệ-thống)
4. [Yêu cầu hệ thống](#-yêu-cầu-hệ-thống)
5. [Hướng dẫn cài đặt & Triển khai](#-hướng-dẫn-cài-đặt--triển-khai)
6. [Danh sách lệnh (Commands)](#-danh-sách-lệnh-commands)
7. [Kinh nghiệm triển khai VPS / Cloud 24/7](#-kinh-nghiệm-triển-khai-vps--cloud-247)
8. [Xử lý sự cố (Troubleshooting)](#-xử-lý-sự-cố-troubleshooting)
9. [Công nghệ sử dụng](#-công-nghệ-sử-dụng)
10. [Giấy phép & Bản quyền](#-giấy-phép--bản-quyền)

---

### 🌟 Tổng quan
**Aigis Music Bot** là giải pháp phát nhạc Discord self-hosted tinh gọn, ổn định và tối ưu tài nguyên phần cứng. Bot được lấy cảm hứng từ nhân vật **Aigis** trong tựa game *Persona 3 Reload*, tích hợp phản hồi hoàn toàn bằng tiếng Việt thân thiện, rõ ràng và mạch lạc.

> ⚠️ **Lưu ý về phương thức điều khiển:** Bot vận hành hoàn toàn bằng **tiền tố cố định (Prefix `!`)**, không sử dụng Slash Commands (`/`). Điều này giúp bot nhận diện lệnh tức thì, tối ưu độ trễ và không bị phụ thuộc vào phân quyền slash command phức tạp.

---

### ✨ Tính năng nổi bật

* **🎵 Đa nguồn phát âm thanh:** Hỗ trợ link trực tiếp hoặc tìm kiếm theo từ khóa từ **YouTube**, **SoundCloud** và **Spotify** (Track / Album / Playlist).
* **🎶 Xử lý Spotify thông minh:** Trích xuất metadata bài hát qua Spotify Web API và tự động khớp nối bản thu chất lượng cao nhất trên YouTube để phát trực tiếp (bỏ qua giới hạn DRM).
* **🎧 Opus Passthrough Stream:** Ưu tiên truyền tải luồng Opus nguyên gốc từ nguồn phát đến Discord Voice Channel, hạn chế tối đa việc re-encode qua FFmpeg nhằm tiết kiệm CPU và giữ trọn dải âm.
* **🛡️ Chống chặn IP (Anti-Bot Bypass):** Tích hợp sẵn dịch vụ giải mã PoToken nội bộ (`bgutil-ytdlp-pot-provider`), giúp giải quyết triệt để vấn đề `429 Too Many Requests` và lỗi `Sign in to confirm you're not a bot` của YouTube khi chạy trên VPS/Datacenter.
* **🔁 Quản lý hàng đợi chuyên nghiệp:** Hỗ trợ xem danh sách chờ, xáo trộn bài hát (`shuffle`), cùng 3 chế độ lặp linh hoạt (Tắt / Lặp 1 bài / Lặp toàn bộ hàng đợi).
* **⚡ Tự động phục hồi (Auto-Reconnect):** Cơ chế tự động kết nối lại luồng audio khi mạng bị gián đoạn giữa chừng mà không làm gián đoạn cả phiên nghe nhạc.

---

### 🏗️ Kiến trúc hệ thống

```text
               ┌────────────────────────────────────────────────────────┐
               │                     MẠNG DOCKER NỘI BỘ                │
               │                                                        │
[Discord API] ──► [ Container: bot ] ──(Lấy PoToken)──► [ Container:    │
       │       │   ├── discord.py                      │  pot-provider ]│
       ▼       │   ├── yt-dlp                          └────────────────┘
[Voice Channel]│   └── FFmpeg (Opus Stream)                     │
   (Âm thanh)  └────────────────────────────────────────────────┘
                               ▲
             [YouTube / SoundCloud / Spotify API]
```

Hai container chạy độc lập trong cùng một Docker Network nội bộ và giao tiếp qua biến `POT_PROVIDER_URL`, tuyệt đối không cần mở bất kỳ port nào ra Internet ngoài.

---

### 📦 Yêu cầu hệ thống

- **Docker:** Phiên bản `>= 20.10` & **Docker Compose** `>= v2.0`.
- **Discord Bot Token:** Tạo tại [Discord Developer Portal](https://discord.com/developers/applications) *(Cần bật **Server Members Intent** & **Message Content Intent**)*.
- *(Tùy chọn)* **Spotify API Credentials:** Client ID & Client Secret lấy từ [Spotify Developer Dashboard](https://developer.spotify.com/dashboard).

---

### 🚀 Hướng dẫn cài đặt & Triển khai

#### 1. Clone mã nguồn
```bash
git clone https://github.com/2amkeyl/aigis-bot.git
cd aigis-bot
```

#### 2. Thiết lập biến môi trường
Tạo file `.env` tại thư mục gốc:
```bash
cp .env.example .env  # hoặc tạo file .env mới
```

Điền các thông số tương ứng vào `.env`:
```env
# [BẮT BUỘC] Token Bot Discord của bạn
TOKEN=your_discord_bot_token_here

# [TÙY CHỌN] Cấu hình Spotify (Bỏ trống nếu không dùng link Spotify)
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret

# [DEBUG] Đặt 1 để in chi tiết log yt-dlp, đặt 0 khi chạy thực tế
YTDLP_DEBUG=0
```

> 🔒 **Cảnh báo bảo mật:** Tuyệt đối không đẩy file `.env` lên GitHub hoặc chia sẻ token bot cho bất kỳ ai.

#### 3. Khởi chạy với Docker Compose (Khuyên dùng)
```bash
# Build và chạy ngầm bot cùng dịch vụ PoToken
docker compose up -d --build

# Xem log hoạt động trực tiếp của bot
docker compose logs -f bot

# Dừng bot
docker compose down
```

---

### 🕹️ Danh sách lệnh (Commands)

> Toàn bộ lệnh đều sử dụng tiền tố cố định `!`

| Lệnh | Cú pháp | Yêu cầu Voice | Mô tả chi tiết |
| :--- | :--- | :---: | :--- |
| `!play` | `!play <tên bài / link URL>` | 🟢 Có | Tìm và phát nhạc từ YouTube, SoundCloud, Spotify hoặc nạp vào hàng đợi. |
| `!skip` | `!skip` | 🟢 Có | Bỏ qua bài hát đang phát và chuyển sang bài kế tiếp. |
| `!pause` | `!pause` | 🟢 Có | Tạm dừng phát luồng âm thanh hiện tại. |
| `!resume` | `!resume` | 🟢 Có | Tiếp tục phát lại bài hát đang tạm dừng. |
| `!queue` | `!queue` | ⚪ Không | Hiển thị danh sách các bài hát đang chờ trong hàng đợi. |
| `!loop` | `!loop` / `!loop all` / `!loop off` | 🟢 Có | Chuyển chế độ lặp: lặp 1 bài / lặp cả hàng đợi / tắt chế độ lặp. |
| `!shuffle`| `!shuffle` | 🟢 Có | Xáo trộn ngẫu nhiên toàn bộ danh sách bài hát trong hàng đợi. |
| `!stop` | `!stop` | 🟢 Có | Dừng nhạc ngay lập tức và xóa sạch toàn bộ hàng đợi. |
| `!leave` | `!leave` | ⚪ Không | Ngắt kết nối và yêu cầu bot rời khỏi kênh thoại. |
| `!help` | `!help` | ⚪ Không | Hiển thị bảng tóm tắt hướng dẫn các lệnh khả dụng. |

---

### ☁️ Kinh nghiệm triển khai VPS / Cloud 24/7

Dự án được tối ưu để hoạt động ổn định trên các VPS cấu hình nhẹ (như Google Cloud `e2-micro` Always Free Tier hoặc Oracle Cloud Free Tier):

#### 1. Bật Swap Memory (Dành cho VPS RAM ≤ 1GB)
Để tránh hiện tượng Out-Of-Memory (OOM) khi Docker build và nạp thư viện:
```bash
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

#### 2. Khắc phục triệt để lỗi YouTube Bot-Check bằng Cookie
Nếu dải IP VPS của bạn bị YouTube gắn cờ bot-check:
1. Dùng tiện ích trình duyệt (ví dụ: *Get cookies.txt LOCALLY*) export file cookie từ tài khoản Google phụ ở định dạng Netscape.
2. Đặt file vào thư mục dự án với tên `cookies.txt`.
3. Mount vào `docker-compose.yml`:
   ```yaml
   services:
     bot:
       volumes:
         - ./cookies.txt:/app/cookies.txt:ro
   ```

---

### 🛠️ Xử lý sự cố (Troubleshooting)

<details>
<summary><b>1. Bot vào kênh thoại nhưng không phát ra tiếng rồi tự thoát?</b></summary>

- Kiểm tra xem FFmpeg hoặc các thư viện giải mã giọng nói (`libopus`, `PyNaCl`) đã được cài đặt hoàn chỉnh trong môi trường chạy hay chưa.
- Kiểm tra quyền hạn của Bot trong kênh thoại (cần quyền `Connect` và `Speak`).
</details>

<details>
<summary><b>2. Lỗi "Sign in to confirm you're not a bot" hoặc lỗi 429?</b></summary>

- Kiểm tra container `pot-provider` có đang chạy ổn định không: `docker compose logs pot-provider`.
- Tiến hành mount file `cookies.txt` theo hướng dẫn cấu hình VPS ở trên.
</details>

<details>
<summary><b>3. Bot không nhận link Spotify?</b></summary>

- Đảm bảo `SPOTIFY_CLIENT_ID` và `SPOTIFY_CLIENT_SECRET` trong file `.env` đã được điền chính xác.
- Đảm bảo playlist/album Spotify bạn chia sẻ đang ở chế độ Công khai (Public).
</details>

---

### 🧰 Công nghệ sử dụng

* **Ngôn ngữ:** [Python 3.12+](https://www.python.org/)
* **Discord API Wrapper:** [discord.py v2.x](https://github.com/Rapptz/discord.py)
* **Xử lý luồng âm thanh:** [yt-dlp](https://github.com/yt-dlp/yt-dlp) & [FFmpeg](https://ffmpeg.org/)
* **Tích hợp Spotify:** [Spotipy](https://github.com/spotipy-dev/spotipy)
* **Giải pháp Anti-Bot YouTube:** [bgutil-ytdlp-pot-provider](https://github.com/Brainicism/bgutil-ytdlp-pot-provider)
* **Container hóa:** [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/)

---

### 📄 Giấy phép & Bản quyền

Dự án được phân phối dưới giấy phép **MIT License**. Xem chi tiết tại [LICENSE](LICENSE).

*Dự án được xây dựng phục vụ mục đích học tập và nghiên cứu phi thương mại. Vui lòng tuân thủ Điều khoản dịch vụ của YouTube và Spotify khi sử dụng.*

---

<a name="-english"></a>
## 🇬🇧 English

### Overview
**Aigis Music Bot** is an efficient, reliable, and lightweight self-hosted Discord music bot written in Python and fully containerized with Docker. Inspired by **Aigis** from *Persona 3 Reload*, the bot delivers high-quality audio streams with zero-fuss setup and robust anti-bot measures.

> ⚠️ **Command Format:** The bot strictly uses the **prefix `!`** (Slash commands are not used).

### Key Features
- **Multi-Source Audio:** Stream directly from YouTube, SoundCloud, and Spotify.
- **Smart Spotify Resolution:** Resolves Spotify tracks/albums via Spotify Web API and streams the highest matching audio stream from YouTube.
- **Opus Passthrough:** Preserves native Opus stream quality while minimizing CPU usage.
- **Anti-Bot Protection:** Bundled with PoToken provider (`bgutil-ytdlp-pot-provider`) to eliminate YouTube `429` and bot-verification errors on datacenter VPS IPs.
- **Queue Controls:** Loop modes (Single, All, Off), Shuffle, and clean Queue inspection.

### Quick Start with Docker

1. **Clone repo & setup environment:**
   ```bash
   git clone https://github.com/2amkeyl/aigis-bot.git
   cd aigis-bot
   cp .env.example .env
   ```

2. **Configure `.env`:**
   ```env
   TOKEN=your_discord_bot_token_here
   SPOTIFY_CLIENT_ID=your_spotify_client_id
   SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
   YTDLP_DEBUG=0
   ```

3. **Run:**
   ```bash
   docker compose up -d --build
   ```

### Command Quick Reference
* `!play <query/URL>` - Play audio or add to queue
* `!skip` - Skip current track
* `!pause` / `!resume` - Pause or resume playback
* `!queue` - Show current queue
* `!loop` / `!loop all` / `!loop off` - Change repeat modes
* `!shuffle` - Shuffle track queue
* `!stop` - Stop audio and clear queue
* `!leave` - Disconnect bot from voice channel
* `!help` - Show help message

---

<div align="center">
  <p>Tạo bởi <a href="https://discord.com/users/1147592525696204822"><b>Keyl</b></a> • Tham gia cộng đồng tại <a href="https://discord.gg/5XbvxEkCbG"><b>Discord Support Server</b></a> 🎧</p>
</div>

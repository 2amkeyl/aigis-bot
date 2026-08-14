# 🎀 Aigis Music Bot

Discord music bot viết bằng Python, phát nhạc trực tiếp từ **YouTube, SoundCloud và Spotify** ngay trong kênh thoại. Tính cách bot lấy cảm hứng từ Aigis (Persona 3 Reload) — toàn bộ phản hồi bằng tiếng Việt.

> ⚠️ Bot chỉ dùng lệnh **prefix `!`**, không dùng slash command (`/`).

---

## ✨ Tính năng

- 🎵 Phát nhạc từ **link YouTube / SoundCloud / Spotify**, hoặc tìm theo tên bài
- 📀 Hỗ trợ nạp cả **playlist / album** nhiều bài cùng lúc
- 🔁 3 chế độ lặp: tắt / lặp 1 bài / lặp cả hàng đợi
- 🔀 Trộn ngẫu nhiên hàng đợi
- 🎧 Ưu tiên luồng âm thanh Opus gốc — giữ chất lượng cao, ít tốn CPU khi phát
- 🛡️ Tự động reconnect khi luồng phát bị ngắt giữa chừng (hay gặp khi host trên IP datacenter)
- 🎶 Spotify: dùng [Spotify Web API](https://developer.spotify.com/) (Client Credentials) để lấy metadata rồi tìm bản phát tương ứng trên YouTube — vì Spotify không cho phát trực tiếp (DRM)
- 🧱 Đi kèm [`bgutil-ytdlp-pot-provider`](https://github.com/Brainicism/bgutil-ytdlp-pot-provider) để giảm tỉ lệ bị YouTube chặn khi chạy trên VPS/Cloud

---

## 📦 Yêu cầu

- [Docker](https://docs.docker.com/get-docker/) & Docker Compose
- 1 Discord Bot Token ([Discord Developer Portal](https://discord.com/developers/applications))
- (Tuỳ chọn) Spotify Client ID / Secret nếu muốn phát nhạc từ link Spotify ([Spotify for Developers](https://developer.spotify.com/dashboard))

---

## 🚀 Cài đặt

```bash
git clone https://github.com/<your-username>/aigis-bot.git
cd aigis-bot
```

Tạo file `.env` ở thư mục gốc:

```env
TOKEN=your_discord_bot_token
SPOTIFY_CLIENT_ID=your_spotify_client_id      # tuỳ chọn — bỏ trống nếu không cần Spotify
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
YTDLP_DEBUG=0                                  # đặt 1 để bật log chi tiết yt-dlp khi debug
```

> ❗ **Không commit file `.env` lên GitHub.** File `.gitignore` đã loại trừ sẵn, nhưng luôn kiểm tra lại trước khi push.

Build và chạy:

```bash
docker compose up -d --build
```

Xem log:

```bash
docker compose logs -f bot
```

---

## 🕹️ Danh sách lệnh

| Lệnh | Mô tả |
|---|---|
| `!play <link/tên>` | Phát nhạc từ YouTube, SoundCloud, Spotify hoặc tìm theo tên |
| `!skip` | Bỏ qua bài đang phát |
| `!pause` | Tạm dừng |
| `!resume` | Tiếp tục phát |
| `!loop` / `!loop all` / `!loop off` | Lặp 1 bài / lặp cả hàng đợi / tắt lặp |
| `!shuffle` | Trộn ngẫu nhiên hàng đợi |
| `!queue` | Xem danh sách hàng đợi |
| `!stop` | Dừng nhạc, xoá trắng hàng đợi |
| `!leave` | Bot rời kênh thoại |
| `!help` | Hiện danh sách lệnh |

---

## 🏗️ Kiến trúc

```
docker-compose.yml
├── bot            → container chạy main.py (discord.py + yt-dlp + ffmpeg)
└── pot-provider   → brainicism/bgutil-ytdlp-pot-provider, hỗ trợ vượt bot-check của YouTube
```

Hai container giao tiếp nội bộ qua `POT_PROVIDER_URL`, không cần mở port ra ngoài.

---

## ☁️ Triển khai lên VPS/Cloud (khuyên dùng)

Bot được thiết kế để chạy 24/7 trên một VM nhỏ (đã test ổn định trên **Google Cloud e2-micro — Always Free Tier**). Các điểm cần lưu ý khi tự host:

- YouTube hay chặn IP của các nhà cung cấp cloud lớn — nếu gặp lỗi `Sign in to confirm you're not a bot`, cân nhắc mount thêm file `cookies.txt` (export từ tài khoản Google phụ) vào container `bot`.
- VM RAM thấp (≤1GB) nên thêm swap file để tránh lỗi out-of-memory lúc `docker compose build`.

---

## 🛠️ Công nghệ sử dụng

- [discord.py](https://github.com/Rapptz/discord.py)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [spotipy](https://github.com/spotipy-dev/spotipy)
- [bgutil-ytdlp-pot-provider](https://github.com/Brainicism/bgutil-ytdlp-pot-provider)
- FFmpeg

---

## 📄 License

Dự án cá nhân, phục vụ mục đích học tập/sử dụng nội bộ. Vui lòng tôn trọng [Điều khoản dịch vụ của YouTube](https://www.youtube.com/t/terms) và [Spotify](https://www.spotify.com/legal/end-user-agreement/) khi sử dụng.

---

<p align="center">Made with 🎧 by Keyl</p>

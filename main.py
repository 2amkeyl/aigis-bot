import discord
from discord.ext import commands
import yt_dlp
import asyncio
import os
import re
import random
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import aiohttp
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# --- 1. CONFIGURATION ---
TOKEN = os.getenv('TOKEN')
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

# Khởi tạo Spotify Client
sp = None
if SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET:
    try:
        auth_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
        sp = spotipy.Spotify(auth_manager=auth_manager)
        print("✅ Đã kết nối thành công với Spotify API!")
    except Exception as e:
        print(f"❌ Lỗi khởi tạo Spotify API: {e}")

FFMPEG_OPTIONS = {
    'before_options': (
        '-reconnect 1 -reconnect_streamed 1 -reconnect_at_eof 1 '
        '-reconnect_on_network_error 1 -reconnect_delay_max 10'
    ),
    'options': '-vn -b:a 256k -ar 48000 -ac 2'
}

COLOR = discord.Color.gold()

POT_PROVIDER_URL = os.getenv('POT_PROVIDER_URL')
YTDLP_DEBUG = os.getenv('YTDLP_DEBUG', '').lower() in ('1', 'true', 'yes')

SPOTIFY_URL_RE = re.compile(r'open\.spotify\.com/(?:intl-\w+/)?(track|album|playlist)/([A-Za-z0-9]+)')

def get_ydl_options(fallback=False, flat=True):
    opts = {
        'format': 'best' if fallback else 'bestaudio[acodec=opus][protocol^=http]/bestaudio[protocol^=http]/bestaudio/best[protocol^=http]/best',
        'noplaylist': False,
        'extract_flat': 'in_playlist' if flat else False,
        'default_search': 'ytsearch',
        'geo_bypass': True,
        'quiet': not YTDLP_DEBUG,
        'no_warnings': not YTDLP_DEBUG,
        'verbose': YTDLP_DEBUG,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    }
    extractor_args = {}
    if not fallback:
        extractor_args['youtube'] = {'player_client': ['android', 'web']}
    if POT_PROVIDER_URL:
        extractor_args['youtubepot-bgutilhttp'] = {'base_url': [POT_PROVIDER_URL]}
    if extractor_args:
        opts['extractor_args'] = extractor_args
    return opts

async def extract_stream_info(url, flat=True):
    def _run(fallback):
        with yt_dlp.YoutubeDL(get_ydl_options(fallback=fallback, flat=flat)) as ydl:
            return ydl.extract_info(url, download=False)
    try:
        return await asyncio.to_thread(_run, False)
    except Exception as e:
        print(f"Lỗi trích xuất (lần 1): {e} -> thử lại với cấu hình dự phòng...")
        return await asyncio.to_thread(_run, True)

# --- 2. AIGIS DIALOGUES & SETUP ---
Aigis = {
    "noVoice": "❌ Bạn cần tham gia vào một Kênh Thoại trước khi gọi Aigis.",
    "busy": "❌ Aigis đang phục vụ ở một Kênh Thoại khác. Vui lòng tham gia cùng kênh hoặc chờ Aigis rời đi.",
    "noPerm": "❌ Chỉ thị bị từ chối: Yêu cầu quyền Quản Lý Server.",
    "playing": "🎶 Đang phát: **{}**", 
    "queued": "✅ Đã thêm vào hàng đợi: **{}**",   
    "searching": "🔎 Đang thu thập dữ liệu cho mục tiêu: **{}**",
    "notFound": "❌ Aigis không tìm thấy mục tiêu phù hợp với dữ liệu này.",
    "extractError": "❌ Đã xảy ra lỗi khi truy xuất dữ liệu từ nguồn phát.",
    "stopped": "⏹️ Đã ngừng mọi hoạt động âm thanh và xoá hàng đợi.",
    "paused": "⏸️ Trạng thái: Tạm dừng.",
    "resumed": "▶️ Trạng thái: Tiếp tục.",
    "skipped": "⏭️ Đã bỏ qua mục tiêu hiện tại.",
    "nothingPlaying": "❌ Hiện không có mục tiêu nào đang được phát.",
    "emptyQueue": "📭 Hàng đợi hiện đang trống.",
    "shuffled": "🔀 Đã trộn ngẫu nhiên hàng đợi.",
    "joined": "✅ Đã kết nối vào kênh thoại. Aigis sẽ ở lại 24/7.",
    "left": "👋 Đã ngắt kết nối khỏi kênh thoại.",
}

LOOP_LABELS = {0: "Tắt lặp", 1: "Lặp bài hiện tại", 2: "Lặp cả hàng đợi"}
guild_settings = {}
guild_queues = {}

def get_settings(guild_id):
    if guild_id not in guild_settings:
        guild_settings[guild_id] = {"prefix": "!", "announce": True}
    return guild_settings[guild_id]

def get_queue(guild_id):
    if guild_id not in guild_queues:
        guild_queues[guild_id] = {"songs": [], "loop": 0, "channel": None}
    return guild_queues[guild_id]

async def get_prefix(bot_instance, message):
    if not message.guild:
        return "!"
    return get_settings(message.guild.id)["prefix"]

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
bot = commands.Bot(command_prefix=get_prefix, intents=intents)
bot.help_command = None

class Song:
    def __init__(self, url, title, requester):
        self.url = url
        self.title = title
        self.requester = requester

def make_embed(description, title=None):
    embed = discord.Embed(description=description, color=COLOR)
    if title:
        embed.title = title
    return embed

async def send_to(channel_or_ctx, content=None, embed=None):
    if embed is None and content is not None:
        embed = make_embed(content)
    try:
        await channel_or_ctx.send(embed=embed)
    except Exception as e:
        print(f"Không thể gửi tin nhắn: {e}")

# --- 3. HỆ THỐNG BẮT LỖI TỔNG (GLOBAL ERROR HANDLER) ---
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        if ctx.command.name == 'play':
            await send_to(ctx, "❌ Thiếu thông tin rồi! Hãy nhập tên bài hát hoặc dán link nhé. (VD: `!play nhạc lofi`)")
        else:
            await send_to(ctx, f"❌ Thiếu thông tin bắt buộc cho lệnh `{ctx.command.name}`.")
    elif isinstance(error, commands.CommandNotFound):
        pass
    elif isinstance(error, commands.CheckFailure):
        pass
    else:
        print(f"Lỗi hệ thống không xác định: {error}")

def require_voice():
    async def predicate(ctx):
        if not ctx.author.voice:
            await send_to(ctx, Aigis["noVoice"])
            return False
        voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        if voice_client and voice_client.channel != ctx.author.voice.channel:
            await send_to(ctx, Aigis["busy"])
            return False
        return True
    return commands.check(predicate)

# --- 4. PHÁT NHẠC ---
async def play_next(guild: discord.Guild):
    queue = get_queue(guild.id)
    voice_client = discord.utils.get(bot.voice_clients, guild=guild)
    if not voice_client or not queue["songs"]: return

    song = queue["songs"].pop(0)
    if queue["loop"] == 2:
        queue["songs"].append(song)

    try:
        info = await extract_stream_info(song.url, flat=False)
        if 'entries' in info and len(info['entries']) > 0:
            info = info['entries'][0]
            
        stream_url = info['url']
        
        if song.url.startswith("ytsearch:"):
            song.title = info.get('title') or song.title
            
        source = await discord.FFmpegOpusAudio.from_probe(stream_url, **FFMPEG_OPTIONS)

        def after_playing(error):
            if error: print(f"Lỗi phát: {error}")
            if queue["loop"] == 1:
                queue["songs"].insert(0, song)
            asyncio.run_coroutine_threadsafe(play_next(guild), bot.loop)

        voice_client.play(source, after=after_playing)
        settings = get_settings(guild.id)
        if settings["announce"] and queue["channel"]:
            await send_to(queue["channel"], Aigis["playing"].format(song.title))

    except Exception as e:
        print(f"Lỗi phát nhạc ({song.title}): {e}")
        if queue["channel"]:
            await send_to(queue["channel"], f"⚠️ Bỏ qua **{song.title}** do lỗi lấy nguồn phát.")
        await play_next(guild)

@bot.event
async def on_ready():
    try:
        # Xoá mọi lệnh Slash đã đăng ký từ trước (bản cũ dùng hybrid_command) —
        # nếu không Discord vẫn hiện "/" cũ dù code giờ chỉ còn lệnh prefix "!".
        bot.tree.clear_commands(guild=None)
        await bot.tree.sync()
    except Exception as e:
        print(f"Không thể xoá lệnh Slash cũ: {e}")
    print(f'Aigis đã được đánh thức: {bot.user}')

# --- 5. GIẢI QUYẾT TRUY VẤN ---
async def _song_from_full_info(info, requester):
    url = info.get('webpage_url') or info.get('url')
    title = info.get('title') or "Không rõ tên bài"
    if not url:
        return None
    return Song(url, title, requester)

async def _enrich_missing_titles(songs, concurrency=4):
    """Một số nguồn (đặc biệt SoundCloud) không trả title ở chế độ liệt kê nhanh
    (extract_flat) cho MỌI track trong playlist — chỉ track nào thiếu mới cần
    resolve lại đầy đủ, tránh làm chậm toàn bộ playlist chỉ vì vài track lỗi."""
    sem = asyncio.Semaphore(concurrency)
    async def fix_one(song):
        async with sem:
            try:
                info = await extract_stream_info(song.url, flat=False)
                if 'entries' in info and info['entries']:
                    info = info['entries'][0]
                real_title = info.get('title')
                if real_title:
                    song.title = real_title
            except Exception:
                pass  # giữ nguyên "Không rõ tên bài" nếu vẫn không lấy được
    targets = [s for s in songs if s.title == "Không rõ tên bài"]
    if targets:
        await asyncio.gather(*(fix_one(s) for s in targets))

async def spotify_oembed_title(spotify_url: str):
    """Fallback KHÔNG cần API key/đăng nhập — dùng khi Client Credentials bị Spotify
    từ chối (401) do chính sách siết chặt từ 02/2026. Chỉ trả về ĐÚNG 1 title,
    không liệt kê được từng bài trong album/playlist."""
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(
                "https://open.spotify.com/oembed",
                params={"url": spotify_url},
                timeout=aiohttp.ClientTimeout(total=10),
            ) as resp:
                if resp.status != 200:
                    return None
                data = await resp.json()
                return data.get("title")
        except Exception:
            return None

async def resolve_query(query: str, requester: discord.Member):
    spotify_match = SPOTIFY_URL_RE.search(query)
    if spotify_match:
        kind, sp_id = spotify_match.groups()
        
        if not sp:
            return [], "❌ **LỖI API SPOTIFY:** Aigis không tìm thấy Client ID hoặc Secret. Hãy kiểm tra lại file `.env` và chắc chắn đã khởi động lại Docker bằng lệnh `--build`."

        songs = []
        try:
            if kind == 'playlist':
                results = await asyncio.to_thread(sp.playlist_items, sp_id, limit=50)
                for item in results.get('items', []):
                    track = item.get('track')
                    if track:
                        artists = " ".join([a.get('name') for a in track.get('artists', [])])
                        title = f"{track.get('name')} - {artists}"
                        songs.append(Song(f"ytsearch:{title}", title, requester))
                if not songs: return [], "❌ Playlist trống hoặc đang để chế độ Riêng tư (Private)."
                return songs, f"✅ Đã thêm thành công **{len(songs)}** bài hát vào hàng đợi."
            
            elif kind == 'album':
                results = await asyncio.to_thread(sp.album_tracks, sp_id, limit=50)
                for track in results.get('items', []):
                    artists = " ".join([a.get('name') for a in track.get('artists', [])])
                    title = f"{track.get('name')} - {artists}"
                    songs.append(Song(f"ytsearch:{title}", title, requester))
                return songs, f"✅ Đã thêm thành công **{len(songs)}** bài hát vào hàng đợi."
            
            elif kind == 'track':
                track = await asyncio.to_thread(sp.track, sp_id)
                artists = " ".join([a.get('name') for a in track.get('artists', [])])
                title = f"{track.get('name')} - {artists}"
                songs.append(Song(f"ytsearch:{title}", title, requester))
                return songs, None
        except spotipy.oauth2.SpotifyOauthError:
            return [], "❌ **SAI MÃ API:** Client ID hoặc Client Secret của Spotify bị sai. Chồng check lại file `.env` nhé!"
        except spotipy.exceptions.SpotifyException as e:
            if getattr(e, "http_status", None) == 401:
                # Từ 02/2026 Spotify bắt buộc đăng nhập tài khoản thật (Authorization
                # Code Flow) cho nhiều endpoint — Client ID/Secret đơn giản không còn
                # đủ quyền, đặc biệt với playlist. Fallback qua oEmbed công khai,
                # không cần đăng nhập, đổi lại chỉ lấy được 1 title đại diện.
                title = await spotify_oembed_title(query)
                if not title:
                    return [], "❌ Spotify hiện chặn truy cập kiểu này (chính sách API mới từ 02/2026) và không lấy được tên bài để tìm hộ."
                fallback_data = await extract_stream_info(f"ytsearch:{title}")
                fallback_entries = fallback_data.get('entries') if fallback_data else None
                if not fallback_entries:
                    return [], None
                fb_song = await _song_from_full_info(fallback_entries[0], requester)
                if not fb_song:
                    return [], None
                notice = None
                if kind in ("album", "playlist"):
                    loai = "album" if kind == "album" else "playlist"
                    notice = (
                        f"⚠️ Spotify hiện giới hạn API (từ 02/2026) nên Aigis chỉ đọc được "
                        f"TÊN {loai}, không tách được từng bài — tạm tìm và phát bản liên "
                        f"quan nhất trên YouTube: **{fb_song.title}**. Muốn phát đủ danh sách, "
                        f"dán từng link bài hát riêng lẻ nhé."
                    )
                return [fb_song], notice
            return [], f"❌ **LỖI SPOTIFY:** {e}"
        except Exception as e:
            return [], f"❌ **LỖI SPOTIFY:** {e}"

    if query.startswith("http"):
        info = await extract_stream_info(query)
        if info.get('_type') == 'playlist':
            entries = info.get('entries', [])
            if not entries:
                return [], None
            if len(entries) == 1:
                single_url = entries[0].get('url') or entries[0].get('webpage_url')
                info = await extract_stream_info(single_url, flat=False)
            else:
                songs = []
                for entry in entries:
                    vid_url = entry.get('url') or entry.get('webpage_url')
                    title = entry.get('title') or "Không rõ tên bài"
                    if not vid_url: continue
                    if not vid_url.startswith('http'):
                        # extract_flat của YouTube hay trả về ID trần (11 ký tự) thay vì
                        # URL đầy đủ. Chỉ tự dựng link youtube.com khi chắc chắn đúng định
                        # dạng ID YouTube — tránh trường hợp entry từ nguồn khác (SoundCloud...)
                        # bị ép nhầm thành link YouTube, chắc chắn lỗi khi tới lượt phát.
                        ie_key = (entry.get('ie_key') or entry.get('extractor_key') or '').lower()
                        looks_like_yt_id = bool(re.fullmatch(r'[\w-]{11}', vid_url))
                        if 'youtube' in ie_key or looks_like_yt_id:
                            vid_url = f"https://www.youtube.com/watch?v={vid_url}"
                        else:
                            continue
                    songs.append(Song(vid_url, title, requester))
                await _enrich_missing_titles(songs)
                return songs, f"✅ Đã thêm thành công **{len(songs)}** bài hát vào hàng đợi."
        song = await _song_from_full_info(info, requester)
        return ([song] if song else []), None

    data = await extract_stream_info(f"ytsearch:{query}")
    entries = data.get('entries') if data else None
    if not entries:
        return [], None
    song = await _song_from_full_info(entries[0], requester)
    return ([song] if song else []), None

# --- 6. COMMANDS ---
@bot.command(name="play", aliases=["p"])
@require_voice()
async def play(ctx: commands.Context, *, query: str = None):
    if not query:
        return await send_to(ctx, "❌ Thiếu thông tin rồi! Hãy nhập tên bài hát hoặc dán link nhé. (VD: `!play nhạc lofi`)")

    channel = ctx.author.voice.channel
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    if not voice_client:
        voice_client = await channel.connect()

    queue = get_queue(ctx.guild.id)
    queue["channel"] = ctx.channel

    try:
        songs, notice = await resolve_query(query, ctx.author)
    except Exception as e:
        print(f"Lỗi tìm kiếm: {e}")
        return await send_to(ctx, Aigis["extractError"])

    if not songs:
        if notice:
            return await send_to(ctx, notice)
        return await send_to(ctx, Aigis["notFound"])

    queue["songs"].extend(songs)
    msg = notice or Aigis["queued"].format(songs[0].title)

    await send_to(ctx, msg)

    if not voice_client.is_playing() and not voice_client.is_paused():
        await play_next(ctx.guild)

@bot.command(name="skip")
async def skip(ctx: commands.Context):
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if not voice_client or not (voice_client.is_playing() or voice_client.is_paused()): return await send_to(ctx, Aigis["nothingPlaying"])
    voice_client.stop()
    await send_to(ctx, Aigis["skipped"])

@bot.command(name="stop")
async def stop(ctx: commands.Context):
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    queue = get_queue(ctx.guild.id)
    queue["songs"].clear()
    queue["loop"] = 0
    if voice_client: voice_client.stop()
    await send_to(ctx, Aigis["stopped"])

@bot.command(name="pause")
async def pause(ctx: commands.Context):
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice_client and voice_client.is_playing():
        voice_client.pause()
        await send_to(ctx, Aigis["paused"])

@bot.command(name="resume")
async def resume(ctx: commands.Context):
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice_client and voice_client.is_paused():
        voice_client.resume()
        await send_to(ctx, Aigis["resumed"])

@bot.command(name="queue", aliases=["q"])
async def queue_cmd(ctx: commands.Context):
    queue = get_queue(ctx.guild.id)
    if not queue["songs"]: return await send_to(ctx, Aigis["emptyQueue"])
    lines = [f"`{i}.` {s.title}" for i, s in enumerate(queue["songs"][:10], 1)]
    desc = "\n".join(lines) + f"\n\n*Tổng: {len(queue['songs'])}* | *Lặp: {LOOP_LABELS[queue['loop']]}*"
    await send_to(ctx, embed=make_embed(desc, "📋 Hàng Đợi"))

@bot.command(name="shuffle")
async def shuffle(ctx: commands.Context):
    queue = get_queue(ctx.guild.id)
    if queue["songs"]:
        random.shuffle(queue["songs"])
        await send_to(ctx, Aigis["shuffled"])

@bot.command(name="loop")
async def loop_cmd(ctx: commands.Context, mode: str = None):
    queue = get_queue(ctx.guild.id)
    if mode is None:
        queue["loop"] = 1
    elif mode.lower() == "all":
        queue["loop"] = 2
    elif mode.lower() == "off":
        queue["loop"] = 0
    else:
        return await send_to(ctx, "❌ Cú pháp không hợp lệ. Dùng: `!loop` | `!loop all` | `!loop off`")
    await send_to(ctx, f"🔁 Chế độ lặp: **{LOOP_LABELS[queue['loop']]}**")

@bot.command(name="leave")
async def leave(ctx: commands.Context):
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice_client:
        get_queue(ctx.guild.id)["songs"].clear()
        await voice_client.disconnect()
        await send_to(ctx, Aigis["left"])

@bot.command(name="help")
async def help_command(ctx: commands.Context):
    embed = discord.Embed(
        title="Aigis Music Bot by Keyl",
        description="Sử dụng tiền tố `!` để gọi lệnh.",
        color=COLOR,
    )
    embed.add_field(name="▶️ `!play <link/tên>` (viết tắt: `!p`)", value="Phát nhạc từ YouTube, SoundCloud, Spotify.", inline=False)
    embed.add_field(name="⏭️ `!skip`", value="Bỏ qua bài hát đang phát hiện tại.", inline=False)
    embed.add_field(name="⏸️ `!pause`", value="Tạm dừng phát nhạc.", inline=False)
    embed.add_field(name="▶️ `!resume`", value="Tiếp tục phát nhạc.", inline=False)
    embed.add_field(name="🔄 `!loop` | `!loop all` | `!loop off`", value="Lặp 1 bài, lặp toàn bộ hàng đợi hoặc tắt lặp.", inline=False)
    embed.add_field(name="🔀 `!shuffle`", value="Trộn ngẫu nhiên các bài trong hàng đợi.", inline=False)
    embed.add_field(name="📋 `!queue` (viết tắt: `!q`)", value="Xem danh sách các bài hát đang nằm trong hàng đợi.", inline=False)
    embed.add_field(name="⏹️ `!stop`", value="Dừng nhạc, xoá trắng hàng đợi.", inline=False)
    embed.add_field(name="👋 `!leave`", value="Yêu cầu Bot rời khỏi kênh thoại.", inline=False)
    await ctx.send(embed=embed)

# --- DUMMY WEB SERVER ---
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Aigis is running!")
    def log_message(self, format, *args): pass

def run_web_server():
    server = HTTPServer(('0.0.0.0', int(os.environ.get("PORT", 10000))), SimpleHandler)
    server.serve_forever()

if __name__ == "__main__":
    threading.Thread(target=run_web_server, daemon=True).start()
    bot.run(TOKEN)
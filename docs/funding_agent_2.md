# Funding Agent 2

**Built by Moon Dev**

## What It Does

Scans ALL HyperLiquid symbols for funding rate anomalies and announces the top findings via AI-generated voice.

## Key Features

- **Full Symbol Scan** - Fetches funding rates for ALL HyperLiquid symbols
- **Anomaly Detection** - Identifies top 3 positive and top 3 negative funding rates
- **Voice Announcements** - Uses OpenAI TTS to announce findings
- **Fancy Display** - Unicode table output in terminal
- **CSV Export** - Saves funding rate data with timestamps

## How It Works

1. Fetches all HyperLiquid symbols via API
2. Calculates hourly and annualized funding rates
3. Identifies extremes (top/bottom 3)
4. Generates speech-friendly announcement
5. Uses OpenAI TTS to create audio
6. Plays announcement and saves to file
7. Repeats every 15 minutes

## Requirements

```bash
pip install requests pandas playsound
```

**API Keys** - Add to `.env`:
```
OPENAI_KEY=your_openai_key_here
```

## Usage

```bash
python src/agents/funding_agent_2.py
```

The agent runs continuously, scanning every 15 minutes.

## Configuration

Edit `src/agents/funding_agent_2.py` top section:

```python
# Scan interval in minutes
SCAN_INTERVAL = 15

# Voice settings
VOICE = "fable"  # OpenAI TTS voice
SPEECH_SPEED = 1.0  # Playback speed
```

## Output

### Terminal Display
```
╔════════════════════════════════════════════════╗
║           FUNDING RATE ANOMALIES               ║
╠════════════════════════════════════════════════╣
║  Symbol  │  Hourly Rate  │  Annualized Rate   ║
╠══════════╪═══════════════╪════════════════════╣
║  BTC     │    0.0012%    │      10.51%        ║
║  ETH     │    0.0008%    │       7.01%        ║
║  SOL     │   -0.0015%    │     -13.14%        ║
╚════════════════════════════════════════════════╝
```

### Data Files
- Location: `src/data/funding_agent_2/`
- Format: `funding_rates_{timestamp}.csv`
- Columns: `symbol`, `hourly_rate`, `annualized_rate`, `timestamp`

### Audio Files
- Location: `src/audio/`
- Format: `funding_anomalies_{timestamp}.mp3`

## Example Announcement

"Funding rate alert! Top positive rates: Bitcoin at 10 percent annualized, Ethereum at 7 percent. Top negative rates: Solana at negative 13 percent. Consider these opportunities carefully."

## Differences from Funding Agent 1

| Feature | Funding Agent 1 | Funding Agent 2 |
|---------|-----------------|-----------------|
| Symbol Coverage | Monitored tokens only | ALL HyperLiquid symbols |
| Voice Announcements | No | Yes (OpenAI TTS) |
| Annualized Rates | No | Yes |
| Table Display | Basic | Unicode fancy table |
| Auto-scan | Manual | Every 15 minutes |

## Technical Notes

- **HyperLiquid API** - No API key required for public data
- **OpenAI TTS** - Requires valid API key with TTS access
- **Base Agent** - Inherits from `BaseAgent` class
- **Audio Playback** - Uses `playsound` library

## API Endpoint

```
POST https://api.hyperliquid.xyz/info
{
    "type": "allMids"  // Gets all symbol data
}
```

---

**Moon Dev's Funding Agent 2** - Scan all symbols, hear the opportunities

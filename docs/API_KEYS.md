# API Keys Setup Guide

## Required API Keys

### 1. Anthropic API Key (Claude AI)
**Get your key:**
1. Visit [https://console.anthropic.com](https://console.anthropic.com)
2. Sign up and go to "API Keys"
3. Create a new key (starts with `sk-ant-...`)

**Cost:** Pay-as-you-go (~$3 per million tokens)

---

### 2. Finnhub API Key (Stock News)
**Get your key:**
1. Visit [https://finnhub.io/register](https://finnhub.io/register)
2. Sign up and verify email
3. Copy your API key from the dashboard

**Free tier:** 60 API calls/minute (sufficient for development)

---

## Configuration

1. **Create .env file:**
```bash
cp .env.example .env
```

2. **Add your keys to `.env`:**
```bash
ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
FINNHUB_API_KEY=your-actual-key-here
```

3. **Test it works:**
```bash
./run_tests.sh news
```

---

## Security Notes

- Never commit `.env` to git (already in `.gitignore`)
- Don't share your API keys
- Rotate keys if exposed

---

## Troubleshooting

**"FINNHUB_API_KEY is required"**
- Make sure you created `.env` (not just `.env.example`)
- Check no spaces or quotes around the key

**"Rate limit exceeded"**
- Free tier: 60 calls/minute
- Wait one minute and retry

# Gamma Deck Generator

Automate professional presentation creation using Claude AI + Gamma API. Transform storylines into McKinsey-style decks in under 60 seconds.

## 🎯 What This Does

Combines [Claude Skills](../README.md) with Gamma's AI design platform to create presentation workflows:

**Input:** Structured storyline (from storyline-builder skill)  
**Output:** Professional PPTX presentation with AI-generated visuals

**Time savings:** 3-5 hours → < 1 minute

## 🚀 Quick Start

### Prerequisites

1. **Gamma Pro Account** (for API access)
   - Sign up at [gamma.app](https://gamma.app)
   - Get API key: Settings > API > Create API Key
   - Format: `sk-gamma-xxxxxxxxxx`

2. **Python 3.7+** installed

3. **Claude Skills** (optional but recommended)
   - Install [storyline-builder](../storyline-builder/), [issue-tree-builder](../issue-tree-builder/), [scpr-framework](../scpr-framework/)

### Installation

```bash
# 1. Clone this repo
git clone https://github.com/sruthir28/claude-skills.git
cd claude-skills/gamma-automation

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set your Gamma API key (Option A: Environment variable)
export GAMMA_API_KEY="sk-gamma-xxxxxxxxxx"

# OR Option B: Edit the script directly
# Open gamma_deck_generator.py and replace YOUR_API_KEY_HERE with your key
```

## 📖 Usage

### Basic Usage

```bash
python gamma_deck_generator.py --input-file storyline.txt
```

This creates `storyline.pptx` in your current directory.

### Advanced Options

```bash
python gamma_deck_generator.py \
  --input-file my_storyline.txt \
  --theme Chisel \
  --output pitch_deck.pptx \
  --tone "professional, strategic" \
  --audience "executives, investors" \
  --image-style "minimalist, charts and graphs, clean"
```

### All Available Options

| Option | Description | Default |
|--------|-------------|---------|
| `--input-file` | Path to storyline file (required) | - |
| `--output` | Output filename | `<input-file>.pptx` |
| `--theme` | Gamma theme (Chisel, Oasis, etc.) | Auto |
| `--slides` | Number of slides | Auto |
| `--tone` | Presentation tone | professional |
| `--audience` | Target audience | executives |
| `--text-mode` | preserve/generate/condense | preserve |
| `--image-style` | AI image style description | professional, clean, business |

## 🎨 Available Themes

Popular McKinsey-style themes:
- **Chisel** - Clean, professional (recommended)
- **Oasis** - Modern, vibrant
- **Sapphire** - Corporate blue
- **Ember** - Warm tones
- **Forest** - Natural greens

Get full list: Visit [gamma.app/themes](https://gamma.app/themes) or use GET `/v1.0/themes` API

## 📝 Complete Workflow

### Method 1: Using Claude Code (Recommended)

1. **Open Claude Code in your terminal:**
   ```bash
   claude code
   ```

2. **Ask Claude to create a storyline:**
   ```
   Create a McKinsey-style storyline for [topic] following the storyline-builder 
   framework and save it as storyline.txt
   ```

3. **Run the generator:**
   ```bash
   python gamma_deck_generator.py --input-file storyline.txt
   ```

4. **Open your presentation:**
   - Local file: `storyline.pptx`
   - Online editor: Gamma URL (printed in output)

### Method 2: Using Claude.ai Web Interface

1. **Create storyline in Claude:**
   - Use storyline-builder skill
   - Copy output to a text file (e.g., `storyline.txt`)

2. **Run generator locally:**
   ```bash
   python gamma_deck_generator.py --input-file storyline.txt
   ```

### Method 3: Manual Storyline Creation

1. **Write your storyline** (see [examples/](examples/))
   - Use `---` to separate slides
   - Write action-oriented titles
   - Include specific data points

2. **Generate presentation:**
   ```bash
   python gamma_deck_generator.py --input-file your_storyline.txt
   ```

## 📚 Example Storylines

See [examples/sample_storyline.txt](examples/sample_storyline.txt) for a complete example.

**Storyline structure:**
```
Presentation Title

Market represents $XXB opportunity growing at XX% CAGR
---
We operate in [segment] worth $XXB with XX% growth
---
Top 3 competitors generate $XXM revenue growing XX% annually
---
Our product addresses [use case] for [customer segment]
---
Three growth opportunities identified: [opp 1], [opp 2], [opp 3]
---
18-month roadmap prioritizes [capability 1], [capability 2], [capability 3]
```

## 🔧 Troubleshooting

**"Error: Please set GAMMA_API_KEY"**
- Set environment variable: `export GAMMA_API_KEY="sk-gamma-xxx"`
- Or edit script and replace `YOUR_API_KEY_HERE`

**"File not found"**
- Check file path is correct
- Use full path if needed: `--input-file /full/path/to/file.txt`

**"Generation failed"**
- Check API key is valid
- Verify Gamma account has credits
- Check input file isn't empty

**"No exportUrl found"**
- PPTX export may take extra time
- You can still access deck via Gamma URL
- Try again in a few minutes

## 💡 Tips for Best Results

**Storyline Best Practices:**
- Use action-oriented slide titles
- Include specific data points (not "good growth", say "40% CAGR")
- Follow logical flow: Problem → Analysis → Solution
- Typical deck: 12-18 slides

**Image Style Recommendations:**
- McKinsey-style: "minimalist, charts and graphs, clean lines"
- Modern tech: "gradient, vibrant colors, geometric shapes"
- Corporate: "professional, conservative, business imagery"
- Startup: "bold, modern, dynamic visuals"

**Text Mode Guide:**
- `preserve` - Keep exact text (best for storylines)
- `generate` - Expand brief outlines into full content
- `condense` - Summarize long documents

## 🤝 Integration with Claude Skills

This tool works seamlessly with:

1. **[storyline-builder](../storyline-builder/)** - Create McKinsey-style storylines
2. **[issue-tree-builder](../issue-tree-builder/)** - Structure problem analysis
3. **[scpr-framework](../scpr-framework/)** - Build executive communications

**Example workflow:**
```
Claude (storyline-builder) → storyline.txt → gamma_deck_generator.py → presentation.pptx
```

## 📊 Output

You'll receive:
1. **Local PPTX file** - Download and edit in PowerPoint/Keynote
2. **Gamma URL** - Edit online in Gamma's web editor
3. **Credit usage** - Track remaining API credits

## 🔐 Security Note

- Never commit API keys to GitHub
- Use environment variables for keys
- Add `.env` to `.gitignore`

## 📄 License

MIT License - see main repo

## 🙋 Support

- Gamma API docs: [developers.gamma.app](https://developers.gamma.app)
- Claude Skills: See main [README](../README.md)
- Issues: Open a GitHub issue

## 🌟 Star This Repo

If this saves you time, give it a ⭐ on GitHub!

---

**Built by:** Sruthi  
**For:** Ex-consultants who want to build decks faster

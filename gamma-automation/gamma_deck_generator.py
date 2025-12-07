#!/usr/bin/env python3
"""
Create presentation using Gamma API from input file or text
Usage:
  python gamma_deck_generator.py --input-file storyline.txt
  python gamma_deck_generator.py --input-file storyline.txt --theme Chisel --output my_deck.pptx
"""

import requests
import time
import json
import argparse
import sys
from pathlib import Path

# Your API key - get from environment variable or replace with your key
import os
API_KEY = os.getenv("GAMMA_API_KEY", "YOUR_API_KEY_HERE")
BASE_URL = "https://public-api.gamma.app/v1.0"

if API_KEY == "YOUR_API_KEY_HERE":
    print("❌ Error: Please set GAMMA_API_KEY environment variable or edit the script with your API key")
    print("   Get your API key from: https://gamma.app/settings (Settings > API)")
    sys.exit(1)

# Parse command line arguments
parser = argparse.ArgumentParser(description='Generate Gamma presentation from file')
parser.add_argument('--input-file', required=True, help='Path to file containing storyline/content')
parser.add_argument('--theme', default=None, help='Gamma theme (optional)')
parser.add_argument('--slides', type=int, help='Number of slides (auto if not specified)')
parser.add_argument('--output', default=None, help='Output PPTX filename (default: derived from input filename)')
parser.add_argument('--tone', default='professional', help='Tone (default: professional)')
parser.add_argument('--audience', default='executives', help='Target audience (default: executives)')
parser.add_argument('--text-mode', default='preserve', choices=['preserve', 'generate', 'condense'], 
                    help='How to process text (default: preserve)')
parser.add_argument('--image-style', default='professional, clean, business', 
                    help='Image style description (default: professional, clean, business)')

args = parser.parse_args()

# Derive output filename from input filename if not specified
if args.output is None:
    input_path = Path(args.input_file)
    args.output = input_path.stem + '.pptx'

# Read input file
try:
    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"❌ Error: File '{args.input_file}' not found")
        sys.exit(1)
    
    with open(input_path, 'r', encoding='utf-8') as f:
        input_text = f.read().strip()
    
    if not input_text:
        print(f"❌ Error: File '{args.input_file}' is empty")
        sys.exit(1)
        
except Exception as e:
    print(f"❌ Error reading file: {e}")
    sys.exit(1)

# Build payload
payload = {
    "inputText": input_text,
    "textMode": args.text_mode,
    "format": "presentation",
    "exportAs": "pptx",
    "textOptions": {
        "amount": "medium",
        "tone": args.tone,
        "audience": args.audience,
        "language": "en"
    },
    "imageOptions": {
        "source": "aiGenerated",
        "model": "flux-1-pro",
        "style": args.image_style
    }
}

# Add themeId if specified
if args.theme:
    payload["themeId"] = args.theme

# Add numCards if specified
if args.slides:
    payload["numCards"] = args.slides

print("🚀 Creating your presentation...")
print(f"📝 Input file: {args.input_file}")
print(f"📄 Content: {len(input_text)} characters")
if args.theme:
    print(f"🎨 Theme: {args.theme}")
else:
    print(f"🎨 Theme: default")
print(f"🎭 Text mode: {args.text_mode}")
print(f"🖼️  Image style: {args.image_style}")
if args.slides:
    print(f"📊 Slides: {args.slides}")
else:
    print(f"📊 Slides: auto")
print()

# Step 1: Create the presentation
try:
    response = requests.post(
        f"{BASE_URL}/generations",
        headers={
            "Content-Type": "application/json",
            "X-API-KEY": API_KEY
        },
        json=payload
    )
    
    response.raise_for_status()
    result = response.json()
    generation_id = result["generationId"]
    
    print(f"✅ Generation started! ID: {generation_id}")
    print()
    
except requests.exceptions.RequestException as e:
    print(f"❌ Error creating presentation: {e}")
    if hasattr(e, 'response') and hasattr(e.response, 'text'):
        print(f"Response: {e.response.text}")
    sys.exit(1)

# Step 2: Poll for completion
print("⏳ Waiting for Gamma to generate your deck...")
poll_count = 0
max_polls = 60  # 5 minutes max

while poll_count < max_polls:
    try:
        status_response = requests.get(
            f"{BASE_URL}/generations/{generation_id}",
            headers={"X-API-KEY": API_KEY}
        )
        status_response.raise_for_status()
        status = status_response.json()
        
        if status["status"] == "completed":
            print()
            print("=" * 60)
            print("🎉 SUCCESS! Your presentation is ready!")
            print("=" * 60)
            print(f"📊 Gamma URL: {status['gammaUrl']}")
            print(f"💳 Credits used: {status['credits']['deducted']}")
            print(f"💰 Credits remaining: {status['credits']['remaining']}")
            print()

            # Check if exportUrl is available
            if "exportUrl" in status:
                pptx_url = status["exportUrl"]
                print(f"📥 PPTX URL found: {pptx_url}")

                try:
                    # Download the PPTX
                    print("⬇️  Downloading PPTX...")
                    pptx_response = requests.get(pptx_url)
                    pptx_response.raise_for_status()

                    # Save locally with specified filename
                    with open(args.output, 'wb') as f:
                        f.write(pptx_response.content)

                    print(f"✅ PPTX saved locally as: {args.output}")
                    print()
                    print("=" * 60)
                    print("📄 Files:")
                    print(f"  • Gamma URL: {status['gammaUrl']}")
                    print(f"  • Local PPTX: {args.output}")
                    print("=" * 60)

                except requests.exceptions.RequestException as e:
                    print(f"❌ Error downloading PPTX: {e}")
                    if hasattr(e, 'response') and hasattr(e.response, 'text'):
                        print(f"Response: {e.response.text}")
            else:
                print("⚠️  No exportUrl found in response")
                print("The PPTX may not have been generated yet.")
                print("You can still access your deck at the Gamma URL above.")

            break
            
        elif status["status"] == "failed":
            print()
            print("❌ Generation failed!")
            print(f"Response: {json.dumps(status, indent=2)}")
            break
            
        else:  # pending
            poll_count += 1
            print(f"⏳ Still generating... ({poll_count * 5}s elapsed)", end='\r')
            time.sleep(5)
            
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Error checking status: {e}")
        break

if poll_count >= max_polls:
    print("\n⏱️  Timeout: Generation took too long. Check Gamma dashboard.")
    print(f"Generation ID: {generation_id}")
    sys.exit(1)

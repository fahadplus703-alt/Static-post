# Ajaira Gyan — daily static posts playbook

Fully automatic: no approval. Every day = 3 static posts + 1 carousel on the
Ajaira Gyan Facebook page + Instagram @ajaira.gyan, scheduled through Metricool
(brand "ajaira.gyan", blogId 7743513, timezone Asia/Dhaka, FB type POST, IG type POST,
isAiGenerated false, no AI label).

## Hard rule: never the video topics
Videos already cover motivation, জানেন কি? facts, and কাজের কথা tips
(relationship / mind / money). Static posts must NOT use those topics.

## Slots and pillars (Dhaka time; videos are 9:00, 17:00, 19:00; carousel moved to 18:00 on 31 Oct 2026)
| Time  | Template | Kicker (English, caps) | Pillar (rotate inside the slot) |
|-------|----------|------------------------|----------------------------------|
| 11:00 | engage   | DAILY RIDDLE / THIS OR THAT / FILL THE BLANK | আজকের ধাঁধা · এটা নাকি ওটা? · শূন্যস্থান পূরণ · ইমোজি দেখে প্রবাদ চিনুন · ছোট অংক-পাজল |
| 13:30 | fact     | WORD STORIES / PROVERB STORIES | শব্দের গল্প (Bangla word origins) · প্রবাদের পেছনের গল্প |
| 15:30 | tip      | MYTH CHECK | মিথ নাকি সত্যি? (everyday science / health / tech myths) |
| 18:00 | carousel | e.g. THE 90s EDITION / PHONE HACKS / HIDDEN BANGLADESH / FOOD STORIES | নস্টালজিয়া · ফোনের লুকানো ট্রিক · বাংলাদেশের অচেনা ঘোরার জায়গা · দেশি খাবারের আসল গল্প |

Rotate so the same sub-pillar doesn't repeat two days running. Riddle answers are revealed
in the next day's riddle caption ("গতকালের উত্তর: …").

## Brand v2 — modern editorial (Fahad, 31 Oct 2026, "modern like Masala Chowk")
- Palette stays Cha-stall: yellow #FFC531, ink #141414, paper #FAF6EC. Dark ink with a warm
  glow for engage/tip/carousel, paper for the fact post.
- Type: headline Noto Serif Bengali ExtraBold; the 1–3 accent words wrapped in `<em>` render
  in Tiro Bangla italic yellow (never `<mark>`). Body Hind Siliguri. Small English kicker in
  DM Sans letter-spaced caps. Use `<br>` to control headline line breaks.
- **Every post has a photo** (Fahad: photos make it look niche). Layout is fixed in render.py.

## Photos (generated, never downloaded from random sites)
- Generate with Magnific `images_generate`: mode `flux-2-klein`, aspectRatio `4:5`,
  resolution `1k`, count 1 (10 credits each, ~90/day). If Magnific is out of credits or
  fails, use Higgsfield `generate_image` at the cheapest model.
- Prompt style: concrete Bangladeshi scene/object for the topic + "nostalgic 35mm film photo,
  grain, no text, no logos" (or "clean editorial photo" for non-nostalgia). People only from
  behind or as generic crowds/children; never real public figures, brand logos, or known
  cartoon/TV characters (show the TV/object, not the character).
- Save with curl: `photos/<date>_<id>/00.jpg` for single posts and the carousel cover;
  `01.jpg`–`05.jpg` for carousel slides. Look at each one; if it has garbled text, wrong
  culture or anything odd, set a crop (third field of the slide, CSS object-position, e.g.
  "center 85%") or regenerate once.

## Copy rules
- Bangla, আপনি form, warm and witty (the page name is আজাইরা জ্ঞান — light, not preachy).
- Headline hooks with curiosity. Keep headlines short: single posts max ~8 words;
  carousel slide headline 2–4 words; carousel sub max 1 line ~60 chars.
- Every post ends with a comment trigger (question, number to comment, tag a friend) and
  the caption asks to save/share. Hashtags: #আজাইরাজ্ঞান #AjairaGyan + 2–3 topic tags.
- Facts must be verified with a web search before use (etymology, myths, places, dates).
  If a claim can't be confirmed, drop it.
- No copyrighted images, characters, logos or song lyrics.
- Never repeat a topic already listed in `log.md`.

## JSON shape (see posts/2026-10-31.json carousel and render.py)
single: {id, time, template: engage|fact|tip, kicker, tag, headline, body, foot, caption}
carousel: {id, time, template: carousel, kicker, tag, cover, cover_sub,
           slides: [[headline, sub, optional object-position] x5], cta, cta_sub, caption}

## Daily run
1. Read `log.md`, pick the next sub-pillar for each slot, research + verify.
2. Write `posts/YYYY-MM-DD.json`. Generate + download photos into `photos/`.
3. `npm i` then `python3 render.py posts/YYYY-MM-DD.json posts` → PNG per slide; convert to
   JPG (quality 85) and delete PNGs. Look at every image and fix overflow before pushing.
4. Commit + push to main. Image URLs:
   `https://raw.githubusercontent.com/fahadplus703-alt/static-post/main/posts/<date>_<id>/<nn>.jpg`
5. Schedule each post in Metricool (FB + IG; carousel = all slide URLs in order).
6. Append the day's topics + Metricool status to `log.md`; commit + push.

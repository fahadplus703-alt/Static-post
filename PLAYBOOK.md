# Ajaira Gyan — daily static posts playbook

Fully automatic: no approval. Every day = 3 static posts + 1 carousel on the
Ajaira Gyan Facebook page + Instagram @ajaira.gyan, scheduled through Metricool
(brand "ajaira.gyan", blogId 7743513, timezone Asia/Dhaka, FB type POST, IG type POST,
isAiGenerated false, no AI label).

## Hard rule: never the video topics
Videos already cover motivation, জানেন কি? facts, and কাজের কথা tips
(relationship / mind / money). Static posts must NOT use those topics.

## Slots and pillars (Dhaka time; videos are 9:00, 17:00, 19:00)
| Time  | Template | Pillar (rotate inside the slot) |
|-------|----------|----------------------------------|
| 11:00 | engage   | আজকের ধাঁধা (riddle) · এটা নাকি ওটা? (this-or-that) · শূন্যস্থান পূরণ · ইমোজি দেখে প্রবাদ চিনুন · ছোট অংক-পাজল |
| 13:30 | fact     | শব্দের গল্প (Bangla word origins) · প্রবাদের পেছনের গল্প |
| 15:30 | tip      | মিথ নাকি সত্যি? (everyday science / health / tech myths) |
| 21:30 | carousel | নস্টালজিয়া (90s/2000s BD childhood) · ফোনের লুকানো ট্রিক · বাংলাদেশের অচেনা ঘোরার জায়গা · দেশি খাবারের আসল গল্প |

Rotate so the same sub-pillar doesn't repeat two days running. Riddle answers are revealed
in the next day's riddle caption ("গতকালের উত্তর: …").

## Copy rules
- Bangla, আপনি form, warm and witty (the page name is আজাইরা জ্ঞান — light, not preachy).
- Headline hooks with curiosity; one `<mark>` highlight of 1–3 words (kept on one line).
- Every post ends with a comment trigger (question, number to comment, tag a friend) and
  the caption asks to save/share. Hashtags: #আজাইরাজ্ঞান #AjairaGyan + 2–3 topic tags.
- Facts must be verified with a web search before use (etymology, myths, places, dates).
  If a claim can't be confirmed, drop it.
- No copyrighted images, characters, logos or song lyrics; text-only designs.
- Never repeat a topic already listed in `log.md`.

## Daily run
1. Read `log.md`, pick the next sub-pillar for each slot, research + verify.
2. Write `posts/YYYY-MM-DD.json` (same shape as earlier days).
3. `npm i` then `python3 render.py posts/YYYY-MM-DD.json posts` → PNG per slide; convert to
   JPG (quality 85) and delete PNGs.
4. Commit + push to main. Image URLs:
   `https://raw.githubusercontent.com/<owner>/ajaira-gyan-posts/main/posts/<date>_<id>/<nn>.jpg`
5. Schedule each post in Metricool (FB + IG; carousel = all slide URLs in order).
6. Append the day's topics + Metricool status to `log.md`; commit + push.

# ארץ האותיות (Eretz Ha'otiyot)

A Hebrew reading and counting game for two young kids, built as one HTML file.
It runs in any browser, works well on a tablet, and needs no install or server.

## Players

**גַּן (preschool, about age 4)**
- **אֵיפֹה הָאוֹת?** The game names a letter out loud and the child taps it.
  From level 3 the wrong choices are letters that look alike (ב/כ/פ, ד/ר, ה/ח/ת…).
- **כַּמָּה יֵשׁ?** Counting objects from 1 to 5, then up to 10. Tapping an object counts it out loud.
- **אוֹת רִאשׁוֹנָה** A picture and its spoken word. The child picks the letter the word starts with.

**כִּתָּה א׳ (first grade, just learning to read)**
- **הַצְּלִיל הָרִאשׁוֹן** Picks the first syllable with its nikud (בָּ / בִּ / מָ…).
- **קוֹרְאִים וּבוֹחֲרִים** Reads a pointed word and picks the matching picture.
- **מָה בַּתְּמוּנָה?** Looks at a picture and picks the right word. On harder levels all the choices start with the same letter, so the child has to read the whole word.
- **בּוֹנִים מִלָּה** Builds the word from syllable tiles. After two wrong taps the right tile starts to glow.

Each round has 8 questions. Every correct answer earns a star, and every 5 stars unlocks a sticker in the child's album.

## Math

**גַּן**
- **אֵיפֹה יוֹתֵר?** Two groups of objects: tap the one with more. The gap between the groups shrinks as levels go up, and level 5 sometimes asks for fewer.
- **חִבּוּר בִּתְמוּנוֹת** Picture addition (🍎🍎 + 🍎 = ?), sums up to 3, 5, 7, then 10. Level 5 is take-away: some objects are crossed out and the child counts what is left. Objects can be tapped to count them out loud.

**כִּתָּה א׳**
- **תַּרְגִּילִים** Level 1: addition up to 5 with dots under the numbers. 2: addition up to 10. 3: subtraction up to 10. 4: addition and subtraction up to 20. 5: missing number (8 + ? = 10).
- **מָה חָסֵר?** A row of five numbers with one missing. Level 1 counts up to 10, 2 up to 20, 3 counts down, 4 goes by 2s, 5 goes by 10s up to 100.

Equations are written left to right, the way Israeli math books write them.

## Levels

Each game has 5 levels, and the level adjusts while the child plays:
3 correct first-try answers in a row move up a level (with a "⬆️ שָׁלָב!" banner),
and 2 answers in a row that needed retries move down one level quietly.

| Level | בּוֹנִים מִלָּה (build a word) | Reading games (words shown) |
|---|---|---|
| 1 | 3-letter words | 2–3 letters |
| 2 | 4-letter words | 3–4 letters |
| 3 | 5-letter words | 4–5 letters |
| 4 | 5–6 letters + 1 extra tile that doesn't belong | 5–6 letters, 4 choices |
| 5 | 6+ letters + 2 extra tiles | 6+ letters, 4 choices |

In מָה בַּתְּמוּנָה? all choices start with the same letter from level 2.

**Kindergarten (גַּן) levels**

| Level | אֵיפֹה הָאוֹת? | כַּמָּה יֵשׁ? | אוֹת רִאשׁוֹנָה |
|---|---|---|---|
| 1 | 2 letters, the letter is shown to match | count 1–3, 2 choices | 2 letters, short words |
| 2 | 3 letters, still shown | count 1–5 | 3 letters |
| 3 | 3 letters, heard only | count 2–7 | 3 letters, longer words |
| 4 | 4 letters incl. look-alikes (ב/כ/פ, ד/ר) | count 3–10, 4 choices | 4 letters, any word |
| 5 | 6 letters incl. look-alikes | two kinds of things mixed, count only one | 4 letters incl. look-alikes |
The current level shows above the question and on each game card in the menu.
Progress is saved in the browser (localStorage), separately for each child.

## Voice

The game uses the device's own Hebrew text-to-speech (`he-IL`).

It can also play pre-recorded clips instead, if `voice/voice.js` exists. That file is
not included right now: the Microsoft and Google voices tried so far (samples in
`voice/samples/`) did not pronounce the phrases well enough. Any phrase without a
clip falls back to the device voice.

- `voice/phrases.txt` lists every phrase the game says (about 250).
- `tools/make_voice.py` records them with Microsoft's neural voices (free, no account) and writes `voice/voice.js`:

  ```
  pip install edge-tts
  python tools/make_voice.py                           # Hila (female)
  python tools/make_voice.py --voice he-IL-AvriNeural  # Avri (male)
  ```

- To fix a word that sounds wrong, edit its line in `phrases.txt` as
  `phrase | how to say it` and run the script again. Only changed lines are re-recorded.
- After adding words or games, refresh the list: in the browser console run
  `copy(allPhrases().join('\n'))` and paste it into `phrases.txt` (keep your `|` fixes).
  `missingClips` in the console shows anything the game tried to say without a clip.

Without `voice/voice.js`, the device voice is used:
- **iPad / iPhone:** Hebrew (Carmit) is built in.
- **Android:** Settings → Text-to-speech → Google → install Hebrew.
- **Windows:** Settings → Time & language → Speech → add Hebrew.

If there is no voice at all, the game still works and shows visual hints in place of the audio.

## Running it

- Open `index.html` in a browser, or
- Turn on GitHub Pages for this repo (Settings → Pages → deploy from branch) and open the link on the tablet.
  "Add to Home Screen" then makes it look like an app.

## Adding words

Words are in the `WORDS` list in `index.html` as `['word with nikud', 'emoji']`.
The game splits each word into syllable tiles automatically.

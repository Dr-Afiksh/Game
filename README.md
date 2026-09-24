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
Each game has 3 levels. A round with 7 or more first-try answers moves up a level, and a round with 3 or fewer moves down.
Progress is saved in the browser (localStorage), separately for each child.

## Voice

Spoken prompts use the browser's text-to-speech with a Hebrew voice (`he-IL`).
- **iPad / iPhone:** Hebrew (Carmit) is built in.
- **Android:** Settings → Text-to-speech → Google → install Hebrew.
- **Windows:** Settings → Time & language → Speech → add Hebrew.

If there is no Hebrew voice, the game still works and shows visual hints in place of the audio.

## Running it

- Open `index.html` in a browser, or
- Turn on GitHub Pages for this repo (Settings → Pages → deploy from branch) and open the link on the tablet.
  "Add to Home Screen" then makes it look like an app.

## Adding words

Words are in the `WORDS` list in `index.html` as `['word with nikud', 'emoji']`.
The game splits each word into syllable tiles automatically.

# Juhee Channel Uploader

A small personal Python tool that uploads short animated videos I make for young children to my own YouTube channel, using the YouTube Data API v3.

- Only I use this tool, and it only accesses my own channel.
- It uses one endpoint: `videos.insert`, with the `youtube.upload` scope.
- For each video it sets title, description, tags, category, privacy status and `selfDeclaredMadeForKids = true`.
- It does not read, store or display any YouTube data or other users' data.
- The only stored data is my own OAuth token, kept in a local file (`token.json`) that is never uploaded.

## Files

- `upload_video.py` – signs in with OAuth and uploads one video
- `auto_upload.py` – uploads videos from a local queue folder, at most 2 per run

## Privacy policy

See the privacy policy linked in the audit form.

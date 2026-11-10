# Channel Uploader (Juhee Channel Uploader)

**Privacy Policy:** https://short-night-d0f.notion.site/Privacy-Policy-for-Juhee-Channel-Uploader-4143376f42d48164bb5def28eaa33f35

This tool uses **YouTube API Services**. By using it you agree to the [YouTube Terms of Service](https://www.youtube.com/t/terms). See also the [Google Privacy Policy](https://policies.google.com/privacy).

A small personal Python tool that uploads short animated videos I make for young children (with AI animation tools) to my own YouTube channel, using the YouTube Data API v3.

- Only I use this tool, and it only accesses my own channel.
- It uses one endpoint: `videos.insert`, with the `youtube.upload` scope.
- For each video it sets title, description, tags, category, privacy status and `selfDeclaredMadeForKids = true`.
- It does not read, store or display any YouTube data or other users' data.
- The only stored data is my own OAuth token, kept in a local file (`token.json`) that is never uploaded.
- Access can be revoked at any time: https://security.google.com/settings/security/permissions

## Files

- `upload_video.py` – signs in with OAuth and uploads one video
- `auto_upload.py` – uploads videos from a local queue folder, at most 2 per run

## Demo

End-to-end screencast (run → upload → video live on YouTube): https://drive.google.com/file/d/1itJmrzISDWpiDs4rJHLlHcO4W73RbeDp/view

## Contact

pompomplay23@gmail.com

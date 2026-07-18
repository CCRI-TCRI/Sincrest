# Sincrest backend data

These files are Sincrest's own replacements for the data feeds MuseScore Studio
used to fetch from musescore.org/musescore.com. They're served straight out of
this repo via GitHub's raw-content URLs (`raw.githubusercontent.com`) — no
separate server needed. Editing one of these files and pushing to `main`
updates what the app sees within minutes (raw.githubusercontent.com caches for
a few minutes).

## learn_started_playlist.json / learn_advanced_playlist.json

Feeds the "Learn" page's video playlists (`src/app/configs/learn.cfg`).
Currently empty — add entries to populate the page:

```json
{
    "default": [
        {
            "title": "Getting started",
            "author": "Your name",
            "url": "https://youtube.com/watch?v=...",
            "thumbnailUrl": "https://img.youtube.com/vi/.../hqdefault.jpg",
            "durationSecs": 245
        }
    ]
}
```

You can also key by locale (e.g. `"en_US"`, `"fr_FR"` — underscore form, from
`QLocale().name()`) alongside `"default"`; the app looks up the current
locale first and falls back to `"default"` if that key is missing or empty.

## release_notes.json

Feeds the "what's new since your last update" notes shown for versions the
user skipped (`update.cfg`'s `all` key). Not required for auto-update itself
to work — only for that extra changelog view. Format:

```json
{
    "releases": [
        { "version": "1.1.0", "notes": "Release notes in markdown" }
    ]
}
```

## Auto-update itself

Auto-update does *not* use a file in here — `update.cfg`'s `latest` key
points directly at GitHub's own Releases API
(`https://api.github.com/repos/CCRI-TCRI/Sincrest/releases/latest`), since
the app's update checker already expects that exact JSON shape (`tag_name`,
`assets[].browser_download_url`). To ship an update: cut a GitHub Release on
this repo with a tag like `v1.2.3` and attach the built installers
(`.msi` for Windows, `.dmg` for macOS, `.AppImage` for Linux) as release
assets. The app will pick it up automatically.

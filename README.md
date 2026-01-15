# Parser Industry-Hardstyle-Sex
:)

## About the project
A parser of videos from porn sites. Downloads videos only in the best quality. Beginning of development 06.01.2026.

## Getting Started
Before starting the project, you need to do the following:

### Installation
1. Libraries for the correct operation of the project:
   - ```shell
      pip install requests
       ```
   - ```shell
       pip install bs4
       ```
   - ```shell
       pip install yt_dlp
      ```
   - ```shell
       pip install ffmpeg-python
       ```
2. Programs for downloading videos correctly:
    - `https://github.com/GyanD/codexffmpeg/releases/tag/2026-01-05-git-2892815c45`

### Create
Create a `data.json` file and write the following code. Then add your links to the `videos` dictionary:
```json
{
  "sites":
    {
      "AnalMedia": "anal.media",
      "Strip2": "vps402.strip2.co"
    },
  "videos":
    {
      "1": "https://vps402.strip2.co/video/...",
      "2": "https://anal.media/ru/video/..."
    }
}
```

## Roadmap
- [x] Add change log
- [ ] Add support site `NoodleMagazine`
- [ ] Add support site `UKDevilz`
- [ ] Add GUI

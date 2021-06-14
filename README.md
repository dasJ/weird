# Windows End-User ISO (Retail) Downloader

This is an automated tool to get Windows 10 download URLs.
Microsoft doesn't provide direct download links anymore, and instead expect the user to go through their website to create a link that is valid for 24 hours.
This tool does exactly that, but automated, yielding a downloadable URL (it doesn't download the file itself, as the title would suggest).

The project is heavily inspired by [FIDO](https://github.com/pbatard/Fido) but aims to provide a headless cross-platform experience.

### Editions

You can download any available edition for Windows.
Since Microsoft only offers one of them on their website, crawling the website and listing the options here doesn't make a lot of sense.
You can use "latest" for the latest version or check [FIDO](https://github.com/pbatard/Fido/blob/master/Fido.ps1#L75) for a lot of IDs.

## Dependencies

- [Requests](https://requests.readthedocs.io/en/master/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

## Usage

```
usage: weird.py [-h] [-8] [-l LANGUAGE] [-L] [-S] edition

positional arguments:
  edition               Edition to request - use "latest" for the latest version

optional arguments:
  -h, --help            show this help message and exit
  -8, --x86             Request x86 instead of x64
  -l LANGUAGE, --language LANGUAGE
                        Language to request link for
  -L, --list-langs      List languages instead of downloading
  -S, --show-edition    Show edition number we would download (mainly useful for the latest edition)
```

# License

MIT

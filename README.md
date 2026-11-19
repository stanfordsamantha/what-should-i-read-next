# What Should I Read Next?

Answer a few questions and get a book recommendation from a 149-book catalog.

- **Five questions:** what form of book (novel, stories or play), which shelf, where it's set, any extras (prize winner, adapted for screen, debut), and an optional favorite author.
- **A live match card:** it updates after every answer, showing the cover, the blurb and why the book fits, plus three other suggestions.
- **A reading list:** save the books you want to read. The list stays in your browser on that device.

It's a single self-contained `index.html` with no build step and no server code.

## Run locally

Open `index.html` in a browser, or serve the folder:

```bash
python3 -m http.server 8000
```

Then visit <http://localhost:8000>.

## Publish with GitHub Pages

1. Push this repository to GitHub.
2. Go to **Settings > Pages**.
3. Under **Build and deployment**, choose **Deploy from a branch**, pick `main` and `/ (root)`, and save.
4. The app appears at `https://<your-username>.github.io/<repo-name>/`.

## Files

Everything sits in one folder, so it uploads cleanly through GitHub's website.

```
index.html          the app
BK001-BK149         book cover images (.avif / .jpg), named by book id
read-next-*.png     home screen icons; read-next.svg, _base.svg.tmpl and
                    make.py are their sources
book_catalog.json   source catalog
inject_catalog.py   embeds the catalog into index.html
restyle.py          one-time theme script (already applied)
```

## Updating the catalog

Edit `book_catalog.json`, then re-embed it:

```bash
python3 -I inject_catalog.py book_catalog.json index.html
```

A book's cover is picked up automatically when a file named with its id sits next to `index.html`, for example `BK012.jpg`.

To redraw the icons, edit `make.py` or `_base.svg.tmpl` and run `python3 -I make.py`. On a Mac, `qlmanage -t -s 1024 -o . read-next.svg` turns the SVG into a PNG.

## Credits

Book cover images belong to their publishers and were collected from aalbc.com and Goodreads.

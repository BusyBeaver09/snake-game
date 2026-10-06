# Snake Game

A classic Snake game written in Python and Pygame by Eddie Liao.

## Play

Click the player to start and focus it. Use the arrow keys or W, A, S, and D to steer. Eat the red food to grow. Avoid the walls and your own body. The snake moves at 10 grid steps per second on a 20 by 20 board. Refresh the page to play again after the game ends.

## Source

The complete original source is preserved unchanged in `original_main.py`, copied from https://onecompiler.com/pygame/453hta9be on October 6, 2026. `main.py` preserves the original movement, collision, food, and win rules. Its loop uses `asyncio` instead of a blocking timer, and the original terminal game-over message is displayed on the canvas in browsers.

## Run locally

```sh
python -m pip install -r requirements.txt
python main.py
```

## Rebuild the browser version

```sh
python build_web.py
python -m http.server 8000
```

Open http://localhost:8000, click to start, and use the controls above. The build script packages only `main.py`, then copies the generated player and archives to the repository root. Pygbag downloads its Python/WebAssembly runtime from the official pygame-web CDN, so the first load needs an internet connection.

## Deploy

Import this repository into Vercel using the Other preset. `vercel.json` selects a static deployment with no build command and the repository root as the output directory. Rebuild and commit the generated files when changing `main.py`.

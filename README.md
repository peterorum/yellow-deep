# Use machine learning to generate colour palettes

Various bitos of code to train on colour palettes, analyse fractals generated from https://github.com/peterorum/functal, use Microsoft Vision API tp genertae captions, and then post to socials from lambda.

### notes on processing functals
* From the `data/hsl-json` folder, `scp functal://data/hsl-json/* .`
* From the `generate` folder, run `combine-jsons.py`, then `convert-to-csv`.
* From the `train` folder, run `003-split`.
* From the `classify` folder, run `node server.js` using the `predictions` file as test.

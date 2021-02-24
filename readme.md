# Steam Game Color Palette
## Description

This is a utility I built for a friend who was researching color palettes for a game he was developing. Some indy games go with a very specific artistic motif to brand the game or at least to stand out. This tool will download and analyze the screenshots from a game on Steam using OpenCV and SciKit Learn. The basic process flow is:

1. Check if the game already has screenshots on the local machine. If not, create a directory and download all the game's screenhots.
2. Resize the screenshots to be MUCH smaller. If you keep the images at the original size, the vector you create from them will be quite large and using any sort of cluster algorithm will be quite slow.
3. Convert the images into a vector space of their colors.
4. Use a K-Means clustering algorithm to find the 5 most common color areas *generally speaking*. While the tool will produce exact hex values, really it's looking at colors that are in clusters to give you the general idea of how the game is styled. 

The k-means clustering and bits that display the palette are largely copied from Adrian Rosebrocks fantastic work on [PyImageSearch.com](https://www.pyimagesearch.com/2014/05/26/opencv-python-k-means-color-clustering/).

## Example

Given this starting bank of screenshots:
![Starting Screenshots](https://github.com/SeanDrum/game-color-palette/blob/master/starting-screenshots.png)

Default settings will result in this palette being produced:
![Resulting Palette](https://github.com/SeanDrum/game-color-palette/blob/master/palette-example.PNG?raw=true)

## Use 

I suppose taking args from a command line would be the standard practice for a utility such as this, but since I developed this in VS Code the intended use case is to clone this repo and just edit the main() function's arguments directly. Parameters available to edit from the main (honestly you could edit *anything* but the things easily played with):

1. **GameId** - By far the most important argument as this dictates which game you wish to produce a pallet for. It's not exactly turnkey but if you know how to clone a Python repo it should be well within your capabilities. Basically every game on Steam has an ID. This is always found within the URL of the game's page. For instance, Cyberpunk 2077's URL is https://store.steampowered.com/app/1091500/Cyberpunk_2077/. Anyone who knows what GUID stands for will know that 1091500 is the game's ID. Plug that bad boy into the GameId argument and you're paletting Cyberpunk!
2. **NumClusters** - I played with this a bit and I found 5 to be the most effective number of clusters to produce. It gives you the gist of the game's palette without glossing over some of the finer points. Results may vary based on the color variance within a game, so sometimes more clusters may make sense.
3. **ImageScale** - This is the percentage that the image should be reduced to (i.e. a value of 30 will produce an image 30% of the size of the original). You could play with this to see if detailed images are losing pixels that are important to the essence of the palette. Of course, the higher the percentage, the larger the vector you're clustering, which means the longer the compute time. 

## Contact Information

Pick your poison at https://seandrum.github.io/.

## License

Emm Eye Tea
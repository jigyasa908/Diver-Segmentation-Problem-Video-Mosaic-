# Diver-Segmentation-Problem-using-OpenCV
## Process
* Build a background model (MOG or MOG2) across enough of the video frames that you can detect substantial motions.
* Use your background model as an initial version of your “foreground mosaic”.
* As you read through the video, use only the brightest frames out of a set of three to six frames.
* Using a background MOG or MOG2 model, identify a foreground region in one of the new frames.
* Performing some erosion to the foreground region, to remove small changes that happen in the background – like other pedestrians, or reflections on the water. Then look at the size of the region that is left.
* Once you find a region that is big enough in a frame, hopefully this is a diver in motion. 
* You may need to use some dilation to make the region big enough to include the diver and all his/her limbs, hairs, and other small features.
* Once you recognize a region that is big enough, add this new “foreground region” to your “foreground mosaic”.
* As each region is added to the foreground mosaic, create a “change map” of where the foreground has been changed.
* This map is important because in subsequent frames, you want to assure that there is no intersection between this map, and the new foreground region detected.
* Repeat the process of capturing a new foreground region, making sure it does not overlap with a previous region, and merging in the new foreground region, until you reach a good stopping point

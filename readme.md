# Mask Detect

### The Trained Model

The trained model is contained in `mask-detect/trained_model/saved model/`. **Do not modify any of the files in this directory**. These are the files used to define our ML model.

### Dependancies

To run the code, you need **tensorflow** and **numpy** installed.

#### Tensorflow Installation

Tensorflow installation instructions can be found here: https://www.tensorflow.org/install/pip

Note that Tensorflow recommends the use of Python virtual environments. It's not mandatory, but it will help to manage potential conflicts between dependancies.

#### Numpy Installation

The command below willl installl numpy. For more installation instructions: https://numpy.org/install/

`pip install numpy`

### Running the trained model

Ensure that `mask-detect/trained_model/test_files/` contains either `PNG` or `JPG` images. The ML model will test the images in this directory. You can find some sample files to use in the [shared Capstone Google Drive: `capstone/images/test_run_images`](https://drive.google.com/drive/u/1/folders/1UGOPLdQuEpYUie_RivxwGFTDOf0ECMzL)

To run the trained model, run the `mask-detect/trained_model/model_run.py` file. You may need to use either `python mask-detect/trained_model/model_run.py` or `python3 mask-detect/trained_model/model_run.py`, depending on the python version

When run,`model_run.py` will look at each of the fles in `mask-detect/trained_model/content/`, and output whether each image is of someone with or without a face mask.

# Do not commit images

This repo is using GitHub LFS (Large File Storage), which only provides 1 GB of data transfer a month. To avoid going over the data cap, **please do not upload any images to the respoitory.**

# Do not modify training and validation data

`train.zip` and `valid.zip` contain the training and validation data used to train the ML model. The code used to train the ML model depends on these files, so please do not modify them.

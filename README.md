# Live ASL Reader

## Dataset
https://www.kaggle.com/datasets/ayuraj/asl-dataset

## Crude outline and initial issues


### model_training
1. read in image data
2. preprocess data in prep for a CNN (Concurrent Neural Network)
3. determine a good starting CNN model
4. adjust model and hyperparameter tune
5. test/repeat step 4 (aim for >90% accuracy with test data)
6. export model

### camera_work
1. access/use camera
2. take image when hand is "still"?
3. preprocess image same as model training preprocessing
4. feed model the image

### issues
- missing 'U,V,W,X,Y,Z' in data

-------------------------



## Files
- 
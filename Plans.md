# Plans and Timeline

## Overall workflow

We plan to build up a multi-input model featured to handle various type of data. 

The information collected during the experiment includes three different types of data representation: image information (multi-modals image matrix), physical properties such as deformation and impedance (numeric information), and velocity profile(sequential data). 



![image-20210604031032073](file://C:/Users/wangs/OneDrive%20-%20Lehigh%20University/reportsandmeeting/060421/image-20210604031032073.png?lastModify=1623118759)



We need to build-up:

- A CNN model for handling static cell image
- A traditional MLP model to encode physics properties in the form of numeric data
- An RNN encoder to project the sequential data to a feature vector

## Data collection script

We already have a pre-written code ready for collecting image and velocity data out of cell video. The scripts are not in the perfect shape but can work in properly to handle the cell video. The 
# Patient Monitoring System with Computer Vision
This repository is dedicated to the development of a patient monitoring system for hospitals, utilizing computer vision to detect potentially dangerous situations such as falls, unusual movements, or the risk of pressure sores.


The primary objective of this project is to implement  soem key functionalities outlined by P. Kittipanya-Ngam, O. S. Guat, and E. H. Lung in their paper titled "Computer vision applications for patients monitoring system," presented at the 2012 15th International Conference on Information Fusion in Singapore (pp. 2201-2208). One such critical feature involves triggering an event if a bed remains unoccupied for an extended period. This detection mechanism, as suggested in the paper, can be efficiently implemented using  simple image processing techniques  implemented in OpenCV like Canny Edge Detection or Hough Line Transformation. 

## Getting started
To get this project up and running on your local machine for development and testing purposes, please follow these steps:
1. Clone the repository to your local machine using `git clone <repository-url>`.
2. Ensure that all external dependencies listed below are properly installed.
3. Follow the build dependencies instructions to set up the development environment.

## External dependencies
This project relies on several external frameworks and libraries, including:
- OpenCV for computer vision tasks. [OpenCV GitHub](https://github.com/opencv/opencv)
- TensorFlow for implementing machine learning models. [TensorFlow GitHub](https://github.com/tensorflow/tensorflow)

## Build dependencies
Refer to the Dockerfile in this repository for a comprehensive list of all build dependencies.
- [Link to Dockerfile](#)

If no Dockerfile is available, required dependencies will include:
- Python 3.8 or newer
- OpenCV 4.5 or newer
- TensorFlow 2.4 or newer

## Run dependencies
In addition to the build dependencies, running this system requires:
- A camera compatible with OpenCV for real-time video capture.
- Adequate hardware to support TensorFlow model inference.

## Authors
| Name | Email |
| ------ | ------ |
| Emircan Tutar    |  emircan.tutar@hs-weingarten.de   |
| Niklas Kleiser   | niklas.kleiser@hs-weingarten.de   |
| David Metzler    | david.metzler@hs-weingarten.de    |


## License
This project is licensed under the MIT License.

## Problems and solutions
For a detailed list of common problems encountered during the development of this project and their solutions, please refer to the following link:
[Problems and solutions](https://fbe-gitlab.hs-weingarten.de/prj-iki-robotics/orga/robolab-wiki/wikis/Problems-And-Solutions)

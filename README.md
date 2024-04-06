# **Comparing OpenCV's Object Tracking Algorithms**

**Authors:** [Rafael Rodríguez](https://github.com/rafardzp), [Alba Martínez]()

This repository contains code and resources for comparing different object tracking algorithms provided in the OpenCV library. The goal is to evaluate the performance, accuracy, and efficiency of these algorithms under various conditions and scenarios.

## **Table of Contents**

- [**Comparing OpenCV's Object Tracking Algorithms**](#comparing-opencvs-object-tracking-algorithms)
  - [**Table of Contents**](#table-of-contents)
  - [**Introduction**](#introduction)
  - [**Tested Algorithms**](#tested-algorithms)
  - [**Dataset**](#dataset)
  - [**Usage**](#usage)
  - [**Results**](#results)
  - [**Contributing**](#contributing)

## **Introduction**

Object tracking is a crucial task in computer vision applications, allowing for the continuous monitoring and analysis of objects in video streams. OpenCV provides several built-in object tracking algorithms. This project aims to provide a comprehensive comparison of these algorithms to aid researchers and developers in choosing the most suitable one for their specific use case.

## **Tested Algorithms**

The following object tracking algorithms from the OpenCV library are included in this project:

- **BOOSTING**: This algorithm is based on online boosting which combines multiple weak learners to create a strong classifier.

- **MIL (Multiple Instance Learning)**: MIL learns a classifier from a set of labeled bags, where each bag contains multiple instances of an object.

- **KCF (Kernelized Correlation Filters)**: KCF is a fast and accurate tracker based on the correlation filter framework.

- **TLD (Tracking, Learning, and Detection)**: TLD integrates tracking, learning, and detection to handle tracking failures effectively.
    
- **MedianFlow**: This algorithm utilizes a robust median flow model to track objects.

- **CSRT**: 

- **MOSSE**:
    
- **GOTURN**: GOTURN (Generic Object Tracking Using Regression Networks) employs deep convolutional neural networks to predict object locations.

- **DaSiamRPN**: 

- **Nano**: 

- **VIT**: 

## **Dataset**

The object tracking algorithms comparison is conducted using the XYZ dataset. This dataset consists of ... . You can download the dataset from [...]().

Options:

- [GOT-10k (Generic Object Tracking Benchmark)](https://paperswithcode.com/dataset/got-10k)

- [VOT2018](https://paperswithcode.com/dataset/vot2018)

- [LaSOT (Large-scale Single Object Tracking)](https://paperswithcode.com/dataset/lasot)

Please refer to the dataset's documentation for more details on its usage and licensing terms.


## **Usage**

TODO

## **Results**

The results of the object tracking comparison will be presented in a structured format, including metrics such as tracking accuracy, computational efficiency, and robustness to various challenges (e.g., occlusion, illumination changes, scale variation).

## **Contributing**

Contributions to this project are welcome! If you have suggestions for additional algorithms to include, improvements to the evaluation methodology, or any other enhancements, feel free to open an issue or submit a pull request.
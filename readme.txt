🏠 Building Segmentation with UNet  (uncomplete readme: project in progress)
A deep learning project for automatic building segmentation from aerial/satellite imagery using a UNet architecture. The model generates pixel-level masks to identify building footprints in aerial images.

📋 Table of Contents
Overview

Dataset

Model Architecture

Results

Installation

Usage

Project Structure

CI/CD Pipeline

API Deployment

Acknowledgments

🎯 Overview
This project implements a binary segmentation model to detect buildings in aerial/satellite imagery. The model outputs pixel-wise masks where:

1 = Building

0 = Background

Key Features
✅ UNet architecture with ResNet34 backbone (pretrained on ImageNet)

✅ COCO-format dataset integration from Roboflow

✅ Combined BCE + Dice Loss for handling class imbalance

✅ SAM (Segment Anything Model) integration for mask generation comparison

✅ CI/CD pipeline with GitHub Actions

✅ Docker containerization for easy deployment

✅ REST API for inference

📊 Dataset
Source: Roboflow - Buildings Instance Segmentation Dataset

Format: COCO Segmentation

Split:

Split	Images	Buildings
Train	~XX	~XXX
Validation	~XX	~XXX
Test	~XX	~XXX
Sample Data:

text
Dataset Structure:
├── train/
│   ├── _annotations.coco.json
│   └── images/
├── valid/
│   ├── _annotations.coco.json
│   └── images/
└── test/
    ├── _annotations.coco.json
    └── images/
🧠 Model Architecture
UNet with ResNet34 Backbone
python
Encoder: ResNet34 (pretrained on ImageNet)
├── Input: 512x512x3
├── Stage 1: 64 channels
├── Stage 2: 128 channels
├── Stage 3: 256 channels
└── Stage 4: 512 channels

Decoder (with skip connections):
├── Up-sampling + Convolution blocks
└── Output: 512x512x1 (sigmoid activation)

Total Parameters: ~24M
Loss Function
Combined Loss = BCE + Dice Loss

BCE Loss: Handles pixel-wise classification

Dice Loss: Addresses class imbalance (more buildings = fewer pixels)

📈 Results
Performance Metrics (on Test Set)
Metric	Score
IoU (Intersection over Union)	XX.XX%
Dice Score	XX.XX%
Precision	XX.XX%
Recall	XX.XX%
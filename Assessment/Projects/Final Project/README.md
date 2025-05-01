# DL Project: garbage classification on the Edge with Raspberry Pi

**Author:** Muchen Han  
**Edge Impulse project:** [View](https://studio.edgeimpulse.com/studio/683042)  
**GitHub repo:** [View](https://github.com/MCH0202/casa0018/)

---

### 🧩 Problem Statement

The project explores whether an edge device like Raspberry Pi, equipped with a camera, can carry out local waste classification using lightweight neural networks.

It addresses the challenge of sorting recyclables in shared spaces like campuses or public bins. By integrating an on-device AI system that can recognize the type of waste placed in front of a camera, the aim is to simplify user experience—only one drop point is needed, and the system does the classification internally.

This system operates without any network connection. A camera captures visual data, which is then interpreted by a model deployed locally. An LED indicator lights up to reflect the predicted category.

The model focuses on three waste types: **glass bottles**, **aluminum cans**, and **cardboard**. Visual data was manually captured under varied lighting and supplemented with internet-sourced samples to boost diversity.

---

### 🧪 Experiments Conducted

Several iterations were run to refine data, architecture, and deployment strategy.

- Initial labels (like food waste and plastic bottles) were replaced due to inconsistency in shape and difficulty in labelling.
- Multiple model structures were tested. Ultimately, MobileNetV2 was used for its compactness and accuracy tradeoff.
- Overfitting was a recurring issue. Earlier versions trained on homogenous backgrounds failed to generalize. Public data and diverse angles helped improve performance.
- Custom scripts were developed to visualize training logs via Colab for better insight into model behaviour.
- The final quantized model was deployed and tested live on Raspberry Pi. Classification triggered GPIO-based LED output with minimal latency.

📈 **Final model metrics:**

| Metric              | Value     |
|---------------------|-----------|
| Validation Accuracy | 79.6%     |
| Validation Loss     | 0.53      |
| Glass Bottle F1     | ~92%      |
| Can Misclass Rate   | ~32% into Glass |

> Example visual outputs and confusion matrix available in the edge impulse link.

---

### 🔍 Reflections and Key Learnings

- **Model tuning is not enough without thoughtful data**: I learned that model overfitting can stem more from dataset limitations than from model architecture itself.
- **Simplifying categories improves performance**: Avoiding ambiguous classes like food waste made model training far more stable.
- **Deployment reveals edge cases**: Real-world tests uncovered issues (like reflective glare on cans) that validation data didn’t fully expose.
- **Hardware-awareness matters**: Even small models behave differently under CPU constraints. Quantized deployment significantly improved performance on-device.

**Next steps** could include:
- Gathering more edge-case samples under difficult conditions.
- Enhancing image pre-processing to counter lighting variance.
- Exploring confidence-based decision thresholds to reduce false positives.

---

### 📌 Note

This project was completed for CASA0018 (UCL). Full training logs, images are in edge impulse link. The deployment code are available in this repository. 


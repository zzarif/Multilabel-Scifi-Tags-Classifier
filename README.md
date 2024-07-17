# Multilabel Scifi Tags Classifier
A multi-label text classification model from data collection, model training and deployment. The model can classify **160** different types of question tags from https://scifi.stackexchange.com. The keys of `tag_types_encoded.json` shows the list of question tags.

## Web Deployment

Developed a Flask Webapp and deployed to Vercel. It takes scifi and fantasy questions as input and classifies the relevant tags associated with the question via HuggingFace API. The webapp is live [here](https://multilabel-scifi-tags-classifier.vercel.app/).

1. The webapp takes scifi and fantasy questions as input:

![Flask App Scifi Tags Classifier](deployment/web_deployed_model0.png)

1. It utilizes HuggingFace API to classify the relevant tags:

![Flask App Scifi Tags Classifier](deployment/web_deployed_model1.png)
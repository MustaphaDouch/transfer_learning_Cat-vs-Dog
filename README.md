# transfer_learning_Cat_vs_Dog

## Description
Simple project for the classification of Cat and Dog images using transfer learning based on [MobileNet v2](https://tfhub.dev/google/tf2-preview/mobilenet_v2/feature_vector/4) pretrained NN fine-tuned by [Kaggle dataset](https://www.kaggle.com/competitions/dogs-vs-cats/overview) __(4000 images)__

## Directory tree
![dir_tree](https://github.com/MustaphaDouch/transfer_learning_Cat-vs-Dog/blob/main/github_readme/dir_tree.png)

#### _1. fastapi_
  Create small API to call _model.py_ where our saved trained model _transfer_learning_dog_vs_cat.h5_ was loaded

#### _2. streamlit_
  Create light UI to interacte with our API

#### _3. docker-compose.yaml_
  Used to run apps in static IP

#### _4. Transfer_learning_Dogs_vs_Cats.ipynb_
  Our project Notebook

#### _5. run.sh_
  Small bash script to automate creating docker images/container and up docker compose file
  _Note: Tested only in zshell env_

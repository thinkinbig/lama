# LAMA Proposal

Team 11

[our github repo](https://github.com/thinkinbig/lama)

## Content

---

* [Motivation](#1)
  * [What's the topic about](#1.1)

  * [Why choosing this](#1.2)

* [Ultimate Target](#2)

* [Plans & Models](#3)
  * [Challenges in a glimpse](#3.1)
  * [Data Preprocessing](#3.2)
  * [Features Engineering](#3.3)
  * [Models training](#3.4)

* [Datasets links](https://www.kaggle.com/c/elo-merchant-category-recommendation/data)

* Team Members
  * Zeyu Li
  * Toprak Emrah

* Project Name
  * Elo Merchant Category Recommendation

<h2 id=1> Motivation </h2>

---

- <h3 id="1.1">What's the topic about</h3>
  
    Have you ever experienced receiving nagging spams from companies who requires your email address as your account?
    You might have just asked for their services on that website once, and they relentlessly keep ruining your lives. Protecting your private data is one issue, but it is also these companies duty to figure out their clients' loyality on their services ans stop wasting time from clients from which the companies not profiting.

    And that's exactly what our topic is about. To help Elo, a credit card company in Brazil to identify and serve the most relevant opportunities to individals, reduce unwanted campaigns and create the right experience for customers. 

    for more detailed infos, you can click on the website: [Elo Merchant Category Recommendation](https://www.kaggle.com/c/elo-merchant-category-recommendation)


- <h3 id="1.2">Why choosing this</h3>

  This is the first time we making data analysis on our own. We have planned making a plan on mask detection before, but we don't want to scratch the surface. Making this project should be a starting point of further study, not an end point.

  That's why we've given up our previous plan and chosen a competition on Kaggle instead.
  Concerning the difficulty we may encountered during our process, we chose a competition that had been closed, and of course also an interesting competition. We can reference other people's solution to learn how to tune the datas, and make our model perform better.


<h2 id=2> Ultimate Goal</h2>

---

- As the competition's goal implies, we will make a regression model to fit the loyality of different clients, the perfoemance of our model will be scored online by Kaggle.
Submissions are scored on the root mean squared error. 


- check out the website for more details:
- [Overview](https://www.kaggle.com/c/elo-merchant-category-recommendation/overview)


<h2 id=3> Plans & Models </h2>

---
  - <h3 id="3.1">Challenges in a glimpse</h3>

    Perhaps the most significant challenges lies in the enormous datasets. The overall raw datasets provided by the officials amounts 3.1Gb. It's almost impossible to load all datasets into memories. Critical technics like Generator notation, gc collector and slice notation will be deployed to ease the burden, an elaborate software design will also come into play. 

    Another difficulty is to make fully use of the data, which requires an in-dept understanding of each tables.

  - <h3 id="3.2">Data Preprocessing</h3>
  
    This includes filter out Nan values, check unique columns, convert object values to numericals, catagorize discrete and continous features, scaling columns with Standardizer or Normalizer. More detailed technics relies on specific context, *a prior* statements of this types not possible.

  - <h3 id="3.3">Features Engineering</h3>
    The quality of our training models weighs heavily on this part. To get a more accurate models more features will be added based on additional Datasets provided by the officials. It is also where we have to strike the balance between time and accuracy. Features selections tricks like PCR, filter methods, wrapper methods will be settled to get best filter set.
  - <h3 id="3.4">Models training</h3>
    By models training, we will firstly make a simple prototype(e.g. RandomForest), and optimize our model either by applying more optimizors or tuning the hyperparameters.
    Note that hyperparameters in preprocessing and features engineerings will also be included in this section so a clear and reusable software architecture matters. 
    
    **The hyperparameters by default will be saved as yaml(or json) configuration files to enable a quick and non-side-effect altering.**

# Project Summary


In this section we will explain what we have done in our project. You can also refer to our presentation which we think (unfortunately though) are quite detailed.

### Short Introduction

Our project is separated into different sections. The general utility class lies in util folder, all datas and **`results`** will be found in data folder. In preprocessing folder you will find a preprocessing notebook, which records how we process the datas, and some utility classes specified in preprocessing datas.

A short introduction to our Streamerbuilder.You might think designing such a class unnecessary. In fact, we have a big dataset we think may cause trouble directly reading into the memory. When designing this class, we have no idea whether this table has an effects on our datasets into the model, that is, the model's training and testing dataset can also be that large. Luckily that doesn't happen. We have also suggest python can read the whole files as stream concurrently, however, reading a file and processing it can't run in pararell because of [GIL](https://wiki.python.org/moin/GlobalInterpreterLock). So speeding up failed, but we managed to limits only 10**6 lines into memory.

### Data Processing

The first thing we've done is to analyze the data. In short, we have inspected every data dictionaries, tried to figure out each columns' meaning and their correlations. We have also plot some distributions to see their distributions. After that we replace NaNs with means and drop outliers outside IQR, converting category columns into numericals(similar to Integer Encoding, but we've forgotten this method). Then we aggregate all tables into one large train-, test table, appending features extracted from other tables.
Honestly speaking there is a lot more we can do to refine our feature engineering. For example, we can observe the user with the same card-id's merchants patronizations in timeseries. And extracts their favorite shops as new features, from this aspect we believe a RNN model might help. Since we don't have enough time preparing a vastly different datasets to be feed into RNN, we gave up this idea.

### Model Training

We have prepared different tree ensembled algorithms based on decision tree. We don't spend a lot of time tuning parameters because we hope to solve underfitting problem with other tactics. Firstly we trained with random forest, the model is underfitting even after hyperparameter optimizations. However, training with random forest proves that decision tree based algorithms work. So we continued with our model, to solve the underfitting problem we select another boosting tree model(lightGBM and Xgboost). This time it works better even before hyperparamters tuning. However, when we want to combine these models together, we don't know if there exists a tree based stacking library. After making our stacking by ourself, we make only one layer, and the time left don't allow us to put the whole process into one layer sothat we can reuse the layer and training stacking with multiple times.
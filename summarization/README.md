## Summarizing Amazon product reviews and descriptions

This directory contains code for the end-to-end summarization application for Amazon product descriptions and reviews. Broadly there are following stages:

1. Data Collection
2. Data Labelling and processing
3. Benchmarking with out-of-the-box model
4. Finetuning to improve the performance
5. Package/Dockerize the finetuned model for deployment
6. Deploy/Test the deployed service

Let us look at the details of each of these steps.

### 1. Data Collection

[Here](https://cseweb.ucsd.edu/~jmcauley/datasets/amazon_v2/) is the link for the data we used for our summarization tasks. This is a large-scale dataset containing Amazon product reviews and metadata from May 1996 - Oct. 2018, this is released by UCSD's [McAuley Lab](https://cseweb.ucsd.edu/~jmcauley/) in 2019. There is a newer [2023 version](https://amazon-reviews-2023.github.io/) of this data that contains Amazon data from May 1996 to Sep. 2023 but we used the 2018 version for our project.

Please note this data is for large-scale purposes and here are the numbers from the website for reference: 

- **raw review data (34gb)** - all 233.1 million reviews
- **ratings only (6.7gb)** - same as above, in csv form without reviews or metadata
- **5-core (14.3gb)** - subset of the data in which all users and items have at least 5 reviews (75.26 million reviews)
- **meta data (24gb)** - metadata for 15.5 million products - includes descriptions, price, sales-rank, brand info, and co-purchasing links.


These files are spanned across various categories as below but we considered only the two highlighted categories due to infrastructure limitations - 

- Amazon Fashion
- All Beauty
- Appliances
- Arts Crafts and Sewing
- Automotive
- Books
- CDs and Vinyl
- **Cell Phones and Accessories**
- Clothing Shoes and Jewelry
- Digital Music
- **Electronics**
- Gift Cards
- Grocery and Gourmet Food
- Home and Kitchen
- Industrial and Scientific
- Kindle Store
- Luxury Beauty
- Magazine Subscriptions
- Movies and TV
- Musical Instruments
- Office Products
- Patio Lawn and Garden
- Pet Supplies
- Prime Pantry
- Software
- Sports and Outdoors
- Tools and Home Improvement
- Toys and Games
- Video Games


We are summarizing two aspects of an Amazon product - 
1. **Product Description** - This is Combination of product information and features that are available in the `metadata` files. This summary should contain the highlights of the product's features.
2. **Product Reviews** - We considered the `5-core` files to extract the reviews information. This summary should give the **pros**, **cons**, and a **final verdict** of the product based on the reviews.

Please find these raw file in `data/raw_compressed/*` folder.


### 2. Data Labelling and processing

We couldn't find any ready-to-use dataset for the type of summaries we want to generate. So we had to create labels on our own and create a dataset to train summarization models. For this we used Gemini API to create label summaries for us. 

Files used to create these are `create_labels_gemini_descriptions.ipynb`, and `create_labels_gemini_reviews.ipynb` to creating summaries for product descriptions, and product reviews respectively. 
Further processing and splitting the labelled data into train, dev and test files can be found in `create_dataset.ipynb` and `train/finetune/product_reviews/data_preprocess.ipynb` files for product descriptions and reviews respectively.


### 3. Benchmarking with out-of-the-box model

We had to consider various factors for selecting a model which we will finetune to improve the baseline scores. Some of the important factors we considered are -

- Model should be of reasonable size to run on any consumer hardware
- It should compete with the similar and larger size models for summarization
- It should be resistant to noisy inputs

After considering all the above factors, we chose [BART](https://arxiv.org/pdf/1910.13461v1.pdf) model because of its impressive downstream capabilities for seq-to-seq tasks like summarization. This is a 400M parameter encoder-decoder model released in 2019. Here is a quick comparision with another SOTA encoder-decoder model [T5](https://arxiv.org/pdf/1910.10683.pdf) for the CNN/Daily Mail summarization - 

```
                    ROUGE-1     ROUGE-2     ROUGE-L

T5-Large (770M)     42.50       20.68       39.75
T5-3B               42.72       21.02       39.94
T5-11B              43.52       21.55       40.69

BART-Large (400M)   44.16       21.28       40.90
```

As shown in the above benchmark, BART is an impressive model for summarization task. It outperformed or matched the performance of similar architecture SOTA model that is ~27 times bigger. Due to its performance-per-size, we selected BART model for our summarization tasks.

Before fine-tuning, we ran the BART-Large-CNN model which is the finetuned for summarization on our test-set to get the initial baseline scores which we hope to improve further.

Please find the scores and code used for the benchmark in `train/benchmark/*` folder.

### 4. Finetuning to improve the performance

TBD










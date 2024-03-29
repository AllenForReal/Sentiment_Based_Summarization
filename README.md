# Sentiment_Based_Summarization

The surge in data availability and data processing methods has led to many applications. 
This project, aimed at capturing sentiment and summarizing Amazon product reviews using 
web scraping, represents a significant stride in the data-driven market landscape. 
Integrating Natural Language Processing for sentiment analysis crucially deciphers customer 
reviews' emotional tones. This insight is vital for understanding customer satisfaction and pinpointing 
areas for product improvement. The project further innovates by condensing lengthy reviews into concise
summaries through sophisticated algorithms, saving considerable time for both consumers and businesses. 
Automating data collection through web scraping ensures efficiency and scalability, 
enabling rapid compilation of extensive datasets. Incorporating data visualization and a user-friendly 
interface simplifies the interpretation and utilization of this data for businesses, analysts, and consumers. 
This project offers companies deep customer insights and competitive advantages and is a valuable tool for market research and academic exploration in data science, NLP, and e-commerce. Its alignment with consumer-centric approaches, promotion of data-driven decision-making, and technological innovation in web scraping, NLP, and data visualization make it a highly relevant and scalable solution across various e-commerce platforms and industries, thus standing out for its practical application in enhancing customer experience and driving business strategies.

Here are the links to the Kaggle dataset:

Amazon review: https://www.kaggle.com/datasets/kritanjalijain/amazon-reviews/data

Reddit sarcasm: https://www.kaggle.com/datasets/danofer/sarcasm

Todo:
1. Average the reviews for both sentiment & summarization, improving from just one or first review.
2. Take the sentiment analysis result into the input parameter for summarization model.
3. Give user option to switch between different models.
4. Storing summarized data for multiple client requests.
5. Hashmap for storing product id & its corresponding sentiment+summary, store it for a period of time, the do an update. (interactive feature, where user enters a price point for a product, then we use something like pagerank to give some of the best results i.e. product) 

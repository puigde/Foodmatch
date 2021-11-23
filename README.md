## The problem
Having trouble in deciding where to eat nowadays has become a common problem. Foodmatch provides NLP-based solution to solve that issue. 

## What it does
Our software provides two functionalities: The matchfinder and the feedback filterer. 
->The matchfinder allows you to find the 5 most compatible restaurants according to your indicated preferences.
->Once you have recieved your top candidates, if you are not decided, you can receive a compact representation of their strong and weak points using the feedback filterer.

## How we built it
We did fine-tuning on a pre-trained sentiment classification neural network, obtaining a very powerful and review-specialised classification tool. For example: if you run "The nachos were good. Although the service was slow." our model will identify "The nachos were good" as positive and that "the service was slow" as a negative.

->The matchfinder has a search algorithm that finds relationships between your preferences and the positive statements in all restaurants, computes a score, ranks them and returns you a top 5.

-> In the feedback filter we have adapted the model to identify strong and weak points in multiple but also in single reviews which is even more impressive. For the same example as before: the more "nachos" similarities we find in positive reviews of a given restaurant, the highest the score we will give it as a positive point and reverse for the negative aspects. 

->feedback filterer could also be used as a way for businesses to obtain a compact overview on the strong and weak points of their business from all the reviews they have received without the need to go one by one.

## Challenges, accomplishments and learning
We are second year students so we had little to no experience with neither neural networks or clustering algorithms. The implementation process was full of ups and downs, the toughest challenge we faced was when we finished training the first model we selected it had some bugs related to tensor dimensions and when we finally managed to fix them the model was not performing as expected. We decided to change it with not much time left that leaving us with a small margin of error but through some discussion we were able to find and train a second one which ended up working wonders. 

In addition to this we consider that the risk of failure was very large as the difficulty level of the techniques we use is quite considerable, specially for our previous knowledge and experience. But the idea was there and it motivated us even more as it was a bigger challenge which enabled us to grow our skills a lot.

## What makes us different:
Our algorithm is not biased depending on who pays us more, allows real-time customisation so it's flexible for every user.

## What's next for Foodmatch
Foodmatch should age like fine wine, getting better as time goes by and the dataset gets bigger and we can bring results with more precision. To make it even faster a cloud or local database would also be really helpful and should be considered in the future. 

## REPO limitations:
-> we could not include both json files as the second one is too big but can be downloaded in the neural network notebook
-> we could not include the neural network archive but can be reproduced executing the neural network notebook

For more info contact: pol.puigdemont@estudiantat.upc.edu

# Based on the 12 steps of ML projects laid out by Cassie Kozyrkov
[Source](https://medium.com/swlh/12-steps-to-applied-ai-2fdad7fdcdf3)

![Infographic version](https://miro.medium.com/max/720/1*DWpwjk-yqNliqQlkqBKfUw.webp)

Most of the list below is Ms. K's (or at least my interpretation of her content). Some of it is my own addition. 

0) Reality Check and Setup
   1) Do you need ML?
      1) Small decisions?
      2) Non-ML not getting the job done?
      3) Have enough data?
      4) Have the hardware?
1) Define your Objective
   1) What is success? Can it be objectively measured?
   2) What are the GO/NO-GO performance criteria for an ML model to move to production?
2) Data Collection
   1) How are you getting the data?
   2) If supervised, how is it getting labeled?
3) Split the Data
   1) Splits: Training, Validation, Testing
4) Exploratory Data Analysis
   1) Use your Training dataset.
   2) Run stats and sanity checks.
   3) Consider engineering new features.
5) Prepare Your Tools
   1) The dataset won't be in a form that the ML tools can accept.
   2) The data will require "formatting".
   3) My approach is to build a composite object that holds:
      1) the data in a Pandas DataFrame,
      2) traceability info, i.e. a full path and filename if stored locally, something unique descriptive, easily traceable, and human-readable,
      3) basic stats about each feature,
      4) labels for plotting, i.e. "Wine Quality", to provide an easy way of building automated plotting tool.
6) Train Models
   1) Ms. K recommends splitting your Dataset and finding and exploiting patterns in it.
   2) My approach would be to start simple and work towards more complexity.
      1) Does something like Least-Squares work for a regression problem?
      2) No, try again after some feature engineering. No reason feature engineering should stop in Step 4.
      3) Still no, what about a Decision Tree?
   3) If your dataset has a common format, such as was laid out in Step 5, the simple models can be explored automatically without a lot of engineer time. If you are exploring a large dataset it might still require a lot of computer time.
7) Debug, Analyze, and Tune
   1) Debug: Why is the ML model giving my garbage answers? If you've split your Training dataset into 2 pieces, as recommended in Step 7, you have a holdout dataset to work with here.
   2) Analyze: Advanced analytics specific to the dataset.
   3) Tune: Search the Hyperparameter space.
8) Validate the Models
   1) Do anything you like with the Training dataset. Don't even look at the Validation dataset until this step.
   2) The Validation dataset must remain isolated from all previous steps in order for the validation to be meaningful.
   3) Run the Validation dataset through the models and look only at the performance metric. If it isn't good enough go back to previous steps. Work only with the Training dataset.
9) Test the Model
   1) The Testing dataset hasn't been run through any analysis or model until this step.
   2) Run the Testing dataset on the best model from Step 8.
   3) If your best model passes, move on. Otherwise, the ML project dies. No 2nd chances for tuning this model or trying more models. You get 1 shot at the Testing dataset.
10) Productionize the Model
    1) Make the model work on the production environment including scaling, adversarial attacks, and more.
11) Run Live Experiments to Launch Safely
    1) Gradually bring the model online.
12) Monitor and Maintain


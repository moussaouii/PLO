# Evaluation

Once the model has been trained.The question is How “good” is the model that it came up with? That’s where our test set comes into play. Since our learning algorithm hasn’t “seen” this test set before, it should give us a pretty unbiased estimate of its performance on new, unseen data! So, what we do is to take this test set and use the model to predict the class labels. Then, we take the predicted class labels and compare it to the “ground truth,” the correct class labels to estimate its generalization accuracy.

To evaluate the model rasa nlu provides the script `evaluate.py`. This allows you to test your models performance for intent classification and entity recognition. You invoke this script supplying test data, model, and config file arguments:

    python -m rasa_nlu.evaluate \
        --data data/examples/rasa/demo-rasa.json \
        --model projects/default/model_20180323-145833

Where **model** specifies the model to evaluate on the test data specified
with **data**.

### Creating a test set

To measure how good the model generalize, the test set to should also be generalized means to have almost every kind of input(structures of sentences in our case).

We had to manually create the data set (data/test_generalised.json).You can use a simple tool to help you creat the test data.

### Important Note

- **This is a tool to edit your data set for rasa NLU 🤔** [Read About rasa-nlu-trainer](https://github.com/RasaHQ/rasa-nlu-trainer)

Intent Classification
---------------------
The evaluation script will log precision, recall, and f1 measure for
each intent and once summarized for all.
Furthermore, it creates a confusion matrix for you to see which
intents are mistaken for which others.

When working with intities (affirmative, greet, ...) here is the output of the evaluation concerning the intities.

<img align="center" height="244" src="https://github.com/mlabyad/hello-World/blob/master/Evaluate_model_with_logs_intities.png">


Entity Extraction
-----------------
For each entity extractor, the evaluation script logs its performance per entity type in your training data.
So if you use ``ner_crf`` and ``ner_duckling`` in your pipeline, it will log two evaluation tables
containing recall, precision, and f1 measure for each entity type.

In the case ``ner_duckling`` we actually run the evaluation for each defined
duckling dimension. If you use the ``time`` and ``ordinal`` dimensions, you would
get two evaluation tables: one for ``ner_duckling (Time)`` and one for
``ner_duckling (Ordinal)``.

``ner_synonyms`` does not create an evaluation table, because it only changes the value of the found
entities and does not find entity boundaries itself.

Finally, keep in mind that entity types in your testing data have to match the output
of the extraction components. This is particularly important for ``ner_duckling``, because it is not
fitted to your training data.

When working with entities (destination, origin, ...) here is the output of the evaluation concerning the entities.


<img align="center" height="244" src="https://github.com/mlabyad/hello-World/blob/master/Evaluate_model_with_logs_entities_ner_crf.png">

Evaluation Parameters
---------------------

There are a number of parameters you can pass to the evaluation script

    $ python -m rasa_nlu.evaluate --help

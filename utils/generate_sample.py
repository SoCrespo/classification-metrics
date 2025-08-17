import uuid
import random
import pandas as pd


def generate_sample(sample_size:int=10000, nb_categories:int=7): 
    data = []
    categories = ["CATEGORY_" + str(i) for i in range(1, nb_categories+1)]

    # Simulate varying performance (accuracy from 0.5 to 1) according to category
    performances_per_category = {cat: random.randint(5, 10)/10 for cat in categories}

    for _ in range(sample_size):
        category = random.choice(categories)
        performance_for_category = performances_per_category[category]
        ground_truth = random.choice([0, 1])
        # Simulate prediction with probability of it being same as ground truth = performance_for_category
        prediction = ground_truth if bool(random.random() < performance_for_category) else int(not ground_truth)
        data.append({
            "id": str(uuid.uuid4()),
            "category": category,
            "is_category_real_value": ground_truth,
            "is_category_prediction": prediction
    })

    return pd.DataFrame(data)

from typing import Union

import numpy as np
import pandas as pd


def subsampling(data: Union[np.ndarray, pd.DataFrame],
                key: Union[int, str],
                formula: str = "paper",
                threshold: float = 1e-5) -> Union[np.ndarray, pd.DataFrame]:
    r"""Drop occurrences of the most frequent word tokens with the following condition by the given threshold
    value: if :math:`P_{\text{random}} > P_{\text{drop}}`, where :math:`P_{\text{random}} \in U(0, 1)` and 
    :math:`P_{drop} = 1 - \sqrt{\frac{t}{f}}` or :math:`P_{drop} = \frac{f - t}{f} - \sqrt{\frac{t}{f}}`,
    where :math:`f = frequency and t = threshold.`

    Hence,

    #. more samples of token will be dropped if the word token is more frequent, when threshold is larger.

    #. samples of word token where the frequent of it is lower than the threshold will not be dropped.
    
    Args:
        data (Union[np.ndarray, pd.DataFrame], shape = (Number of samples, ...)): A np.array or pd.DataFrame of raw data.
        key (Union[int, str]): An integer of index or a string of name of target field to be used for subsampling.
        formula (str): A string to select which formula to calculate drop ratio in subsampling. Allows: [\"code\"|\"paper\"].
        threshold (float, optional): A float of threshold of subsampling. 
            Defaults to 1e-5.
    
    Raises:
        ValueError: when formula is not in [\"code\"|\"paper\"].
    
    Returns:
        Union[np.ndarray, pd.DataFrame], shape = (Number of subsample samples, ...): A np.array or pd.DataFrame of subsample data.

    :Reference:

    #. `Tomas Mikolov et al, 2013. Distributed Representations of Words and Phrases and their Compositionality <https://arxiv.org/abs/1310.4546>`_.
    
    #. `Omer Levy et al, 2015. Improving Distributional Similarity with Lessons Learned from Word Embeddings <https://levyomer.files.wordpress.com/2015/03/improving-distributional-similarity-tacl-2015.pdf>`_.

    """
    # select the formula used in subsampling
    if formula == "code":
        formula_func = lambda f, t: (f - t) / f - np.sqrt(t / f)
    elif formula == "paper":
        formula_func = lambda f, t: 1 - np.sqrt(t / f)
    else:
        raise ValueError("formula only allows : [\"code\"|\"paper\"].")

    # initialize columns' selector with lambda function
    if isinstance(data, np.ndarray):
        row_func = lambda d, row_key: d[row_key]
        col_func = lambda d, col_key: d[:, col_key]
        val_func = lambda d, row_key, col_key: d[row_key, col_key]
        cat_func = lambda samp: np.vstack(samp)
    elif isinstance(data, pd.DataFrame):
        row_func = lambda d, row_key: d.iloc[row_key]
        cat_func = lambda samp: pd.DataFrame(samp, columns=data.columns).reset_index(drop=True)

        if isinstance(key, int):
            col_func = lambda d, col_key: d.iloc[:, col_key]
            val_func = lambda d, row_key, col_key: d.iloc[row_key, col_key]
        else:
            col_func = lambda d, col_key: d[col_key]
            val_func = lambda d, row_key, col_key: d.loc[row_key, col_key]
    else:
        raise TypeError("type of data is not allowed.")

    # select columns from data
    columns = col_func(data, key)

    # count occurrences of each token
    uniques, counts = np.unique(columns, return_counts=True)

    # calculate the frequencies of each token
    freq = counts / np.sum(counts)

    # calculate the subsampling probabilities
    prob = formula_func(freq, threshold)

    # created subsampling probabilities dict
    prob = dict(zip(uniques, prob))

    # generate random values for each row of samples
    rand_prob = np.random.random(size=(data.shape[0]))

    # subsampling
    sampled_data = []
    for i in range(data.shape[0]):
        if rand_prob[i] > prob[val_func(data, i, key)]:
            sampled_data.append(row_func(data, i))

    return cat_func(sampled_data)

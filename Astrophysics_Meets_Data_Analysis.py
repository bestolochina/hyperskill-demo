import pandas as pd


def stage_1(df: pd.DataFrame) -> None:
    """Prepare the data"""
    # Remove the missing values from the dataset
    df = df.dropna(axis='index')

    # Find a mean value for the IGL mean surface brightness in groups of galaxies (mean_mu)
    # with LSB features (features) and without them;
    mean_values = df.groupby('features')['mean_mu'].mean()

    # Print two floating-point numbers separated by a space:
    # the mean value of the mean surface brightness for galaxies with and without LSB features.
    print(mean_values[1], mean_values[0])


if __name__ == '__main__':
    # Read the following dataset: groups.tsv. TSV stands for tab-separated values.
    # Use the pandas.read_csv() function with the parameter delimiter='\t';
    data = pd.read_csv('groups.tsv', sep='\t')

    stage_1(data)

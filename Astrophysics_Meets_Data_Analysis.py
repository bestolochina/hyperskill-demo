import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt


def stage_1() -> None:
    """Prepare the data"""
    # Read the following dataset: groups.tsv. TSV stands for tab-separated values.
    # Use the pandas.read_csv() function with the parameter delimiter='\t';
    df = pd.read_csv('groups.tsv', sep='\t')

    # Remove the missing values from the dataset
    df = df.dropna(axis='index')

    # Find a mean value for the IGL mean surface brightness in groups of galaxies (mean_mu)
    # with LSB features (features) and without them;
    mean_values = df.groupby('features')['mean_mu'].mean()

    # Print two floating-point numbers separated by a space:
    # the mean value of the mean surface brightness for galaxies with and without LSB features.
    print(mean_values[1], mean_values[0])


def stage_2() -> None:
    """One-way analysis of variance"""
    # Read the following dataset: groups.tsv. TSV stands for tab-separated values.
    # Use the pandas.read_csv() function with the parameter delimiter='\t';
    df = pd.read_csv('groups.tsv', sep='\t')

    # Conduct the Shapiro-Wilk Normality test for the IGL mean surface brightness (the mean_mu column) in galaxies
    # with LSB features and without them. This step checks the second condition of the ANOVA test: each sample came
    # from a normally distributed population. Is the condition satisfied?
    sample_features = df[df['features'] == 1]['mean_mu']
    sample_no_features = df[df['features'] == 0]['mean_mu']

    shapiro_features = stats.shapiro(sample_features, nan_policy='omit')
    shapiro_no_features = stats.shapiro(sample_no_features, nan_policy='omit')

    # Perform the Fligner-Killeen Homogeneity test for variances of the same two data samples. This step checks the
    # third condition: the samples came from populations with equal variances. Is the condition satisfied?
    _, fligner_killeen_pvalue = stats.fligner(sample_features, sample_no_features, nan_policy='omit')

    # Perform the one-way ANOVA test and obtain a p-value. The test's null hypothesis is that both groups (galaxies
    # with LSB features and without them) are drawn from the populations with the same IGL mean surface brightness.
    # Do LSB features significantly influence the IGL mean surface brightness according to the test?
    one_way_anova = stats.f_oneway(sample_features, sample_no_features, nan_policy='omit')

    # Print four floating-point numbers. Separate them with one space: two p-values for the Shapiro-Wilk test for
    # galaxies with LSB features and without them, one p-value obtained from the Fligner-Killeen test,
    # and one p-value of the ANOVA test.
    print(shapiro_features.pvalue, shapiro_no_features.pvalue, fligner_killeen_pvalue, one_way_anova.pvalue)


def stage_3() -> None:
    """Isolated galaxies and galaxies in groups"""
    # Read the datasets: galaxies_morphology.tsv and isolated_galaxies.tsv. Use the pandas.read_csv() function with
    # the parameter delimiter='\t';
    group_galaxies = pd.read_csv(r'C:\Users\T480\Downloads\galaxies_morphology.tsv', sep='\t')
    isolated_galaxies = pd.read_csv(r'C:\Users\T480\Downloads\isolated_galaxies.tsv', sep='\t')

    # Plot the histograms for the Sérsic index (n) for both datasets;
    # bin_edges = np.arange(0, 12.5, 0.5)
    # fig, ax = plt.subplots(figsize=(8, 6))  # Set figure size
    # n1, bins1, patches1 = ax.hist(isolated_galaxies['n'], bins=bin_edges, alpha=0.5, color='red',
    #                               label='Isolated Galaxies', edgecolor='black')
    # n2, bins2, patches2 = ax.hist(group_galaxies['n'], bins=bin_edges, alpha=0.5, color='blue',
    #                               label='Group Galaxies', edgecolor='black')
    # for patch in patches1:
    #     patch.set_hatch('/')  # Forward slashes for Isolated Galaxies
    # for patch in patches2:
    #     patch.set_hatch('\\')  # Backward slashes for Group Galaxies
    # ax.grid(True, linestyle='--', alpha=0.7)  # Dashed grid for better readability
    # ax.set_xlabel('Sérsic Index (n)', fontsize=12)
    # ax.set_ylabel('Count', fontsize=12)
    # ax.set_title('Histogram of Sérsic Index for Galaxies', fontsize=14)
    # ax.legend(loc='upper right')
    # plt.show()

    # Calculate a fraction of galaxies with the Sérsic index n>2 for both datasets;
    group_galaxies_fraction = group_galaxies[group_galaxies['n'] > 2].shape[0] / group_galaxies.shape[0]
    isolated_galaxies_fraction = isolated_galaxies[isolated_galaxies['n'] > 2].shape[0] / isolated_galaxies.shape[0]

    # Perform the two-sample Kolmogorov-Smirnov test to check whether galaxies from two samples are similar for the
    # Sérsic index and obtain a p-value. Note that you must use a two-sided alternative for this test. It means that
    # the null hypothesis is that the two given samples are drawn from the same probability distribution;
    ks_2sample = stats.ks_2samp(group_galaxies['n'], isolated_galaxies['n'], alternative='two-sided')

    # Print three floating-point numbers separated by one space: fractions of galaxies with the Sersic index n>2 for
    # groups and isolated galaxies and a p-value obtained from the Kolmogorov-Smirnov test.
    print(group_galaxies_fraction, isolated_galaxies_fraction, ks_2sample.pvalue)


if __name__ == '__main__':

    stage_3()

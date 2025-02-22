import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
from astropy.cosmology import FlatLambdaCDM
from astropy import units as u
from astropy.coordinates import SkyCoord
from itertools import combinations
# import warnings
#
# warnings.simplefilter("ignore", category=DeprecationWarning)  # Suppress DeprecationWarning



def stage_1() -> None:
    """Prepare the data"""
    # Read the following dataset: groups.tsv. TSV stands for tab-separated values.
    # Use the pandas.read_csv() function with the parameter delimiter='\t';
    df = pd.read_csv(r'C:\Users\T480\Downloads\groups.tsv', sep='\t')

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
    df = pd.read_csv(r'C:\Users\T480\Downloads\groups.tsv', sep='\t')

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


def stage_4() -> None:
    """Intra-group light component and galaxy morphology"""
    # Continue working with galaxies_morphology.tsv from the previous stage. Calculate the mean Sérsic index and the
    # mean numerical Hubble stage for each CG. Group data by the Group column. The values of the new table are the
    # mean Sérsic index (n) and the mean numerical galaxy type (T). Create the columns mean_n and mean_T for obtained
    # values with the help of the .agg() method from pandas.
    group_galaxies = pd.read_csv(r'C:\Users\T480\Downloads\galaxies_morphology.tsv', sep='\t')
    new_group_galaxies = group_galaxies.groupby(by='Group').agg(mean_n=('n', 'mean'), mean_T=('T', 'mean'))

    # Use the Group column and merge the data table with the one from groups.tsv you preprocessed in Stage 1;
    groups = pd.read_csv(r'C:\Users\T480\Downloads\groups.tsv', sep='\t')
    merged = new_group_galaxies.reset_index().merge(right=groups, how='outer', on='Group').dropna()

    # Plot scatterplots for the following value pairs: mean_mu-mean_n and mean_mu-mean_T;
    # plt.scatter(x=merged['mean_mu'], y=merged['mean_n'], color='blue', label='mean_mu vs mean_n')
    # plt.scatter(x=merged['mean_mu'], y=merged['mean_T'], color='red', label='mean_mu vs mean_T')
    # plt.xlabel('mean_mu')
    # plt.ylabel('Values')
    # plt.legend()

    fig, ax = plt.subplots(1, 2, figsize=(10, 5))  # 1 row, 2 columns
    ax[0].scatter(merged['mean_mu'], merged['mean_n'], color='blue')  # First scatter plot
    ax[0].set_xlabel('mean_mu')
    ax[0].set_ylabel('mean_n')
    ax[0].set_title('mean_mu vs mean_n')
    ax[1].scatter(merged['mean_mu'], merged['mean_T'], color='red')  # Second scatter plot
    ax[1].set_xlabel('mean_mu')
    ax[1].set_ylabel('mean_T')
    ax[1].set_title('mean_mu vs mean_T')
    plt.tight_layout()  # Adjust layout to prevent overlap
    plt.show()

    # Conduct the Shapiro-Wilk Normality tests for each variable: mean_mu, mean_n, and mean_T;
    shapiro_mean_mu = stats.shapiro(merged['mean_mu'], nan_policy='omit')
    shapiro_mean_n = stats.shapiro(merged['mean_n'], nan_policy='omit')
    shapiro_mean_T = stats.shapiro(merged['mean_T'], nan_policy='omit')

    # Calculate the Pearson correlation coefficients and the corresponding p-values for testing non-correlation.
    # The null hypothesis of the test is that the considered populations are not correlated;
    valid_mu_n = merged[['mean_mu', 'mean_n']].dropna()
    valid_mu_T = merged[['mean_mu', 'mean_T']].dropna()
    pearson_mean_mu_vs_mean_n = stats.pearsonr(x=valid_mu_n['mean_mu'], y=valid_mu_n['mean_n'])
    pearson_mean_mu_vs_mean_T = stats.pearsonr(x=valid_mu_T['mean_mu'], y=valid_mu_T['mean_T'])

    # Print five floating-point numbers separated by one space: p-values for normality testing of mean_mu,
    # mean_n and mean_T, and p-values for testing non-correlation for mean_mu-mean_n and mean_mu-mean_T.
    print(shapiro_mean_mu.pvalue, shapiro_mean_n.pvalue, shapiro_mean_T.pvalue,
          pearson_mean_mu_vs_mean_n.pvalue, pearson_mean_mu_vs_mean_T.pvalue)


def stage_5() -> None:
    """Median projected separation"""
    # Initialize the ΛCDM cosmology model with the parameters H0=67.74, Ωm=0.3089 using astropy.cosmology.FlatLambdaCDM
    model = FlatLambdaCDM(H0=67.74, Om0=0.3089)

    # Read the dataset with galaxies' equatorial coordinates: galaxies_coordinates.tsv.
    # Use the pandas.read_csv() function with the parameter delimiter='\t'
    df = pd.read_csv(r'C:\Users\T480\Downloads\galaxies_coordinates.tsv', sep='\t')

    # Calculate the angular diameter distances, dAdA, in kiloparsecs for groups' redshifts (the z column in
    # groups.tsv from the Stage 1) using the cosmology model method angular_diameter_distance
    groups = pd.read_csv(r'C:\Users\T480\Downloads\groups.tsv', sep='\t')
    groups['ad_distances'] = model.angular_diameter_distance(groups['z']).to(u.kpc).value

    # Calculate the projected median separation. It is the median of the pairwise projected distance between
    # the galaxies in each group. It is denoted as r in the formula from the Theory section.
    # Use astropy.coordinates.SkyCoord with the "fk5" coordinate frame. To find the angular distance, θ,
    # between two points with the sky coordinates p1 and p2, use the separation method of the SkyCoord object
    def median_separation(df: pd.DataFrame, groups: pd.DataFrame) -> float:
        """Compute the median physical separation (in Mpc) for all galaxy pairs within the group."""

        pairs = list(combinations(df.itertuples(index=False), 2))  # Generate all unique pairs

        separations = []
        for p1, p2 in pairs:
            coord1 = SkyCoord(ra=p1.RA * u.deg, dec=p1.DEC * u.deg, frame='fk5')
            coord2 = SkyCoord(ra=p2.RA * u.deg, dec=p2.DEC * u.deg, frame='fk5')
            separation = coord1.separation(coord2).to(u.rad).value  # Convert to radians

            # Extract angular diameter distance (assumes one value per group)
            ad_distance_series = groups.loc[groups['Group'] == p1.Group, 'ad_distances']
            if ad_distance_series.empty:
                continue  # Skip if no matching group

            ad_distance = ad_distance_series.values[0]  # Extract scalar value

            r = separation * ad_distance  # Compute physical distance
            separations.append(r)

        return np.median(separations) if separations else np.nan  # Handle single-galaxy groups

    # Apply function to each group and store the median separation
    median_separations = df.groupby("Group")[['Group', 'Name', 'RA', 'DEC']].apply(median_separation, groups=groups).reset_index(name="Median_Separation")
    merged = median_separations.merge(right=groups, how='outer', on='Group')

    # Plot a scatterplot for the projected median separation and the IGL mean surface brightness (mean_mu)
    plt.scatter(x=merged['Median_Separation'], y=merged['mean_mu'], color='red', label='Median_Separation vs mean_n')
    plt.xlabel('R (kpc)')
    plt.ylabel(r'$\mu_{IGL,r} (mag~arcsec^{-2})$')  # Correct LaTeX formatting
    plt.legend()
    plt.gca().invert_yaxis()  # Invert the Y-axis
    plt.show()

    merged = merged.dropna()

    # Conduct the Shapiro-Wilk Normality test for the projected median separation and mean_mu
    shapiro_median_separation = stats.shapiro(merged['Median_Separation'], nan_policy='omit')
    shapiro_mean_mu = stats.shapiro(merged['mean_mu'], nan_policy='omit')

    # Calculate the Pearson correlation coefficient and the corresponding p-value
    # for testing the non-correlation for these values
    valid_data = merged[['Median_Separation', 'mean_mu']].dropna()
    pearson_median_separation_vs_mean_mu = stats.pearsonr(x=valid_data['Median_Separation'], y=valid_data['mean_mu'])

    # Print four floating-point numbers separated with a space: the projected median separation for the HCG 2 group,
    # p-values for the normality test of the projected median separation and mean_mu,
    # and a p-value for testing the non-correlation for these values
    print(merged.loc[merged['Group'] == 'HCG 2', 'Median_Separation'].iloc[0],
          shapiro_median_separation.pvalue,
          shapiro_mean_mu.pvalue,
          pearson_median_separation_vs_mean_mu.pvalue)


if __name__ == '__main__':

    stage_5()

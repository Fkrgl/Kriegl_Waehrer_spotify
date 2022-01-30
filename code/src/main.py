"""
Data Literacy - WiSe 21
Project: Assessment of Spotify Chart Preferences across Different Countries
Authors: Florian Kriegel (5746680), Jonathan Waehrer (5776535)

Main script.
"""

# --------------------------------------------------- IMPORTS -------------------------------------------------------- #
# Packages
import os
import pandas as pd

# Scripts
import download_spotify_data
import download_kaggle_data
import sample_kaggle_data
import create_training_data
import regression_models


# ---------------------------------------------------- MAIN ---------------------------------------------------------- #
def main():
    print("====== Data Literacy - WiSe 21, Florian Kriegel (5746680) & Jonathan Waehrer (5776535) ====== ")
    print("###### Project: Assessment of Spotify Chart Preferences across Different Countries ######\n")

    # ======== Load Spotify data sets ======== #
    print("=== Loading Data ===")
    # === Load Spotify chart playlists
    print("Attempting to load charts data from 'code/dat/'...")
    if not os.path.isfile("../dat/charts_data.csv"):
        print("     ...'charts_data.csv' not found in directory...")
        download_spotify_data.main(playlist_links="../dat/spotify_links.txt",
                                   country_codes="../dat/spotify_countries.txt",
                                   continent_codes="../dat/spotify_continents.txt")

    # === Load Spotify data set from Kaggle
    print("Attempting to load kaggle spotify data set from 'code/dat/'...")
    if not os.path.isfile("../dat/kaggle_data.csv"):
        print("     ...'kaggle_data.csv' not found in directory...")
        download_kaggle_data.main(dropbox_file="/kaggle_data.csv", output="../dat/kaggle_data.csv")
    print("DONE\n")

    # ======== Data preprocessing ======== #
    print("=== Preprocessing Data ===")
    # Sample kaggle data and write to .csv
    sample_kaggle_data.main()
    # Create training data
    create_training_data.main()
    print("DONE")

    # ======== Apply regression models to predict popularity ======== #
    print("=== Applying ML model to predict popularity ===")
    regression_models.main()

if __name__ == "__main__":
    main()
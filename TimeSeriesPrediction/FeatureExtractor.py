__author__ = 'denniscf'
import pandas as pd
import numpy as np

class FeatureExtractor:
    def __init__(self):
        className = "featureExtractor"

    def ExtractUpDown(self, dfSeries):
        pctChange = np.array(dfSeries.pct_change())
        featureUpDown = (pctChange > 0)*2 - 1 #1 for up -1 for down
        return featureUpDown

    def ExtractIntensity(self, dfSeries):
        uBoundLow = 0.3
        lBoundMed = 0.3
        uBoundMed = 0.7
        lBoundHigh = 0.7

        pctChange = np.array(dfSeries.pct_change())
        pctChange = np.abs(pctChange)
        featureIntensity = (pctChange - np.min(pctChange))/(np.max(pctChange) - np.min(pctChange))
        featureIntensity[featureIntensity < uBoundLow] = -1
        featureIntensity[featureIntensity >= lBoundMed and featureIntensity < uBoundMed] = 0
        featureIntensity[featureIntensity < lBoundHigh] = 1

        return featureIntensity


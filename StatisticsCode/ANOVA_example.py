# -*- coding: utf-8 -*-

import pandas as pd
import scipy.stats as stats
from statsmodels.formula.api import ols
import statsmodels.stats.anova as anova

galton = pd.read_csv("galton.csv")

height = galton[['sex', 'height']]

m_height = height.query("sex=='M'").height
f_height = height.query("sex=='F'").height
a_height = height.height

print(stats.f_oneway(m_height, a_height))
print(stats.f_oneway(f_height, a_height))
print(stats.f_oneway(m_height, f_height))

B = ols('height ~ C(sex)',data=height).fit()
print(anova.anova_lm(B))
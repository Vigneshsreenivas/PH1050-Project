import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
df = pd.read_csv("ElementData.csv")
noble = df[df['Symbol'].isin(["He", "Ne", "Ar", "Kr", "Xe"])]
noble=noble.set_index('Symbol')
ratio=noble['MeltingPoint']/noble['BoilingPoint']
#Helium does not have a melting point at 1 atm, so it is NaN.
ratio=ratio.dropna() #drop helium
print("ratios are: \n",ratio,"mean of ratios:",np.mean(ratio),"standard deviation of ratios:",np.std(ratio,ddof=1)) #we can see the ratios
n=len(ratio)
mean = np.mean(ratio)
sd = np.std(ratio, ddof=1)
t = stats.t.ppf(0.975, n-1) #t value for 95% confidence interval with n-1=3 degrees of freedom
half1 = t * sd / np.sqrt(n) #half-width of the confidence interval
ci = (mean - half1, mean + half1)
print("95% confidence interval of the mean:", ci)

plt.figure(figsize=(5, 4))
plt.axhspan(mean - sd, mean + sd, color="grey", alpha=0.2, label="mean ± 1 SD")
plt.axhline(mean, color="grey", linestyle="--")
plt.scatter(ratio.index, ratio.values, color="blue", zorder=3)
plt.ylabel("T_melt / T_boil")
plt.xlabel("Noble gas")
plt.title("Noble-gas melting/boiling ratio")
plt.legend()
plt.tight_layout()
plt.savefig("noble_gas_ratio.png", dpi=200)
#okay we can see neon is the outlier from this as it is the only one outside the mean ± 1 SD range. Now we will calculate the prediction interval to see if neon is an outlier.

ratio2= ratio.drop("Ne")
mean2 = np.mean(ratio2)
sd2 = np.std(ratio2, ddof=1)
n2=len(ratio2)
t2 = stats.t.ppf(0.975,n2-1) #t value for 95% prediction interval with n-1=2 degrees of freedom
half2 = t2 * sd2 * np.sqrt(1 + 1/len(ratio2)) #Prediction interval formula. It accounts for the uncertainty in the mean AND the variability of individual observations.
pi = (mean2 - half2, mean2 + half2)
print("95% prediction interval:", pi)
low, high = pi
ne = ratio["Ne"]
if ne < low or ne > high:
    print("Ne =", round(ne, 4), "-> OUTSIDE the interval, so Ne is an outlier")
else:
    print("Ne =", round(ne, 4), "-> INSIDE the interval, so no evidence Ne is an outlier")


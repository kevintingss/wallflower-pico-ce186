import pandas as pd
import datetime
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import matplotlib.image as mpimg


table = pd.read_excel("Bear Transit data (cleaned).xlsx", header =7).loc[:16]
cleaned = table[["Stop", "Passenger Count", "Time", "Latitude", "Longitude"]]
cleaned["location"] = np.array(["After stop" for i in np.arange(len(cleaned))])
cleaned_before = pd.DataFrame()
# manipulate y
y = cleaned["Passenger Count"]
y1 = np.append([0], y[:-1])

# manipulate x
x = cleaned["Time"]
my_day = datetime.date(2014, 7, 15)
x_dt = [ datetime.datetime.combine(my_day, t) for t in x]
x_before = [ t-datetime.timedelta(seconds=1) for t in x_dt]
x1 = matplotlib.dates.date2num(x_dt)
x2 = matplotlib.dates.date2num(x_before)

## update pandas
cleaned_before["Stop"] = cleaned["Stop"]
cleaned_before["Passenger Count"] = y1
cleaned_before["Time"] = [i.time() for i in x_before]
cleaned_before["location"] = np.array(["Before stop" for i in np.arange(len(cleaned))])
cleaned_before["Latitude"] = cleaned["Latitude"]
cleaned_before["Longitude"] = cleaned["Longitude"]

## concat pandas
df_repeated = pd.concat([cleaned, cleaned_before], ignore_index=True).sort_values(by="Time")
df_repeated["Stop"] = df_repeated["Stop"].str.replace(' ', '\n', regex=False)
df_repeated["time_and_stop"] = df_repeated["Time"].astype(str) + "\n" + df_repeated["Stop"].astype(str)
new_x = df_repeated["Time"]
new_x1 = df_repeated["Stop"]
new_x2 = df_repeated["time_and_stop"].reset_index(drop=True)
new_y = df_repeated["Passenger Count"].reset_index(drop=True)

fig = plt.figure(figsize=[10, 6])

sns.set()
sns.set_style("ticks")
for i in np.arange(len(new_x2)):
    # plot
    ax = sns.lineplot(x=new_x2, y=new_y, marker="o",dashes=False)
    plt.xlabel("Time and Bus Stop")
    plt.ylabel("Passenger Count")
    plt.ylim(-1, 27)
    # highlight point
    # legend
    if new_y[i] > 20:
        color = "red"
    else:
        color = "green"
    #
    ax.scatter(new_x2[i], new_y[i], color ="red", s=100)
    plt.ylim(-1, 27)

    sns.set_style("ticks")
    sns.despine(left=True)

    # setting ticks
    ax.set_xticklabels('')
    pos = np.arange(len(new_x2))[0:len(new_x2):2]
    l = new_x2[1:len(new_x2):2]
    ax.set_xticks(pos+0.5,      minor=True)
    ax.set_xticklabels(l, minor=True)
    plt.tick_params(axis='x', which='minor', labelsize=6)
    # plt.locator_params(axis='y', nbins=len(new_y)/2)

    # set grids and depine
    plt.grid(linestyle='dotted')
    sns.despine(offset=14)

    legend = plt.legend(title = "Avg Passengers OnBoard\n\n                   "+ str(int(new_y[i])),
                        edgecolor="white",
                        facecolor=color,
                        shadow=True,
                        framealpha=0.7,
                        loc=1,
                        fancybox=True,
                        borderpad=1
                        )

    j = 0
    for v in np.arange(len(new_x2) / 2):
        plt.axvspan(xmin=new_x2[j], xmax=new_x2[j + 1], alpha=0.1, color="grey")
        j += 2

    # ### plot
    plt.setp(legend.get_title(), color='white', fontweight=600, fontsize=10, fontstyle="italic")
    plt.title("Bear Transit Bus Occupancy Levels from 8AM to 8:30AM \n (Perimiter Line)", fontstyle="italic")
    plt.tight_layout()
    plt.savefig("plot" + str(i) +".png", dpi=200)
    plt.draw()
    plt.pause(0.1)
    plt.clf()

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

    if new_y[i] > 20:
        color = "red"
    else:
        color = "green"
    # ### plot
    if i+1 < 8:
        current_image = str(i+1) + ".png"
    elif (i+1 >= 8) & (i+1<17):
        current_image = "visual0" + str(i-7+1) + ".png"
        print("second")
        print(current_image)
    elif i+1 >=18:
        current_image = "visual" + str(i-8+1) + ".png"
        print("third")
        print(current_image)


    image = mpimg.imread("./GIF Images/" + current_image)
    im = plt.imshow(image)
    plt.axis('off')
    legend = plt.legend(title="Avg Passengers OnBoard\n\n                   "+ str(int(new_y[i])),
                        edgecolor="white",
                        facecolor=color,
                        shadow=True,
                        framealpha=0.7,
                        loc=1,
                        fancybox=True,
                        borderpad=1
                        )

    plt.setp(legend.get_title(), color='white', fontweight=600, fontsize=10, fontstyle="italic")
    plt.title("Bear Transit Bus Occupancy Levels from 8AM to 8:30AM \n (Perimiter Line)", fontstyle="italic")
    plt.tight_layout()
    fig.savefig('map' + str(i) +".png", dpi=300)
    plt.draw()
    plt.pause(0.1)
    plt.clf()

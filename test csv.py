
csvfile = open('C:\\Users\\guia2812\\Desktop\\test.csv', "w")

data_x = []
data_y = []

for x in range(21):
    data_x.append(x*-1e-5)
    data_y.append(x)
    csvfile.write("{},{}\n".format(data_x[-1], data_y[-1]))

csvfile.close()


load "spider-template.gnuplot"

# set title "Best 5 Models"
array Data_labels[8] = ["sn", "population", "elite_rate", "crossover", "mutation_rate",\
      "mutation_change", "error", "generations"]


# set terminal png size 400,400

# best 5 models
array Model_1[8] = [1826, 264, 0.083333, 0.125, 0.15, 0.01,  0.00587, 23]
array Model_2[8] = [2483, 374, 0.058824, 0.375, 0.20, 0.06,  0.00587, 15]
array Model_3[8] = [802, 49, 0.142857, 0.250, 0.10, 0.01,  0.00587, 34]
array Model_4[8] = [2901, 374, 0.045455, 0.125, 0.05, 0.01,  0.00587, 37]
array Model_5[8] = [1703, 204, 0.083333, 0.375, 0.15, 0.01,  0.00587, 49]

# set output "best-models.png"

plot 	  keyentry with spiderplot ls 6 title sprintf("Model %4d (ε=%.4e, %dG)", Model_5[1], Model_5[7], Model_5[8]),\
 	  for [i=2:6] Model_5 using (Model_5[i]) ls 6,\
 	  newspiderplot,\
 	  keyentry with spiderplot ls 7 title sprintf("Model %4d (ε=%.4e, %dG)", Model_4[1], Model_4[7], Model_4[8]),\
 	  for [i=2:6] Model_4 using (Model_4[i]) ls 7,\
 	  newspiderplot,\
 	  keyentry with spiderplot ls 8 title sprintf("Model %4d (ε=%.4e, %dG)", Model_3[1], Model_3[7], Model_3[8]),\
 	  for [i=2:6] Model_3 using (Model_3[i]) ls 8,\
 	  newspiderplot,\
 	  keyentry with spiderplot ls 9 title sprintf("Model %4d (ε=%.4e, %dG)", Model_2[1], Model_2[7], Model_2[8]),\
 	  for [i=2:6] Model_2 using (Model_2[i]) ls 9,\
 	  newspiderplot,\
 	  keyentry with spiderplot ls 10 title sprintf("Model %4d (ε=%.4e, %dG)", Model_1[1], Model_1[7], Model_1[8]),\
 	  for [i=2:6] Model_1 using (Model_1[i]) ls 10


# worst 5 models
array Model_6[8] = [3003, 484, 0.045455, 0.375, 0.0, 0.01,  0.009886, 0]
array Model_7[8] = [428, 34, 0.500000, 0.375, 0.1, 0.01,  0.009886, 0]
array Model_8[8] = [1103, 119, 0.142857, 0.375, 0.2, 0.01,  0.009886, 0]
array Model_9[8] = [2398, 374, 0.058824, 0.375, 0.0, 0.21,  0.009886, 0]
array Model_10[8] = [3054, 484, 0.045455, 0.500, 0.1, 0.01,  0.009886, 0]

# set output "worst-models.png"

plot      keyentry with spiderplot ls 1 title sprintf("Model %4d (ε=%.4e, %dG)", Model_10[1], Model_10[7], Model_10[8]),\
	  for [i=2:6] Model_10 using (Model_10[i]) ls 1,\
 	  newspiderplot,\
 	  keyentry with spiderplot ls 2 title sprintf("Model %4d (ε=%.4e, %dG)", Model_9[1], Model_9[7], Model_9[8]),\
 	  for [i=2:6] Model_9 using (Model_9[i]) ls 2,\
 	  newspiderplot,\
 	  keyentry with spiderplot ls 3 title sprintf("Model %4d (ε=%.4e, %dG)", Model_8[1], Model_8[7], Model_8[8]),\
 	  for [i=2:6] Model_8 using (Model_8[i]) ls 3,\
 	  newspiderplot,\
 	  keyentry with spiderplot ls 4 title sprintf("Model %4d (ε=%.4e, %dG)", Model_7[1], Model_7[7], Model_7[8]),\
 	  for [i=2:6] Model_7 using (Model_7[i]) ls 4,\
 	  newspiderplot,\
 	  keyentry with spiderplot ls 5 title sprintf("Model %4d (ε=%.4e, %dG)", Model_6[1], Model_6[7], Model_6[8]),\
 	  for [i=2:6] Model_6 using (Model_6[i]) ls 5,\

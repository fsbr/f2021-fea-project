import numpy as np

midterm = 88
quizavg = 10*np.mean([10,8,10,10,10,9])
hwavg = np.mean([90, 71, 94, 92, 95, 85, 88, 30,30,30])

project = 80 
finalexam = 80 
print("quiz", quizavg)
print("hw", hwavg)

finalGradeEst = 0.25*hwavg + 0.15*midterm +  0.1*quizavg + 0.15*project + 0.35*finalexam 
print("finalGrade", finalGradeEst)

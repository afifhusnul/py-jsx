#!/usr/bin/python3
import sys

math_paper1_marks = int(input("Insert your mid-term Mathematic paper 1 exam marks :"))
math_paper2_marks = int(input("Insert your mid-term Mathematic paper 2 exam marks :"))

total = math_paper1_marks + math_paper2_marks

math_marks = total/160 * 100

if (math_marks >= 90):
        print("\nAstounding effort! you got an A+")
elif (math_marks <= 80 and math_marks < 90):
	print("\nExtraordinary! that's a A for you")

elif (math_marks <= 70 and math_marks < 80):
	print("\nClose call! At least it's an A-")

else:
	 print("\nThere is more room to improve Dont lose motivation!")

# -*- coding: utf-8 -*-
E={}
RL='''const readline = require("readline");
const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
const ask = (q) => new Promise((res) => rl.question(q, res));
'''
E['7a']=dict(date='24.08.26',title='ELECTRICITY BILL CALCULATION',
aim='To write a JavaScript (Node.js) program that reads the units consumed and calculates the electricity bill using slab-wise tariff rates.',
steps=['Start the program and read the number of units consumed from the user.','Charge Rs. 2 per unit for the first 100 units.','Charge Rs. 3 per unit for the next 100 units (101 to 200).','Charge Rs. 5 per unit for every unit above 200.','Add the slab amounts to get the total bill.','Display the units consumed and the total bill amount.'],
code=[('exp7a.js',RL+'''
(async () => {
  const units = Number(await ask("Enter units consumed: "));
  let bill = 0;
  if (units <= 100) {
    bill = units * 2;
  } else if (units <= 200) {
    bill = 100 * 2 + (units - 100) * 3;
  } else {
    bill = 100 * 2 + 100 * 3 + (units - 200) * 5;
  }
  console.log("Units Consumed : " + units);
  console.log("Total Bill     : Rs. " + bill);
  rl.close();
})();''')],
runs=[(['260'],['Enter units consumed: '])],
result='Thus, the electricity bill was calculated from the units consumed using slab-wise rates in JavaScript.')
E['7b']=dict(date='24.08.26',title='STUDENT MARKS ANALYSIS',
aim='To write a JavaScript program that reads the marks of five subjects and finds the total, average, highest mark, lowest mark and grade.',
steps=['Start the program and create an empty array to hold the marks.','Read the marks of five subjects from the user and store them in the array.','Find the total of the marks using a loop.','Calculate the average by dividing the total by five.','Find the highest and the lowest mark using Math.max() and Math.min().','Decide the grade from the average and display all the results.'],
code=[('exp7b.js',RL+'''
(async () => {
  const marks = [];
  for (let i = 1; i <= 5; i++) {
    marks.push(Number(await ask("Enter mark " + i + ": ")));
  }
  let total = 0;
  for (const m of marks) total += m;
  const avg = total / marks.length;
  let grade = "C";
  if (avg >= 90) grade = "O";
  else if (avg >= 80) grade = "A+";
  else if (avg >= 70) grade = "A";
  else if (avg >= 60) grade = "B";
  console.log("Marks   : " + marks.join(", "));
  console.log("Total   : " + total);
  console.log("Average : " + avg);
  console.log("Highest : " + Math.max(...marks));
  console.log("Lowest  : " + Math.min(...marks));
  console.log("Grade   : " + grade);
  rl.close();
})();''')],
runs=[(['91','84','77','95','88'],['Enter mark 1: ','Enter mark 2: ','Enter mark 3: ','Enter mark 4: ','Enter mark 5: '])],
result='Thus, the JavaScript program to analyse the marks of a student was executed successfully.')
E['7c']=dict(date='24.08.26',title='ATM PIN VERIFICATION',
aim='To write a JavaScript program that verifies an ATM PIN with a maximum of three attempts and blocks the card after three wrong entries.',
steps=['Store the correct four-digit PIN in a variable and set the attempt counter to zero.','Ask the user to enter the PIN.','Compare the entered PIN with the stored PIN.','If both match, display "PIN Verified" and stop.','If they do not match, increase the counter and display the attempts left.','After three wrong attempts, display "Card Blocked" and stop the program.'],
code=[('exp7c.js',RL+'''
(async () => {
  const correct = "4821";
  let tries = 0;
  while (tries < 3) {
    const pin = await ask("Enter your PIN: ");
    if (pin === correct) {
      console.log("PIN Verified");
      rl.close();
      return;
    }
    tries++;
    console.log("Wrong PIN. Attempts left: " + (3 - tries));
  }
  console.log("Card Blocked");
  rl.close();
})();''')],
runs=[(['1234','4821'],['Enter your PIN: ','Enter your PIN: ']),(['1111','2222','3333'],['Enter your PIN: ','Enter your PIN: ','Enter your PIN: '])],
result='Thus, the ATM PIN verification program with three attempts was implemented successfully in JavaScript.')
E['7d']=dict(date='24.08.26',title='SHOPPING PURCHASE AMOUNT',
aim='To write a JavaScript program that reads the prices of four products, finds the total purchase amount and applies a discount for bills of Rs. 2000 or more.',
steps=['Start the program and create an array for the product prices.','Read the price of each of the four products from the user.','Add the prices to find the total purchase amount.','Check whether the total is Rs. 2000 or more.','If it is, give a 10 percent discount; otherwise give no discount.','Display the total, the discount and the final amount to pay.'],
code=[('exp7d.js',RL+'''
(async () => {
  const prices = [];
  for (let i = 1; i <= 4; i++) {
    prices.push(Number(await ask("Price of product " + i + ": ")));
  }
  const total = prices.reduce((a, b) => a + b, 0);
  const discount = total >= 2000 ? total * 0.10 : 0;
  console.log("Total Amount  : Rs. " + total);
  console.log("Discount      : Rs. " + discount.toFixed(2));
  console.log("Amount to Pay : Rs. " + (total - discount).toFixed(2));
  rl.close();
})();''')],
runs=[(['450','900','300','250'],['Price of product 1: ','Price of product 2: ','Price of product 3: ','Price of product 4: ']),(['899','1250','640','410'],['Price of product 1: ','Price of product 2: ','Price of product 3: ','Price of product 4: '])],
result='Thus, the JavaScript program to find the shopping purchase amount with discount was executed successfully.')
E['7e']=dict(date='24.08.26',title='EMPLOYEE ANNUAL SALARY',
aim='To write a JavaScript program that uses an array of objects to calculate and display the annual salary and the annual salary with bonus of each employee.',
steps=['Create an array of employee objects holding the name and monthly salary.','Use a loop to visit every employee in the array.','Calculate the annual salary as monthly salary multiplied by 12.','Calculate the bonus as 8 percent of the annual salary.','Display the name, monthly salary, annual salary and the salary with bonus.','Repeat until all employees are processed.'],
code=[('exp7e.js','''const employees = [
  { name: "Akhilesh Raj P", salary: 32000 },
  { name: "Naveen R", salary: 28500 },
  { name: "Divya S", salary: 41000 }
];

console.log("Employee Details");
console.log("------------------------");
for (const e of employees) {
  const annual = e.salary * 12;
  const withBonus = annual + annual * 0.08;
  console.log("Name           : " + e.name);
  console.log("Monthly Salary : Rs. " + e.salary);
  console.log("Annual Salary  : Rs. " + annual);
  console.log("With 8% Bonus  : Rs. " + withBonus);
  console.log("------------------------");
}''')],
runs=[([],[])],
result='Thus, the JavaScript program to calculate the annual salary of employees was executed successfully.')
KEYS=['7a','7b','7c','7d','7e']

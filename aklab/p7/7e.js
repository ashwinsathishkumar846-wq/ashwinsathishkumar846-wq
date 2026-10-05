const employees = [
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
}
const readline = require("readline");
const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
const ask = (q) => new Promise((res) => rl.question(q, res));

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
})();
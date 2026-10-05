const readline = require("readline");
const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
const ask = (q) => new Promise((res) => rl.question(q, res));

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
})();
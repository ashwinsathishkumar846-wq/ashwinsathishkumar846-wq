const readline = require("readline");
const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
const ask = (q) => new Promise((res) => rl.question(q, res));

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
})();
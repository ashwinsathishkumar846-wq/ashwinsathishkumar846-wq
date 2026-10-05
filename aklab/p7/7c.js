const readline = require("readline");
const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
const ask = (q) => new Promise((res) => rl.question(q, res));

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
})();
const { recoverPersonalSignature } = require("eth-sig-util");
const { bufferToHex } = require("ethereumjs-util");

const myArgs = process.argv;
let signature = myArgs[2];
let publicAddress = myArgs[3];
let nonce = myArgs[4];

process.argv.forEach(function metamaskAuth() {
  if (!signature || !publicAddress || !nonce)
    return { error: "Request should have signature, publicAddress and nonce." };

  const msg = `I am signing my one-time nonce: ${nonce}`;
  // Extracting the signature of the user from the nonce !
  try {
    const msgBufferHex = bufferToHex(Buffer.from(msg, "utf8"));
    const address = recoverPersonalSignature({
      data: msgBufferHex,
      sig: signature,
    });

    if (address.toLowerCase() === publicAddress.toLowerCase()) {
      console.log("Verified");
    } else {
      console.log("Not verified");
    }
  } catch (error) {
    console.log("Invalid signature length");
  }
});

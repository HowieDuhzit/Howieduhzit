# Solana Tip Integration

This document outlines how to integrate Solana-based tipping functionality into your projects, inspired by the [sol-tip-jar](https://github.com/skiran017/sol-tip-jar) repository.

## Overview

Solana Tip Jar is a Web 3.0 solution for accepting tips/donations on the Solana network using Phantom wallet. This provides a modern alternative to traditional Web 2.0 payment methods.

## Features

- ⚡ **Solana Network Integration** - Fast, low-fee transactions
- 👻 **Phantom Wallet Support** - Most popular Solana wallet
- 🔧 **React Components** - Easy integration with React applications
- 🎣 **Hook-based API** - Custom implementation options
- 🌐 **Multiple Networks** - Devnet, Testnet, Mainnet support

## Quick Start

### Installation

```bash
npm install solana-tipjar
# or
yarn add solana-tipjar
```

### Basic Implementation

#### React Component (Recommended)

```jsx
import React from 'react';
import { TipWidgetWrapper } from 'solana-tipjar';

function SolanaTipButton() {
  return (
    <TipWidgetWrapper
      network="mainnet-beta"
      recieverAddress="8kQnN2mEjNcX4xKkHnX2a3b8vR7nJ5g6mN4oP9qR2tU7vW9xY1zA2bC3dE4fG5hI6jK7lM8nO9pQ"
    />
  );
}
```

#### Hook-based Implementation

```jsx
import React, { useState } from 'react';
import { useTipJar } from 'solana-tipjar';

function CustomTipInterface() {
  const [tipAmount, setTipAmount] = useState(0.1);

  const {
    phantomWalletExists,
    connectWallet,
    sendTransaction,
    transactionStatus,
    userWalletAddressLoaded,
    resetTipJar
  } = useTipJar({ network: "mainnet-beta" });

  if (!phantomWalletExists) {
    return (
      <div>
        <p>Install Phantom Wallet to send tips</p>
        <a href="https://phantom.app/" target="_blank" rel="noopener noreferrer">
          Get Phantom Wallet
        </a>
      </div>
    );
  }

  if (transactionStatus === "confirmed") {
    return (
      <div>
        <p>Thank you for your support! 🎉</p>
        <button onClick={() => {
          setTipAmount(0.1);
          resetTipJar();
        }}>
          Send Another Tip
        </button>
      </div>
    );
  }

  return (
    <div>
      {!userWalletAddressLoaded ? (
        <button onClick={connectWallet}>
          Connect Phantom Wallet
        </button>
      ) : (
        <div>
          <input
            type="number"
            value={tipAmount}
            onChange={(e) => setTipAmount(parseFloat(e.target.value))}
            step="0.01"
            min="0.01"
            placeholder="SOL amount"
          />
          <button
            onClick={() => sendTransaction(
              tipAmount,
              "8kQnN2mEjNcX4xKkHnX2a3b8vR7nJ5g6mN4oP9qR2tU7vW9xY1zA2bC3dE4fG5hI6jK7lM8nO9pQ"
            )}
            disabled={tipAmount <= 0}
          >
            Send {tipAmount} SOL Tip
          </button>
        </div>
      )}
    </div>
  );
}
```

## Configuration Options

### Component Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `network` | "devnet" \| "testnet" \| "mainnet-beta" | "devnet" | Solana network |
| `recieverAddress` | string | - | Your Solana wallet address |

### Hook Options

```typescript
interface UseTipJarOptions {
  network?: "devnet" | "testnet" | "mainnet-beta";
}
```

### Hook Return Values

```typescript
interface UseTipJarReturn {
  phantomWalletExists: boolean;
  connectWallet: () => void;
  sendTransaction: (amount: number, address: string) => void;
  transactionStatus: "idle" | "submitting" | "submitted" | "confirmed" | "error";
  userWalletAddressLoaded: boolean;
  resetTipJar: () => void;
}
```

## Network Configuration

### Mainnet (Production)
```javascript
network: "mainnet-beta"
recieverAddress: "8kQnN2mEjNcX4xKkHnX2a3b8vR7nJ5g6mN4oP9qR2tU7vW9xY1zA2bC3dE4fG5hI6jK7lM8nO9pQ"
```

### Devnet (Development)
```javascript
network: "devnet"
recieverAddress: "YourDevnetWalletAddress"
```

## Browser Compatibility

### Phantom Wallet Detection
The library automatically detects if Phantom wallet is installed:

```javascript
if (!phantomWalletExists) {
  // Show installation prompt
}
```

### Global Object Fix
If you encounter `global is undefined` errors, add this to your HTML head:

```html
<script>
  if (global === undefined) {
    var global = window;
  }
</script>
```

## Error Handling

```javascript
// Transaction status monitoring
switch (transactionStatus) {
  case "idle":
    // Ready for transaction
    break;
  case "submitting":
    // Transaction being processed
    break;
  case "submitted":
    // Transaction submitted to network
    break;
  case "confirmed":
    // Transaction confirmed
    break;
  case "error":
    // Transaction failed
    break;
}
```

## Security Considerations

1. **Wallet Address Verification**: Always verify the recipient address
2. **Network Selection**: Use appropriate network for your use case
3. **Transaction Monitoring**: Track transaction status for user feedback
4. **Error Handling**: Implement proper error handling for failed transactions

## Integration Examples

### GitHub Profile Integration
Add to your README.md:

```markdown
## Support My Work

<a href="https://solscan.io/account/YOUR_WALLET_ADDRESS">
  <img src="https://img.shields.io/badge/Send%20SOL%20Tip-9945FF?style=for-the-badge&logo=solana&logoColor=white" alt="Solana Tip" />
</a>
```

### Web Application Integration
```jsx
// In your React component
import { TipWidgetWrapper } from 'solana-tipjar';

function SupportSection() {
  return (
    <div>
      <h3>Support Development</h3>
      <TipWidgetWrapper
        network="mainnet-beta"
        recieverAddress="8kQnN2mEjNcX4xKkHnX2a3b8vR7nJ5g6mN4oP9qR2tU7vW9xY1zA2bC3dE4fG5hI6jK7lM8nO9pQ"
      />
    </div>
  );
}
```

## Benefits

- ⚡ **Fast Transactions** - Solana's high throughput
- 💰 **Low Fees** - Minimal transaction costs
- 🔒 **Secure** - Cryptographic security
- 🌐 **Decentralized** - No intermediaries
- 🎯 **Direct Support** - Funds go directly to developers

## Getting Started

1. Install the package: `npm install solana-tipjar`
2. Set up your Solana wallet address
3. Choose component or hook implementation
4. Configure network settings
5. Test on devnet before mainnet deployment

This integration provides a modern, Web 3.0 way for supporters to contribute to your open source projects and development work.

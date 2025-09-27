import React, { useState } from 'react';
import { useTipJar } from 'solana-tipjar';

/**
 * SolanaTipButton - A reusable component for accepting Solana tips
 * Inspired by: https://github.com/skiran017/sol-tip-jar
 *
 * @param {Object} props
 * @param {string} props.recipientAddress - Solana wallet address to receive tips
 * @param {string} props.network - Network to use (devnet, testnet, mainnet-beta)
 * @param {string} props.buttonText - Custom button text
 * @param {string} props.className - Additional CSS classes
 */
export default function SolanaTipButton({
  recipientAddress = "HowieDuhzit.sol",
  network = "mainnet-beta",
  buttonText = "Send SOL Tip",
  className = ""
}) {
  const [tipAmount, setTipAmount] = useState(0.1);
  const [showCustomAmount, setShowCustomAmount] = useState(false);

  const {
    phantomWalletExists,
    connectWallet,
    sendTransaction,
    transactionStatus,
    userWalletAddressLoaded,
    resetTipJar
  } = useTipJar({ network });

  // Loading state
  if (transactionStatus === "submitting" || transactionStatus === "submitted") {
    return (
      <div className={`solana-tip-container ${className}`}>
        <button className="solana-tip-button loading" disabled>
          <span className="loading-spinner"></span>
          Processing...
        </button>
      </div>
    );
  }

  // Success state
  if (transactionStatus === "confirmed") {
    return (
      <div className={`solana-tip-container ${className}`}>
        <div className="success-message">
          <span className="success-icon">✅</span>
          <p>Thank you for your support!</p>
          <button
            className="reset-button"
            onClick={() => {
              setTipAmount(0.1);
              setShowCustomAmount(false);
              resetTipJar();
            }}
          >
            Send Another Tip
          </button>
        </div>
      </div>
    );
  }

  // Error state
  if (transactionStatus === "error") {
    return (
      <div className={`solana-tip-container ${className}`}>
        <div className="error-message">
          <span className="error-icon">❌</span>
          <p>Transaction failed. Please try again.</p>
          <button
            className="retry-button"
            onClick={() => resetTipJar()}
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  // No Phantom wallet
  if (!phantomWalletExists) {
    return (
      <div className={`solana-tip-container ${className}`}>
        <div className="wallet-prompt">
          <p>Install Phantom Wallet to send tips</p>
          <a
            href="https://phantom.app/"
            target="_blank"
            rel="noopener noreferrer"
            className="wallet-link"
          >
            Get Phantom Wallet
          </a>
        </div>
      </div>
    );
  }

  return (
    <div className={`solana-tip-container ${className}`}>
      {!userWalletAddressLoaded ? (
        <button
          className="solana-tip-button connect"
          onClick={connectWallet}
        >
          Connect Phantom Wallet
        </button>
      ) : (
        <div className="tip-interface">
          <div className="amount-selector">
            <div className="preset-amounts">
              {[0.1, 0.5, 1.0, 5.0].map((amount) => (
                <button
                  key={amount}
                  className={`amount-preset ${tipAmount === amount ? 'active' : ''}`}
                  onClick={() => setTipAmount(amount)}
                >
                  {amount} SOL
                </button>
              ))}
            </div>

            <button
              className="custom-amount-toggle"
              onClick={() => setShowCustomAmount(!showCustomAmount)}
            >
              {showCustomAmount ? 'Preset Amounts' : 'Custom Amount'}
            </button>
          </div>

          {showCustomAmount && (
            <div className="custom-amount-input">
              <input
                type="number"
                value={tipAmount}
                onChange={(e) => setTipAmount(parseFloat(e.target.value) || 0)}
                step="0.01"
                min="0.01"
                placeholder="Enter SOL amount"
                className="amount-input"
              />
              <span className="sol-symbol">SOL</span>
            </div>
          )}

          <button
            className="solana-tip-button send"
            onClick={() => {
              if (tipAmount > 0 && recipientAddress) {
                sendTransaction(tipAmount, recipientAddress);
              }
            }}
            disabled={tipAmount <= 0 || !recipientAddress}
          >
            {buttonText} ({tipAmount} SOL)
          </button>

          <div className="tip-info">
            <small>
              Powered by Solana • Low fees • Fast transactions
            </small>
          </div>
        </div>
      )}
    </div>
  );
}

// CSS Styles (add to your component or global styles)
export const solanaTipStyles = `
.solana-tip-container {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.solana-tip-button {
  background: linear-gradient(135deg, #9945FF, #14F195);
  border: none;
  border-radius: 8px;
  color: white;
  padding: 12px 24px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.solana-tip-button:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(153, 69, 255, 0.3);
}

.solana-tip-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.loading-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.success-message, .error-message {
  text-align: center;
  padding: 20px;
  border-radius: 8px;
}

.success-message {
  background: rgba(20, 241, 149, 0.1);
  border: 1px solid #14F195;
}

.error-message {
  background: rgba(255, 69, 69, 0.1);
  border: 1px solid #ff4545;
}

.success-icon, .error-icon {
  font-size: 24px;
  margin-bottom: 8px;
  display: block;
}

.wallet-prompt {
  text-align: center;
  padding: 20px;
}

.wallet-link {
  display: inline-block;
  background: #9945FF;
  color: white;
  padding: 10px 20px;
  border-radius: 6px;
  text-decoration: none;
  margin-top: 10px;
}

.wallet-link:hover {
  background: #7c3aed;
}

.amount-selector {
  margin-bottom: 15px;
}

.preset-amounts {
  display: flex;
  gap: 8px;
  margin-bottom: 10px;
  flex-wrap: wrap;
}

.amount-preset {
  background: rgba(153, 69, 255, 0.1);
  border: 1px solid #9945FF;
  border-radius: 6px;
  padding: 6px 12px;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.amount-preset.active,
.amount-preset:hover {
  background: #9945FF;
  color: white;
}

.custom-amount-toggle {
  background: transparent;
  border: 1px solid #9945FF;
  color: #9945FF;
  border-radius: 6px;
  padding: 6px 12px;
  font-size: 12px;
  cursor: pointer;
}

.custom-amount-input {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 15px;
}

.amount-input {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #9945FF;
  border-radius: 6px;
  background: transparent;
  color: white;
  font-size: 14px;
}

.sol-symbol {
  color: #9945FF;
  font-weight: 600;
  font-size: 14px;
}

.tip-info {
  text-align: center;
  margin-top: 10px;
}

.tip-info small {
  color: rgba(255, 255, 255, 0.6);
  font-size: 11px;
}

.reset-button, .retry-button {
  background: #9945FF;
  border: none;
  border-radius: 6px;
  color: white;
  padding: 8px 16px;
  font-size: 12px;
  cursor: pointer;
  margin-top: 10px;
}
`;

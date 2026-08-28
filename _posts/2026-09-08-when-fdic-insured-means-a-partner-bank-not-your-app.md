---
layout: post
title: "When 'FDIC Insured' Means a Partner Bank, Not Your App"
date: 2026-09-08 11:26:40 +0000
categories: [savings]
description: "Pass-through deposit insurance covers the failure of the partner bank holding a fintech's pooled custodial account — not the app, not the middleware, and not a gap between the ledger and the cash."
tags: [savings, fdic-insurance, fintech, deposit-accounts, consumer-protection]
---

![When "FDIC Insured" Means a Partner Bank, Not Your App](/assets/pin-images/2026-09-08-when-fdic-insured-means-a-partner-bank-not-your-app.png)

The app shows a balance, and somewhere near the bottom of the screen a line says deposits are [FDIC](https://www.fdic.gov/resources/deposit-insurance) insured up to $250,000 through a partner bank. The balance is a number the app maintains. The money is at a bank you never applied to, pooled in one account with everyone else's.

Both things are true at once, and the distance between them is the entire subject. It caught tens of thousands of people in 2024, and not one of them was at a bank that failed.

## One account, many owners

A fintech company without a bank charter of its own cannot hold deposits. It contracts with an insured institution and places customer funds there in a custodial account, often titled "for the benefit of" its users. One account number. One balance on the bank's books.

Which slice of that balance is yours is not something the bank observes. It lives in a ledger kept by the fintech, or by a middleware provider sitting between the app and the bank. When the FDIC [proposed a rule](https://www.fdic.gov/news/press-releases/2024/fdic-proposes-deposit-insurance-recordkeeping-rule-banks-third-party) on this in September 2024, it stated the problem plainly: non-banks "often deposit these funds together into a single custodial account at a bank," and "the bank may not readily know or be able to determine the individual owners of funds in the custodial account."

Two things follow. Money you have sent to the app is not insured while it is in transit, because coverage attaches only once the funds are actually on deposit at an insured bank. And a fintech without a charter is never the insured party: the app, the payment company, the program manager carry no FDIC insurance of their own, only access to a bank that does. A handful of fintechs have gone the other way and obtained charters — Varo Bank, N.A. and SoFi Bank, N.A. are insured banks in their own right — and that exception announces itself, because the insured name on the disclosure is the company's own.

## The conditions the coverage turns on

Pass-through insurance is conditional, and the [FDIC's three requirements](https://www.fdic.gov/financial-institution-employees-guide-deposit-insurance/pass-through-deposit-insurance-coverage) are worth reading in order.

First, the funds must "be in fact owned by the principal and not by the third party who set up the account." Second, the bank's "account records must indicate the agency nature of the account." Third, the records of the bank, of the third party depositing the funds, or of another third party in the usual course of business must indicate "both the identities of the principals as well as their ownership interests."

Then comes the sentence that decides everything: "If all of these requirements are not satisfied, the deposits will be insured to the named account owner (typically the third party), aggregated with any other funds that the third party holds at the same bank in the same deposit insurance category."

Coverage does not fail down to $250,000 apiece. It fails down to $250,000 for the account. One limit, on a pooled balance that may hold money belonging to thousands of people.

The third requirement is the one doing the real work, and it is the one you cannot inspect. Your coverage rests on the accuracy of a ledger maintained by a company whose bookkeeping you have no way to audit.

There is a second boundary, easier to miss, that no amount of recordkeeping can move. Pass-through decides how a balance is divided. It does not create balance. FDIC Vice Chairman Travis Hill put it in one line in his [September 2024 statement](https://www.fdic.gov/news/speeches/2024/notice-proposed-rulemaking-custodial-deposit-accounts-transaction-features-and) on the proposal: "the FDIC's authority only extends to money actually deposited at a bank." Insurance is measured against the bank's balance, not the app's. If the ledger says more than the bank holds, the difference was never insured, and the bank failing does not change that. Satisfying all three conditions perfectly would divide the real balance correctly among its real owners and stop there.

## The failure that insurance is not aimed at

Deposit insurance answers one question: what happens when an insured bank fails. It has nothing to say about the company standing between you and that bank.

Synapse Financial Technologies was middleware, connecting consumer-facing apps to partner banks. It filed for Chapter 11 on April 22, 2024. No bank went into receivership, so no insurance determination was ever made.

Access stopped anyway. [CFPB](https://www.consumerfinance.gov/) Director Rohit Chopra, writing as a member of the FDIC Board on September 17, 2024, [described](https://www.consumerfinance.gov/about-us/newsroom/statement-of-cfpb-director-rohit-chopra-member-fdic-board-of-directors-on-stopping-fintech-deposit-meltdowns/) the result: "tens of thousands of customers have had their funds frozen for months." The reconciliation that would have released the money could not be completed, because the banks' records and Synapse's records did not agree.

They disagreed by a wide margin. The CFPB's [complaint](https://www.consumerfinance.gov/enforcement/actions/synapse-financial-technologies-inc/), filed August 21, 2025, states that the partnering banks "determined that the total funds they were holding for consumers was less than the total amount of consumer funds reflected in records Synapse provided to them, reflecting a shortfall of between $60 and $90 million." The alleged violation was the recordkeeping itself: failing to maintain adequate records of where consumers' funds were, and failing to ensure those records matched the banks'. A stipulated judgment entered September 12, 2025 imposed a civil money penalty of $1, the company being in bankruptcy.

A shortfall of that kind has no insurance answer, and it would not acquire one if a partner bank had also failed. What it gets instead is a bankruptcy court. Someone has to reconstruct ownership from records that were already wrong. Banks that never saw individual names have to agree with a reconstruction they have no independent way to check. Every party runs up professional fees against an estate smaller than the claims on it, and the customers whose balances are being argued over are not in the room. The FDIC states the boundary directly on its [consumer page](https://www.fdic.gov/consumer-resource-center/2024-06/banking-third-party-apps): deposit insurance "does not protect against the insolvency or bankruptcy of a nonbank company," and on how long recovery through such a proceeding takes, the agency's own phrase is that "such recovery may take some time."

| | Partner bank fails | App or middleware fails |
|---|---|---|
| Who takes over | FDIC as receiver | Bankruptcy court and trustee |
| What decides your payout | The bank's actual balance, divided by records that satisfy the pass-through conditions | Records, plus how much cash the banks actually hold |
| Deposit insurance | Applies, if the conditions are met | Not triggered |
| Gap between ledger and cash | Not insured; the FDIC pays only on funds actually on deposit at the bank | Falls on customers |
| Timeline | Next business day for ordinary accounts; longer for a pooled custodial account, where the FDIC must first reconcile who owns what | Months, in the 2024 case |

The second column is the more probable event. Bank failures are rare. Fintech companies close, get acquired, and lose their bank partners on an ordinary schedule.

## What the disclosure is now required to say

Subpart B of the FDIC's Part 328 rules carried a compliance date of January 1, 2025. Under [section 328.102(b)(5)](https://www.law.cornell.edu/cfr/text/12/328.102), a statement about deposit insurance counts as omitting material information when the absence of that information could lead a reasonable consumer to a false impression. Four specific cases are listed.

A non-insured company representing that a product is FDIC-insured must clearly and conspicuously identify the insured depository institution or institutions with which it has a direct or indirect business relationship. It must disclose that it is not itself an FDIC-insured depository institution "and that FDIC insurance only covers the failure of the FDIC-insured depository institution" — the sentence this whole piece is about, already written into the rule. It must distinguish insured deposits from non-deposit products. And a statement about pass-through coverage must clearly and conspicuously disclose "that certain conditions must be satisfied" for that coverage to apply.

Those are required sentences now, not optional fine print. The second and the fourth, read together, are the shortest possible summary of everything above, which is the argument for stopping on them rather than scrolling past.

The FDIC's September 2024 proposal would go further. Banks holding custodial accounts with transactional features would have to keep records identifying each beneficial owner and that owner's balance, reconcile them at the close of every business day, and maintain internal controls over the process, including where a third party keeps the ledger. The formal title says what the recordkeeping is for: "Requirements for Custodial Deposit Accounts with Transactional Features and Prompt Payment of Deposit Insurance to Depositors." Prompt payment is in the title because prompt payment is the thing that does not currently happen. The FDIC cannot pay out a pooled account until it knows who owns what, and when the ownership record sits at a company the receiver does not control, that determination is the delay. The proposal was [published](https://www.federalregister.gov/documents/2024/10/02/2024-22565/recordkeeping-for-custodial-accounts) on October 2, 2024, and the comment period closed on January 16, 2025 after [an extension](https://www.fdic.gov/news/financial-institution-letters/2024/fdic-extends-comment-period-proposed-rule-custodial-deposit). As of this writing it is still a proposal — never finalized, never withdrawn — and the recordkeeping behind your balance is whatever the app's bank contract calls for.

## What to check on the app you use

1. **Name the bank.** It is in the deposit account agreement or the terms of service, not on the marketing page. Confirm the charter through the FDIC's [BankFind](https://banks.data.fdic.gov/bankfind-suite/bankfind) tool. If the name that comes back is the app's own, the company holds a charter and is itself the insured bank, which is a different and simpler arrangement than everything described here. If no bank is named anywhere, that is the answer to what the insurance line means.
2. **Find out whether there is a middleware layer.** Some apps hold their account at the partner bank directly. Others reach it through a banking-as-a-service provider whose name appears nowhere on the screen. Synapse was that layer for apps whose customers had never heard of it. The terms of service sometimes name it, and support sometimes will. A party you cannot name is a party whose bankruptcy can freeze your balance.
3. **Look for a bank list rather than a single name.** Some apps spread balances across several partner banks, which raises an aggregation question the app cannot answer: deposits you hold directly at one of those banks combine with your app balance against the same $250,000 limit. How that stacking works across account types is [covered separately](/2026/08/21/how-fdic-ownership-categories-stack-coverage-at-one-bank/), and the same pooled structure inside a brokerage sweep program is [covered here](/2026/08/30/where-brokerage-cash-actually-sits-and-what-insures-it/).
4. **Find the pass-through sentence.** The conditions language has been required since January 2025. An app that invokes FDIC insurance without it is worth a second look.
5. **Ask who keeps the ledger.** Support can usually say whether the bank maintains records of individual ownership or whether the app or a program manager does. The answer sets how quickly anyone could prove your balance is yours.
6. **Export your own records monthly.** Statements and transaction history downloads are the only copy of the ledger you control. In 2024 that was what customers had while other people's records were being reconciled.
7. **Split the balance by what it does.** Rent, payroll, and the next tax payment belong at a bank you can name and log into directly. Yield-chasing money can sit behind more layers, at a size you could stand to have frozen for a quarter.

The banks stayed solvent through all of it. The money was frozen anyway, because nobody could prove whose it was, and that is the failure the line at the bottom of the screen was never written to answer.

## Further Reading

- [Is Your Money Market Fund Safe? What Changed After 2023](/2026/09/07/money-market-funds-after-the-2023-reforms-fees-not-gates/)
- [Trust Account Coverage After the 2024 FDIC Rule Change](/2026/09/06/trust-account-coverage-after-the-2024-fdic-rule-change/)
- [Why Your Deposit Is Not Available Yet: Funds Availability Rules](/2026/09/05/why-your-deposit-is-not-available-yet-funds-availability-rules/)
- [How a Savings Account Goes Dormant and Ends Up With the State](/2026/09/04/how-a-savings-account-goes-dormant-and-ends-up-with-the-state/)
- [When Your Bank Is Acquired, Not Failed: What Happens to Your CD](/2026/09/03/when-your-bank-is-acquired-not-failed-what-happens-to-your-cd/)


---
layout: post
title: "How to Verify a Bank Is Actually FDIC-Insured Before You Transfer"
date: 2026-09-09 09:03:42 +0000
categories: [savings]
description: "A one-minute BankFind lookup that reverses the direction of trust — plus the fields to read, the false positives that trip up honest banks, and what to do when the app holding your money is not itself a bank."
tags: [savings, fdic, deposit-insurance, bankfind, fraud-prevention, personal-finance]
---

![How to Verify a Bank Is Actually FDIC-Insured Before You Transfer](/assets/pin-images/2026-09-09-how-to-verify-a-bank-is-actually-fdic-insured-before-you-transfer.png)

You found a savings rate that beats your current bank by a full point. The site looks professional. The footer says "Member [FDIC](https://www.fdic.gov/resources/deposit-insurance)." Before the money moves, there is a lookup that takes under a minute and answers the question that footer cannot.

## Ask the FDIC which bank owns the domain

[BankFind Suite](https://banks.data.fdic.gov/bankfind-suite/bankfind) is the FDIC's public register of insured institutions. It searches on institution name, FDIC certificate number, web address, location, or branch office.

Start with the web address, because it reverses the direction of trust. Rather than asking a website whether it is insured, you ask the FDIC which insured bank owns that domain.

Type the domain exactly as it sits in your browser's address bar right now. Copy it straight out of the bar. The email that brought you here and the ad that sold you the rate are the two places a wrong domain comes from.

A clean result returns exactly one institution. Searching `www.ally.com` returns Ally Bank, certificate 57803, headquartered in Sandy, Utah. One domain, one charter, one number.

Then try `www.chase.com` and the count comes back zero. The web address on file for JPMorgan Chase Bank is `www.jpmorganchase.com` — the holding company's domain, not the one tens of millions of customers log into every day. A consumer brand domain that differs from the registered one is common at large banks, because the FDIC carries a single address per institution: the one that institution reported.

Treat an empty result as an unfinished check. The next move is to search the institution's legal name, then confirm that the certificate number, city, and status on the record line up with what the site says about itself. That second pass takes another twenty seconds, and it is the pass a lookalike fails.

## Read the whole record, not just the name at the top

A genuine listing carries specific, cross-checkable facts. The certificate number is the anchor: every insured institution has one, it does not change, and it belongs to a charter rather than to a brand.

Pull up JPMorgan Chase Bank, National Association and the record shows certificate 628, main office in Columbus, Ohio, established January 1, 1824, insured since January 1, 1934, primary federal regulator the OCC, 5,389 offices.

Six fields worth reading on any institution you look up:

1. **Certificate number.** Write it down. If a site quotes a certificate number, search that number on its own and confirm it returns the same name.
2. **Insured since.** New charters open every year, so a recent date is ordinary on its own. A site claiming a century of heritage attached to an insurance date of 2024 is a contradiction. A gap of a decade or two usually means a charter conversion or a rebrand — Ally dates its story to a 1919 auto-finance company and its charter to 2004. The gap worth a phone call is the one that lands on the current year.
3. **Main office city and state.** Compare it against the address in the site's own deposit disclosures. Your memory and the first search result are the wrong benchmarks here, because a charter address is frequently something other than the corporate headquarters: the FDIC lists JPMorgan Chase Bank in Columbus, Ohio, while the parent company is famously a New York institution.
4. **Primary federal regulator.** OCC, [Federal Reserve](https://www.federalreserve.gov/monetarypolicy.htm), or FDIC. This tells you who supervises the charter, and it gives you the right agency to complain to later.
5. **Number of offices.** Read the count against what the site claims for itself. Ally's record shows a single office, which is exactly what an internet bank should look like. The mismatch to catch is a site promising a nationwide branch network on an office count of two.
6. **Active status.** Acquired and merged institutions stay in the database with their history attached.

There were 4,241 active FDIC-insured institutions in the FDIC's index as of late August 2026. The list is finite, and the agency publishes all of it, including through a public API at `api.fdic.gov` if you would rather query it directly.

## What lookalike sites actually get wrong

The FDIC's own description of fake bank sites is narrower and more useful than generic advice about looking suspicious.

Fake sites use the FDIC name or the "Member FDIC" logo to create a false sense of security. That text and that image copy in seconds.

Two URL patterns recur. Misspellings, where a letter is transposed or doubled somewhere in the middle of a familiar name. And the real bank's name buried as a subdomain of an unrelated domain — `realbankname.something-else.com` reads left to right as the bank, but the domain is the part immediately before the `.com`.

The FDIC also flags typos and unusual fonts in the emails that route people to these sites, and banking apps that request access to contacts, text messages, stored passwords, or credit card information.

One timing detail cuts both ways. The FDIC rule requiring an official *digital* sign on a bank's homepage, login page, and first account-opening screen carries a [compliance date of April 1, 2027](https://www.fdic.gov/deposit-insurance/questions-and-answers-related-fdics-part-328-final-rule). A real bank's website may not display it yet. A fake one can display a copy of it today. Treat the sign as decoration and the certificate number as the test.

On scale, from FTC figures the [FDIC cites](https://www.fdic.gov/consumer-resource-center/2025-06/bank-impersonation-scams-and-fake-banks): consumers reported $12.5 billion in fraud losses in 2024, with imposter scams the second-largest category by dollars lost. Bank impersonation was the most reported scam arriving by text message in 2022, up nearly twentyfold from 2019, at a typical loss of $3,000.

## When the name on the app is not the name on the charter

This is where most legitimate confusion sits. A large share of high-rate accounts are offered by companies that are not banks. They place your money at partner banks, and the coverage that reaches you is pass-through insurance.

The FDIC's position is direct. Deposit insurance does not protect against the insolvency or bankruptcy of a nonbank company, and funds you send to such a company are not insured unless and until the company deposits them at an insured bank.

So the verification changes shape. You stop checking the app and start checking the bank behind it.

| The claim on the site | What it asserts | What confirms it |
|---|---|---|
| "Member FDIC" | The company is itself an insured bank | Its name and domain return a certificate number in BankFind |
| "Held at FDIC-insured partner banks" | The company is not a bank; another institution holds the funds | Each named partner appears in BankFind, and the account agreement titles the funds for your benefit |
| "FDIC-insured up to $3 million" | Funds are spread across a network of banks | The network's bank list is disclosed, and none of those banks already holds money of yours |

If the brand name returns nothing, open the deposit account agreement, find the partner bank's legal name, and search that. A company unwilling to name the institutions holding customer deposits has a problem larger than your comfort level. In March 2024 the FDIC [issued cease-and-desist demands](https://www.fdic.gov/news/press-releases/2024/pr24016.html) to three companies over exactly that cluster of behavior: stating or suggesting they were FDIC-insured, misusing the FDIC name or logo, misrepresenting the nature or extent of deposit insurance, and failing to clearly identify the insured institutions where customer deposits were placed.

Where the bank list lives is itself a signal. A program that publishes its participating institutions on a page you can open before you sign up has made itself checkable. A program that mentions "our network of partner banks" and leaves it at that has handed you a claim with nothing behind it. When the list exists, run every name on it through [BankFind](https://banks.data.fdic.gov/bankfind-suite/bankfind) once and file the certificate numbers with your account records, because the roster changes and the disclosure should tell you when it does.

## Credit unions sit in a different register

Credit unions fall outside BankFind entirely, so a blank result there says only that you searched the wrong database. Federally insured credit unions are covered by the NCUA's Share Insurance Fund, also at $250,000 per member, per insured credit union, per ownership category.

The equivalent lookup is the NCUA's [Research a Credit Union](https://mapping.ncua.gov/ResearchCreditUnion) tool, which searches by charter number, name, type, status, state, and city, and reports insurance status alongside financial data.

## If the lookup does not resolve

Call the FDIC's National Center for Consumer and Depositor Assistance at 1-877-ASK-FDIC (1-877-275-3342), or file the question through [ask.fdic.gov](https://ask.fdic.gov/fdicinformationandsupportcenter/s/). The agency's own guidance on fake bank sites invites the question in as many words — "contact us, and we can verify it for you" — so give them the exact web address and ask whether it belongs to an insured institution.

Use a number you already have — the one printed on the back of your card, or one you found through the database rather than through the site in question. Every phone number, chat window, and support address on a fraudulent site is operated by the people who built it.

Since the FDIC was founded in 1933, no depositor has lost a penny of FDIC-insured funds. That record covers insured deposits at insured institutions, which is the specific thing a certificate number establishes.

## Further Reading

- [Is Your Money Market Fund Safe? What Changed After 2023](/2026/09/07/money-market-funds-after-the-2023-reforms-fees-not-gates/)
- [Trust Account Coverage After the 2024 FDIC Rule Change](/2026/09/06/trust-account-coverage-after-the-2024-fdic-rule-change/)
- [Why Your Deposit Is Not Available Yet: Funds Availability Rules](/2026/09/05/why-your-deposit-is-not-available-yet-funds-availability-rules/)
- [How a Savings Account Goes Dormant and Ends Up With the State](/2026/09/04/how-a-savings-account-goes-dormant-and-ends-up-with-the-state/)
- [When Your Bank Is Acquired, Not Failed: What Happens to Your CD](/2026/09/03/when-your-bank-is-acquired-not-failed-what-happens-to-your-cd/)


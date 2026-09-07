# CreditPrice Agent: State-Dependent Corporate Loan Pricing under Borrower Risk, Relationship History, and Dynamic Balance-Sheet Constraints

**Dmitry Kazakov**  
Independent Researcher  
September 2026

## Abstract

Loan pricing is often modeled as a borrower-level problem: estimate credit risk, add funding and capital costs, and choose a margin. This paper studies a different formulation. The economically relevant price of a corporate loan depends not only on the borrower but also on the lender's contemporaneous state. We introduce CreditPrice Agent, a transparent research framework in which the pricing policy conditions jointly on borrower risk, relationship history, price acceptance, market funding, and dynamic balance-sheet pressure. A structural synthetic data-generating process makes the counterfactual pricing problem observable and reproducible without using confidential bank data. In a reference simulation of 30,000 applications, the state-dependent policy changes quoted prices relative to a risk-and-demand-only optimizer and increases simulated total economic value by 7.9% relative to the risk-and-demand-only optimizer under the known data-generating process. Relative to the historical synthetic policy, the simulated EV improvement is 70.3%. These figures are simulation results, not empirical claims about any institution. The main contribution is conceptual and operational: corporate loan pricing is represented as a borrower-relationship-bank-state decision rather than a static markup over expected loss.

**Keywords:** corporate lending; loan pricing; risk-based pricing; price elasticity; balance-sheet optimization; machine learning; decision systems

**JEL:** G21, G32, C61, C63


## 1. Introduction

Credit pricing has a habit of looking simpler on a whiteboard than it does in a bank. A stylized formula starts with a reference rate, adds expected loss, funding, capital and a target margin, and produces a quote. This is useful, but incomplete. A loan is simultaneously a customer decision, a risk exposure and a balance-sheet transaction.

The same borrower can be economically attractive on Monday and expensive on Friday without any change in probability of default. Liquidity may have tightened. Capital may have become scarce. A sector limit may be close to binding. Funding may have moved. The borrower may also have revealed something through previous negotiations: a history of accepting 150 basis points above a competing quote is information, although perhaps not information one should announce too loudly at lunch.

This paper formulates individualized corporate-loan pricing as a state-dependent decision problem. The pricing state contains four blocks: borrower fundamentals and risk; relationship history; market and funding conditions; and the lender's own balance-sheet state. The action is the offered rate subject to economic floors and policy constraints, including an explicit no-offer action. The objective is expected economic value rather than acceptance, spread, or risk in isolation.

The contribution is deliberately narrower than a claim of inventing dynamic pricing. Prior work has already demonstrated offline reinforcement learning for consumer-credit pricing and has emphasized price responsiveness, default risk and long-run outcomes. Our extension asks what happens when the lender itself becomes part of the state. In corporate lending, where exposures are large, concentrated and capital-intensive, this distinction is not cosmetic.

The repository accompanying this paper implements the full simulation, estimation and pricing pipeline. No confidential observations are used. The synthetic DGP is explicit, seeded and inspectable. This matters because synthetic data are useful only when they expose assumptions; otherwise they are merely fictional data wearing a lab coat.

## 2. Related work and positioning

The closest methodological reference is Khraishi and Okhrati (2022), who formulate consumer-credit pricing as an offline reinforcement-learning problem and demonstrate a personalized pricing policy learned from static data. Their work is important for two reasons: it avoids unsafe online price experimentation and treats customer response as part of the pricing problem rather than an afterthought.

Our framework differs in unit of analysis and state definition. Corporate exposures are typically fewer, larger and more heterogeneous than retail applications. More importantly, the marginal economics of a corporate facility can depend materially on portfolio concentration, liquidity usage, capital consumption and tenor. We therefore make lender state explicit.

The project also relates to risk-based and profit-based pricing. Risk-based pricing maps expected loss and other cost components into a rate. Profit-based pricing additionally models demand or price response. CreditPrice Agent retains both ideas but places them inside a state-dependent economic-value objective.

This paper does not claim that every pricing problem requires reinforcement learning. In fact, the reference implementation intentionally starts with transparent supervised models and constrained grid optimization. A complicated algorithm is not a contribution by itself. Sometimes it is merely a very expensive way to rediscover a spreadsheet.

## 3. Problem formulation

Let borrower i at time t be represented by state

S_it = {X_it, H_it, M_t, B_t},

where X contains borrower fundamentals and risk variables, H relationship history, M market and funding conditions, and B the lender's balance-sheet state. The action a_it is an offered annualized rate r.

The policy chooses

r* = argmax_r E[V_it(r) | S_it]

subject to a minimum economic spread and any external policy constraints.

Expected value is decomposed as

V(r) = P(Accept=1 | r,S) × [NII(r) - EL - CapitalCost - StatePenalty + RelationshipValue].

Expected loss is approximated by EAD × PD × LGD. StatePenalty is a transparent function of capital pressure, liquidity pressure and sector-concentration pressure. The reference code uses linear penalties because interpretability is useful at this stage; a production implementation could replace them with marginal shadow prices derived from optimization of the full balance sheet.

The key comparative-static result follows immediately. Holding borrower variables fixed, an increase in the shadow cost of capital or liquidity raises the economically required price unless the higher price reduces acceptance so sharply that the transaction should not be pursued at all. Thus the correct action is not always 'charge more'. Sometimes the economically correct quote is effectively 'no thanks', expressed more politely through a constraint.

## 4. Synthetic data-generating process

The reference experiment contains 30,000 synthetic applications over 60 monthly states. Borrowers are assigned sector, revenue scale, EBITDA margin, leverage, interest coverage, relationship tenure, repayment quality and prior acceptance propensity. Market rates, funding spreads, liquidity pressure and capital pressure evolve over simulated time.

Latent PD is generated through a logistic structural equation driven primarily by leverage, interest coverage, repayment quality and relationship tenure. LGD is generated separately. A latent reservation rate combines market and funding rates, risk, relationship effects and noise. Historical offered rates are produced by an intentionally imperfect policy that is mostly risk-based.

Acceptance is sampled from a logistic response to the difference between reservation rate and offered rate. Defaults are sampled from latent PD with a modest adverse-selection adjustment. This design gives us something unavailable in ordinary observational data: the counterfactual response surface is known. We can therefore evaluate alternative policies against the DGP rather than pretending that every rejected loan would have behaved exactly like an accepted one.

The simulation is not intended to mimic any named bank. Monetary scales, coefficients and state variables are synthetic. The point is identification of mechanisms, not reverse engineering of an institution.

## 5. Estimation and policy construction

The reference pipeline splits months 0-47 for training and months 48-59 for out-of-time evaluation. A logistic PD model is fitted on borrower characteristics. Its out-of-time ROC AUC in the seeded run is 0.828. A separate logistic model estimates acceptance using borrower, relationship, market, facility and offered-rate features.

For each test application the optimizer searches a feasible rate grid from 6% to 30% in 25-basis-point increments. Candidate prices below market rate plus funding spread plus a minimum economic spread are rejected. Two optimized policies are compared.

The first policy uses borrower risk and estimated price acceptance but ignores balance-sheet penalties. The second, CreditPrice Agent, adds capital, liquidity and sector-concentration state. Both are evaluated using the known structural acceptance function from the synthetic DGP, not the fitted acceptance model. This separation is important: policy construction may be imperfect, while evaluation should exploit the fact that the simulation gives us ground truth.

## 6. Results

The historical synthetic policy quotes an average rate of 16.10%. The risk-and-demand-only optimizer quotes 16.60% on average, while the state-dependent policy quotes 17.60%.

Under the known DGP, the state-dependent policy increases aggregate simulated economic value by 7.9% relative to the risk-and-demand-only policy. Relative to the historical synthetic policy, the improvement is 70.3%. Mean structural acceptance is 24.2% for the agent versus 52.2% under the historical synthetic policy.

These numbers should be interpreted with discipline. They establish internal behavior of the simulation, not external performance. The useful result is the mechanism: the agent's price premium relative to the borrower-only optimizer moves with bank-state pressure. Two economically identical borrowers can therefore receive different quotes because the marginal balance-sheet cost of their loans differs at the decision date.

That is the feature, not a bug. The bug would be hiding the mechanism and calling it artificial intelligence.

## 7. Robustness, governance and failure modes

A credible pricing system needs more than a high objective value. At minimum, robustness analysis should vary demand elasticity, risk calibration, funding volatility, state-penalty coefficients, price-grid resolution and the correlation between borrower risk and willingness to pay.

Model governance is equally important. Protected attributes should not enter the pricing state, directly or through obvious proxies without a lawful and reviewed basis. Price-response models are especially sensitive because historical offers were themselves policy decisions. Naive supervised learning can reproduce historical discretion and call it optimization.

The framework therefore separates risk estimation, demand estimation and economic optimization. This is less fashionable than a single end-to-end network and much easier to challenge in a model committee. In banking, 'the model learned it' is not an explanation; it is the beginning of the meeting.

For real data, off-policy evaluation becomes central because counterfactual outcomes are not observed. Doubly robust estimators, inverse-propensity weighting and conservative offline RL are natural extensions. The codebase is structured so that the transparent optimizer can serve as a benchmark before more complex policies are introduced.

## 8. Limitations

The present study is synthetic. It does not model regulatory capital formulas in full, prepayment, covenant optionality, collateral dynamics, multi-product relationships, transfer pricing curves by tenor and currency, or endogenous competitor response. Acceptance is represented by a single binary decision. Corporate negotiations are usually messier and occasionally involve more people than the model has features.

The balance-sheet state is summarized by normalized pressure variables rather than a complete asset-liability model. This is intentional for a first reproducible implementation, but it limits quantitative interpretation.

Finally, the optimization is myopic at the transaction level. Relationship value is included as a static term, not as a fully dynamic customer lifetime value. A sequential formulation using offline RL would be appropriate when today's quote changes future borrowing, cross-sell, refinancing and default behavior.

## 9. Extensions

Three extensions are particularly useful.

First, replace normalized balance-sheet penalties with endogenous shadow prices from a constrained portfolio optimizer. Capital, liquidity and concentration would then acquire marginal economic costs directly from binding constraints.

Second, estimate heterogeneous price response with causal or uplift methods rather than ordinary supervised classification. The question is not simply who accepted historical offers, but how acceptance changes under a counterfactual price.

Third, move from one-step optimization to conservative offline reinforcement learning. The state would include evolving relationship value and portfolio state, and the reward would capture long-run risk-adjusted economics. The transparent policy in this repository should remain the benchmark. If the RL agent cannot beat a clear baseline out of sample, it has earned the right to be deleted.

## 10. Conclusion

CreditPrice Agent reframes corporate-loan pricing as a joint borrower-relationship-bank-state decision. Borrower risk remains necessary, but it is not sufficient. A loan consumes scarce balance-sheet resources, and the shadow cost of those resources changes over time.

The practical implication is straightforward: individualized pricing should condition on both sides of the transaction. The borrower has a state; so does the bank.

The research implication is that pricing models can be evaluated not only on prediction accuracy but on policy value under explicit economic constraints. The accompanying repository provides a reproducible starting point, with a visible DGP, transparent objective and baseline policies. The next useful step is not to add another neural network. It is to test the framework on properly governed historical data with defensible off-policy evaluation.

## References

Khraishi, R., & Okhrati, R. (2022). Offline Deep Reinforcement Learning for Dynamic Pricing of Consumer Credit. Proceedings of the Third ACM International Conference on AI in Finance, 325-333. DOI: 10.1145/3533271.3561682.

Levine, S., Kumar, A., Tucker, G., & Fu, J. (2020). Offline Reinforcement Learning: Tutorial, Review, and Perspectives on Open Problems. arXiv:2005.01643.

Phillips, R. L. (2020). Pricing Credit Products. In Pricing and Revenue Optimization. Stanford University Press.

Basel Committee on Banking Supervision. Basel Framework. Bank for International Settlements. Used as conceptual background for capital and liquidity constraints; the reference implementation does not reproduce regulatory formulas.

Repository note: all empirical-looking values in this paper are generated by the synthetic DGP distributed with the code and can be reproduced with seed 42.

## Experimenting with Pyomo

My understanding is that pyomo isn't typically integrated with ML models directly but since my beta customer price sensitivity model was a logistic regression I figured I could pull the coefficients from it and use that symbolic function as an input in a pyomo optimization problem. This was my attempt to do that - which produced a file with wildly errant rates. It seems the order of my feature columns was mixed up, leading to the error.

`Upon further consideration it seems like ML models can be integrated with pyomo as standard practice using tools like OMLT. But it doesn't seem to be the best route for black box models like XGBoost that can't be represented symbolically. So for the purposes of this project I think I was on the right track: build a custom optimization loop that interacts with both black box models without needing explicit coefficients.`

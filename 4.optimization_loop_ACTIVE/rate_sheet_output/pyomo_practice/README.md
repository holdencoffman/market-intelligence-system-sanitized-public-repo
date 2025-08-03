## Experimenting with Pyomo

My understanding is that pyomo isn't typically integrated with ML models directly but since my beta customer price sensitivity model was a logistic regression I figured I could pull the coefficients from it and use that symbolic function as an input in a pyomo optimization problem. This was my attempt to do that - which produced a file with wildly errant rates. It seems the order of my feature columns was mixed up, leading to the error.

`Upon further consideration it seems like ML models are in fact integrated with pyomo as standard practice using tools like OMLT. I'll have to use that next time.`

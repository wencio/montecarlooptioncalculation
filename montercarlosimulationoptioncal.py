import QuantLib as ql

# Option parameters
spot_price = 100
strike_price = 105
interest_rate = 0.05
volatility = 0.2
time_to_maturity = 1.0
num_simulations = 100000

# Create QuantLib objects
today = ql.Date(15, ql.May, 2023)
ql.Settings.instance().evaluationDate = today

# Define handles for spot price, interest rate, and volatility
spot_handle = ql.QuoteHandle(ql.SimpleQuote(spot_price))
rate_handle = ql.YieldTermStructureHandle(ql.FlatForward(today, ql.QuoteHandle(ql.SimpleQuote(interest_rate)), ql.Actual360()))
vol_handle = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(today, ql.NullCalendar(), ql.QuoteHandle(ql.SimpleQuote(volatility)), ql.Actual360()))

# Create a European option
option_type = ql.Option.Call
payoff = ql.PlainVanillaPayoff(option_type, strike_price)
exercise = ql.EuropeanExercise(today + ql.Period(int(time_to_maturity * 365), ql.Days))
option = ql.VanillaOption(payoff, exercise)

# Define a random number generator using SobolRsg
num_paths = num_simulations
num_samples = 1  # 1 sample per path
seqGen = ql.SobolBrownianGenerator(ql.BrownianBridgePathGenerator, ql.SobolRsg, num_paths, num_samples)

# Perform Monte Carlo simulations
time_steps = int(time_to_maturity * 365)
seqGenVec = ql.SequenceStatistics(time_steps)

engine = ql.MCEuropeanEngine(seqGen, spot_handle, rate_handle, vol_handle, False, False, num_paths, seqGenVec)
option.setPricingEngine(engine)
option_price = option.NPV()

print("Option Price (Monte Carlo):", option_price)
